from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient, DESCENDING
from datetime import datetime
import os
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# MongoDB connection
client = MongoClient(app.config['MONGODB_URI'])
db = client[app.config['DATABASE_NAME']]
events_collection = db['events']

# Create index for better query performance
events_collection.create_index([('timestamp', DESCENDING)])


def parse_push_event(payload):
    """Parse GitHub push event"""
    return {
        'author': payload['pusher']['name'],
        'action': 'PUSH',
        'to_branch': payload['ref'].split('/')[-1],
        'from_branch': None,
        'timestamp': datetime.utcnow()
    }


def parse_pull_request_event(payload):
    """Parse GitHub pull request event"""
    pr = payload['pull_request']
    action_type = payload['action']
    
    # For merged pull requests
    if action_type == 'closed' and pr.get('merged', False):
        return {
            'author': pr['user']['login'],
            'action': 'MERGE',
            'from_branch': pr['head']['ref'],
            'to_branch': pr['base']['ref'],
            'timestamp': datetime.utcnow()
        }
    # For opened/reopened pull requests
    elif action_type in ['opened', 'reopened']:
        return {
            'author': pr['user']['login'],
            'action': 'PULL_REQUEST',
            'from_branch': pr['head']['ref'],
            'to_branch': pr['base']['ref'],
            'timestamp': datetime.utcnow()
        }
    return None


@app.route('/')
def index():
    """Serve the main UI page"""
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    """GitHub webhook endpoint"""
    try:
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')
        
        event_data = None
        
        if event_type == 'push':
            event_data = parse_push_event(payload)
        elif event_type == 'pull_request':
            event_data = parse_pull_request_event(payload)
        
        if event_data:
            # Insert into MongoDB
            result = events_collection.insert_one(event_data)
            return jsonify({
                'status': 'success',
                'message': 'Event stored successfully',
                'id': str(result.inserted_id)
            }), 200
        
        return jsonify({
            'status': 'info',
            'message': 'Event not tracked'
        }), 200
        
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    """API endpoint to fetch latest events"""
    try:
        # Get the latest 10 events, sorted by timestamp descending
        events = list(events_collection.find(
            {},
            {'_id': 0}
        ).sort('timestamp', DESCENDING).limit(10))
        
        # Format timestamps for display
        for event in events:
            if 'timestamp' in event:
                event['timestamp'] = event['timestamp'].isoformat()
        
        return jsonify({
            'status': 'success',
            'events': events
        }), 200
        
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
