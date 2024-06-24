import json
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO
def album(data):
    #album details
    album_details=[]
    for row in data["items"]:
        album_id=row["track"]["album"]["id"]
        album_name=row["track"]["album"]["name"]
        album_release_date=row["track"]["album"]["release_date"]
        album_total_tracks=row["track"]["album"]["total_tracks"]
        album_url=row["track"]["album"]["external_urls"]["spotify"]
        album_elements={
            "album_id":album_id,
            "album_name":album_name,
            "album_release_date":album_release_date,
            "album_total_tracks":album_total_tracks,
            "album_url":album_url
                       }
        album_details.append(album_elements)
        
    return album_details     
def  artist(data):
    #Track details
    artists_details=[]
    for row in data["items"]:
        for key,value in row.items():
            if key=='track':
                for artist in value["artists"]:
                    artist_id=artist["id"]
                    artist_name=artist["name"]
                    artist_external_urls=artist["href"]
                    artist_elements={
                        "artist_id":artist_id,
                        "artist_name":artist_name,
                        "artist_external_urls":artist_external_urls
    
                    }
                    artists_details.append(artist_elements)
    return artists_details                 

def songs(data):
    songs_details=[]
    for row in data["items"]:
        song_id=row["track"]["id"]
        song_name=row["track"]["name"]
        song_duration=row["track"]["duration_ms"]
        song_url=row["track"]["external_urls"]["spotify"]
        song_added=row["added_at"]
        album_id=row["track"]["album"]["id"]
        artist_id=row["track"]["album"]["artists"][0]["id"]
        sonngs_elements={
            "song_id":song_id,
            "song_name":song_name,
            "song_duration":song_duration,
            "song_url":song_url,
            "song_added":song_added,
            "album_id":album_id,
            "artist_id":artist_id,
        }
        songs_details.append(sonngs_elements)
    return songs_details
    

def lambda_handler(event, context):
    try:
        s3=boto3.client('s3')
        Bucket ='spotify-etl-projectha'
        Key ='raw_data/to_processed/'
        spotify_data=[]
        spotify_keys=[]
        # print(s3.list_objects(Bucket=Bucket,Prefix=Key)["Contents"])
        for file in s3.list_objects(Bucket=Bucket,Prefix=Key)["Contents"]:
            file_key=file["Key"]
            # print(file_key.split('.')[-1])
            if file_key.split('.')[-1]=='json':
                repsonse = s3.get_object(Bucket=Bucket,Key=file_key)
                content = repsonse['Body']
                jsonObject = json.loads(content.read())
                spotify_data.append(jsonObject)
                spotify_keys.append(file_key)
        for data in spotify_data:
            album_details =  album(data)
            artists_details = artist(data)
            songs_details1 =  songs(data)
            #running
            #album
            album_df=pd.DataFrame.from_dict(album_details)
            album_df.drop_duplicates(subset=["album_id"])
            album_df["album_release_date"]=pd.to_datetime(album_df["album_release_date"])
            
            #artists
            artists_df=pd.DataFrame.from_dict(artists_details)
            artists_df.drop_duplicates(subset=["artist_id"])
            
            #songs
            songs_df=pd.DataFrame.from_dict(songs_details1)
            
            #album
            album_key = 'transformed_data/albums_data/album_transformed_'+str(datetime.now())+".csv"
            album_buffer = StringIO()
            album_df.to_csv(album_buffer,index=False)
            album_content = album_buffer.getvalue()
            s3.put_object(Bucket=Bucket ,Key=album_key,Body=album_content)
            #artist
            artist_key='transformed_data/artists_data/artist_transformed_'+str(datetime.now())+'.csv'
            artist_buffer=StringIO()
            artists_df.to_csv(artist_buffer,index=False)
            artist_content=artist_buffer.getvalue()
            s3.put_object(Bucket=Bucket ,Key=artist_key,Body=artist_content)
            
        
            
            songs_df["song_added"]=pd.to_datetime(songs_df["song_added"])
            song_key = 'transformed_data/songs_data/song_transformed_'+str(datetime.now())+".csv"
            song_buffer = StringIO()
            songs_df.to_csv(song_buffer,index=False)
            song_content = song_buffer.getvalue()
            s3.put_object(Bucket=Bucket ,Key=song_key,Body=song_content)
            
            
        s3_resource = boto3.resource('s3')
        for key in spotify_keys:
            copy_source = {
                    'Bucket':Bucket,
                    'Key':key
            }
            # print(copy_source)
            s3_resource.meta.client.copy(copy_source,Bucket, 'raw_data/processed/' + key.split("/")[-1])
            # print(data)
            s3_resource.Object(Bucket,key).delete()
            
    
    except Exception as err:
        print(err)
