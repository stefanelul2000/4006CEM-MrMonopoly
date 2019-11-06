import os
import random
import giphy_client
from giphy_client.rest import ApiException

giphy_token= os.environ.get('GIPHY_TOKEN')
api_instance = giphy_client.DefaultApi() #Giphy API

def search_gifs(query):
    try:
        return api_instance.gifs_search_get(giphy_token, query, limit=5, rating = 'g')

    except ApiException as e:
        return "Exception when calling DefaultApi->gifs_search_get: %s\n" % e

def gif_response(emotion):
    gifs = search_gifs(emotion)
    lst = list(gifs.data)
    gif = random.choices(lst)

    return gif[0].url
