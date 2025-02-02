from mastodon import Mastodon
from config import ACCESS_TOKEN
import random
from lyrics import lyrics_list

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

post_lyrics()
)
