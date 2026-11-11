import json
import urllib.request
import urllib.error

try:
    with open(r'C:\Users\Mattia\.gemini\oauth_creds.json', 'r') as f:
        creds = json.load(f)
    token = creds.get('access_token')
    
    req = urllib.request.Request(
        'https://serviceusage.googleapis.com/v1/projects/job-application-material/services/youtube.googleapis.com',
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("YouTube API status on job-application-material:", data.get('state'))
except Exception as e:
    print("Error checking YouTube API:", e)

