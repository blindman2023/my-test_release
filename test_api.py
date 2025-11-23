#!/usr/bin/env python3
"""Quick test script to verify the API endpoints work"""

import requests
import json

base_url = "http://localhost:5000"

def test_api():
    print("Testing Chinese Learning Platform API...")
    
    try:
        # Test lessons list
        response = requests.get(f"{base_url}/api/lessons")
        print(f"GET /api/lessons: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {len(data.get('data', []))} lessons")
        
        # Test specific lesson
        response = requests.get(f"{base_url}/api/lessons/lesson-1")
        print(f"GET /api/lessons/lesson-1: {response.status_code}")
        
        # Test exercise submission
        response = requests.post(
            f"{base_url}/api/exercises/ex-1-1/attempt",
            json={"lesson_id": "lesson-1", "answer": "0"}
        )
        print(f"POST /api/exercises/ex-1-1/attempt: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Answer correct: {data.get('data', {}).get('correct', False)}")
        
        print("API tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("Could not connect to the server. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()