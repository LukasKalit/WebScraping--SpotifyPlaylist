import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pprint

load_dotenv()

Client_ID = os.getenv("Client_ID")
Client_Secret = os.getenv("Client_Secret")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID,
                                               client_secret=Client_Secret,
                                               redirect_uri="http://example.com"))

# date = input("Chose a day you want to travel YYYY-MM-DD: ")
# print(date)

year = "2010"
html_doc = f"https://www.billboard.com/charts/hot-100/2010-12-27/"

response = requests.get(html_doc)
response.status_code

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all(class_="o-chart-results-list-row-container")
list_of_titles = [row.find("h3").string.strip() for row in links]
list_of_artists = [row.find("span", ["c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only", "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet"]).text.strip().split()[0] for row in links]

# print(links)
# print(list_of_titles)
# print(list_of_artists)


for i in range(100):
    query = f"track:{list_of_titles[i]} AND artist:{list_of_artists[i]}"
    playlists = sp.search(q=query, type="track", limit=1)
    # pprint.pprint(playlists)

    try:
        pprint.pprint(playlists["tracks"]["items"])
        for j in range(10):
            pprint.pprint(playlists["tracks"]["items"][j]["name"])
            pprint.pprint(playlists["tracks"]["items"][j]["external_urls"]["spotify"])

    except:
        pass
