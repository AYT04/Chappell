import feedparser
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import schedule
import time

# python -m venv myenv
# myenv\Scripts\activate  # on Windows
# source myenv/bin/activate  # on Linux/Mac
# pip install feedparser google-api-python-client google-auth-httplib2 google-auth-oauthlib schedule requests
# pip freeze > requirements.txt


# RSS feed URL
rss_feed_url = 'https://www.ohthatremindsme.com/feed.xml'

# Google Drive API credentials
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', 'https://www.googleapis.com/auth/drive')
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Create Google Drive API client
drive_service = build('drive', 'v3', credentials=creds)

def download_and_upload_podcast():
    # Parse RSS feed
    feed = feedparser.parse(rss_feed_url)
    latest_episode = feed.entries[0]

    # Download latest episode
    episode_url = latest_episode.links[0].href
    episode_title = latest_episode.title
    import requests
    response = requests.get(episode_url)
    with open(episode_title + '.mp3', 'wb') as f:
        f.write(response.content)

    # Upload episode to Google Drive
    file_metadata = {'name': episode_title + '.mp3'}
    media = MediaFileUpload(episode_title + '.mp3', mimetype='audio/mpeg')
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    # Remove downloaded episode
    os.remove(episode_title + '.mp3')

# Schedule task to run every Tuesday
schedule.every().tuesday.at("21:00").do(download_and_upload_podcast)  # 8am every Tuesday

while True:
    schedule.run_pending()
    time.sleep(1)
