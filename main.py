from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime

year = input("What year would you like to travel? ")
month = input("Which month? ")
day = input("Which day? ")

date = f"{year}-{month}-{day}"
month_name = datetime.datetime.strptime(f"{month}", "%m").strftime("%B")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
songs_web = response.text

soup = BeautifulSoup(songs_web, "html.parser")
all_titles = soup.select(selector="li h3", class_="c-title")
titles = [title.getText().strip() for title in all_titles[:100]]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=" ",
        client_secret=" ",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
uri = [sp.search(title, type='track')["tracks"]["items"][0]["uri"] for title in titles]
playlist_ID = sp.user_playlist_create(user=user_id, name=f"Top 100s of {year} {month_name} {day}", public=False)["id"]
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_ID, tracks=uri)