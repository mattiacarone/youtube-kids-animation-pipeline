import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

try:
    with open(r'C:\Users\Mattia\.gemini\oauth_creds.json', 'r') as f:
        data = json.load(f)
    
    # Check if there is client_id and client_secret
    print("Keys in creds:", list(data.keys()))
except Exception as e:
    print("Error:", e)

