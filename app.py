from mastodon import Mastodon
from config import *
import random
from lyrics import lyrics

# lista de letras
lyrics = lyrics

def lambda_handler(event, context):
    # seleciona um índice aleatório
    indice_selecionado = random.randint(0, len(lyrics) - 1)

    # autenticação com Mastodon
    mastodon = Mastodon(
        access_token=ACCESS_TOKEN,
        api_base_url='https://mastodon.social'
        # api_base_url=''
        # Choose an instance that allows the 'development' tab in settings.
        # I only know .social allows this.
    )

    # texto do toot
    texto_do_tweet = lyrics[indice_selecionado]

    # postar!
    mastodon.toot(texto_do_tweet)
