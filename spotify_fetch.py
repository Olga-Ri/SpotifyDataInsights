import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd

# get environment variables
load_dotenv()

# Spotify Credentials 
client_id = "612d9ac09f64466983707724a9d95da6"
client_secret = "60804efb333d41beaf2c5effcbe44ef5"

print("CLIENT ID:", client_id)
print("CLIENT SECRET:", client_secret)

# Authenticate w/ Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Sample songs from personal playlist
songs = [
    {'title': 'The Smallest Man Who Ever Lived', 'artist': 'Taylor Swift'},
    {'title': 'mirrorball', 'artist': 'Taylor Swift'},
    {'title': 'About You', 'artist': 'The 1975'},
    {'title': 'So Long, London', 'artist': 'Taylor Swift'},
    {'title': 'Please Please Please', 'artist': 'Sabrina Carpenter'},
    {'title': 'Espresso', 'artist': 'Sabrina Carpenter'},
    {'title': 'Need You Now', 'artist': 'Lady A'},
    {'title': 'Traitor', 'artist': 'Olivia Rodrigo'},
    {'title': '360', 'artist': 'Charli xcx'},
    {'title': 'The Body Is a Blade', 'artist': 'Japanese Breakfast'},
    {'title': 'En El Olvido', 'artist': 'Omar Apollo'},
    {'title': 'Fix You', 'artist': 'Coldplay'},
    {'title': 'Girl Crush', 'artist': 'Little Big Town'},
    {'title': 'SkeeYee', 'artist': 'Sexyy Red'},
    {'title': 'euphoria', 'artist': 'Kendrick Lamar'},
    {'title': 'I Hope You Dance', 'artist': 'Lee Ann Womack'},
    {'title': 'Clarity', 'artist': 'Zedd,Foxes'},
    {'title': 'One Of Your Girls', 'artist': 'Troye Sivan'},
    {'title': 'Yeah Glo!', 'artist': 'GloRilla'},
    {'title': 'Tennessee Whiskey', 'artist': 'Chris Stapleton'},
    {'title': 'ghostin', 'artist': 'Ariana Grande'}
]

data = []

for song in songs:
    query = f"track:{song['title']} artist:{song['artist']}"
    print(f"🔍 Searching for: {query}")
    result = sp.search(q=query, type='track', limit=1)

    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        track_id = track['id']
        popularity = track['popularity']
        album = track['album']['name']
        release_date = track['album']['release_date']
        print(f"✅ Found: {track['name']} — Popularity Score: {popularity}")

        if popularity is not None:
            data.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': album,
                'release_date': release_date,
                'popularity': popularity
            })
            print(f"✅ Added: {track['name']} — Popularity: {popularity}")
        else:
            print(f"⚠️ No popularity data for {track['name']}")
    else:
        print(f"❌ No track found for: {song['title']} by {song['artist']}")

# Save to CSV
if data:
    df = pd.DataFrame(data)
    #drop duplicates
    df = df.drop_duplicates(subset=['name', 'artist'])
    #sort by popularity
    df = df.sort_values(by='popularity', ascending=False)
    #standarize casing
    df['name'] = df['name'].str.title()
    df['artist'] = df['artist'].str.title()
    #save to CSV
    df.to_csv('spotify_audio_features.csv', index=False)
    print("✅ Data cleaned and saved to spotify_audio_features.csv")
else:
    print("⚠️ No data fetched — check your credentials or song list")





