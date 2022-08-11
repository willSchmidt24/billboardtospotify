import requests
from bs4 import BeautifulSoup
import spotipy

CLIENT_ID = CLIENT ID
CLIENT_SECRET = CLIENT SECRET
REDIRECT_URIS = REDIRECT URI

sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)

soup = BeautifulSoup(response.text, 'html.parser')
songs = soup.find_all(name="h3", class_="a-no-trucate")
song_titles = [song.getText().strip() for song in songs]
song_uris = []
year = date.split("-")[0]

for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} is not on Spotify.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
