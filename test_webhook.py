"""
Test script to verify webhook endpoint works correctly
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_push_event():
    """Test push event webhook"""
    print("Testing PUSH event...")
    payload = {
        "ref": "refs/heads/main",
        "pusher": {
            "name": "TestUser"
        }
    }
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "push"
    }
    response = requests.post(f"{BASE_URL}/webhook", 
                            json=payload, 
                            headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_pull_request_event():
    """Test pull request event webhook"""
    print("Testing PULL_REQUEST event...")
    payload = {
        "action": "opened",
        "pull_request": {
            "user": {
                "login": "TestUser"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request"
    }
    response = requests.post(f"{BASE_URL}/webhook", 
                            json=payload, 
                            headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_merge_event():
    """Test merge event webhook"""
    print("Testing MERGE event...")
    payload = {
        "action": "closed",
        "pull_request": {
            "merged": True,
            "user": {
                "login": "TestUser"
            },
            "head": {
                "ref": "feature-branch"
            },
            "base": {
                "ref": "main"
            }
        }
    }
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request"
    }
    response = requests.post(f"{BASE_URL}/webhook", 
                            json=payload, 
                            headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_get_events():
    """Test getting events from API"""
    print("Testing GET events...")
    response = requests.get(f"{BASE_URL}/api/events")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Retrieved {len(data.get('events', []))} events")
    print(json.dumps(data, indent=2))
    print()

if __name__ == "__main__":
    print("="*50)
    print("GitHub Webhook Receiver - Test Suite")
    print("="*50)
    print()
    
    try:
        test_health()
        test_push_event()
        test_pull_request_event()
        test_merge_event()
        test_get_events()
        
        print("="*50)
        print("All tests completed!")
        print("Check http://localhost:5000 to see the UI")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server.")
        print("Make sure the Flask app is running on http://localhost:5000")
        print("Run: python app.py")
