import json
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    client_id_value=os.environ.get('client_id')
    client_secret_value=os.environ.get('client_secret')
    client_credentials_manager=SpotifyClientCredentials(client_id=client_id_value, client_secret=client_secret_value)
    sp=spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
    play_list_uri=playlist_link.split('/')[-1].split('?')[0]
    spotify_data=sp.playlist_tracks(play_list_uri)
    file_name="spotify_raw_"+str(datetime.now())+".json"
    client= boto3.client('s3')
    client.put_object(
        Bucket="spotify-etl-projectha",
        Key="raw_data/to_processed/"+file_name,
        Body=json.dumps(spotify_data)
        )
    
#We need to create enviroment variable to store user and password details