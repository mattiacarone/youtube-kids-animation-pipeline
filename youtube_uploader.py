import os
import sys
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_PATH = "youtube_token.json"
SECRETS_PATH = "client_secrets.json"

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"Token load error: {e}")
            creds = None
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired YouTube access token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(SECRETS_PATH):
                print(f"\n[!] Required: '{SECRETS_PATH}' not found.")
                print("To enable 1-click automatic uploads to YouTube:")
                print("1. Go to https://console.cloud.google.com/apis/credentials")
                print("2. Create an OAuth 2.0 Client ID (Type: Desktop Application)")
                print("3. Download JSON and save it as 'client_secrets.json' in this folder.")
                return None
            
            print("Opening browser for 1-time YouTube channel authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
        print(f"YouTube authorization credentials saved to {TOKEN_PATH}.")

    return build("youtube", "v3", credentials=creds)

def upload_short(video_file, title, description, tags=None, category_id="27", privacy="public"):
    """
    Uploads a video to YouTube with Shorts and Made For Kids metadata.
    """
    if not os.path.exists(video_file):
        print(f"Error: Video file not found: {video_file}")
        return None

    service = get_authenticated_service()
    if not service:
        return None

    if tags is None:
        tags = ["Shorts", "Pixieland", "YouTubeKids", "LearnEnglish", "Preschool", "Cartoons"]

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": True
        }
    }

    media = MediaFileUpload(
        video_file,
        mimetype="video/mp4",
        resumable=True,
        chunksize=1024*1024*4
    )

    print(f"\nUploading '{video_file}' to YouTube as '{title}'...")
    request = service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%...")

    video_id = response.get("id")
    video_url = f"https://youtube.com/shorts/{video_id}"
    print(f"\n[SUCCESS] Short published successfully!")
    print(f"Short URL: {video_url}")
    return video_url

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = "output/Pixi_Wobbly_Penguin_Short.mp4"
    
    upload_short(
        video_file=video_path,
        title="Can You Waddle Like a Penguin? 🐧✨ | Pixieland English #Shorts",
        description="Pixi travels to Antarctica and meets a cute baby penguin! ❄️ Can you waddle like a penguin too? Subscribe to Pixieland for more learning adventures!\n\n#Shorts #YouTubeKids #LearnEnglish #Pixieland",
        tags=["Pixieland", "Kids", "YouTubeKids", "LearnEnglish", "Penguin", "Shorts", "ChildrensAnimation"],
        privacy="public"
    )

