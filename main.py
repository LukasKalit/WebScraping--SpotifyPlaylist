import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import pprint



#                 Environment Variable
load_dotenv()
Client_ID = os.getenv("Client_ID")
Client_Secret = os.getenv("Client_Secret")

#                  Connection to spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID,
                                               client_secret=Client_Secret,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private"))
user_name = sp.current_user()["id"]
print(user_name)

date = input("Chose a day you want to travel YYYY-MM-DD: ")
# print(date)


#                Taking data from site
html_doc = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(html_doc)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

#                 Scraping
links = soup.find_all(class_="o-chart-results-list-row-container")
list_of_titles = [row.find("h3").string.strip() for row in links]
list_of_artists = [row.find("span", ["c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max"
                                     " u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block"
                                     " a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only",
                                     "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height"
                                     "-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis"
                                     "-2line u-max-width-330 u-max-width-230@tablet-only u-font-size-20@tablet"]
                            ).text.strip().split()[0] for row in links]

# print(links)
# print(list_of_titles)
# print(list_of_artists)

#              Searching for songs in spotify

list_of_uri = []

for i in range(100):
    query = f"track:{list_of_titles[i]} AND artist:{list_of_artists[i]}"
    play_search = sp.search(q=query, type="track", limit=1)
    # pprint.pprint(playlists)

    try:
        # pprint.pprint(play_search["tracks"]["items"][0]["name"])
        # pprint.pprint(play_search["tracks"]["items"][0]["uri"])
        list_of_uri.append(str(play_search["tracks"]["items"][0]["uri"].split(":")[2]))

    except:
        pass

#               Create a playlist and save 100 songs on private account
playlist_ID = sp.user_playlist_create(user=user_name, name=f"Top 100 of {date}", public=False,
                                      description="Practising of using spotipy module")

sp.playlist_add_items(playlist_id=playlist_ID["id"], items=list_of_uri)

# pprint.pprint(playlist_ID)
# print(list_of_uri)
