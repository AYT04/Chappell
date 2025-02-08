from mastodon import Mastodon
from dotenv import load_dotenv
import os
import random
#from lyrics import lyrics_list
import schedule
import time

# Load environment variables from .env file
load_dotenv()

# Get the access token from environment variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

def post_lyrics():
    try:
        # Select a random index
        indice_selecionado = random.randint(0, len(lyrics_list) - 1)

        # Authenticate with Mastodon
        mastodon = Mastodon(
            access_token=ACCESS_TOKEN,
            api_base_url='https://mastodon.social'
        )

        # Get the text of the toot
        texto_do_tweet = lyrics_list[indice_selecionado]

        # Post the toot
        mastodon.toot(texto_do_tweet)
    except Exception as e:
        print(f"Error: {e}")

# Schedule the post_lyrics function to run every hour
schedule.every(1).hours.do(post_lyrics)

# Run indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
    
