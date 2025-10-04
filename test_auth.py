# test_auth.py
import requests
from base64 import b64encode

# Test authentication directly
def test_auth():
    # Encode credentials in base64
    credentials = b64encode(b"admin:admin123").decode('utf-8')
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('http://127.0.0.1:8000/tasks/', headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
        else:
            print("❌ Authentication failed")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_auth()