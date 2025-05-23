from MySpotifyStats import MySpotifyStats
from SpotifyStatsModel import SpotifyStatsModel
import datetime as dt

def simplify_top_songs(top_songs):
    top_songs_simplified = []
    for track in top_songs:
        # artist name
        artists = ', '.join(artist['name'] for artist in track['artists'])
        # track name
        track_name = track['name']
        # track id
        track_id = track['id']
        # track link
        track_link = track['external_urls']['spotify']
        # track image 640 x 640
        track_image_640 = track['album']['images'][0]['url']
        # track image 300 x 300
        track_image_300 = track['album']['images'][1]['url']
        # track image 64 x 64
        track_image_64 = track['album']['images'][2]['url']
        # track release date
        track_release_date = track['album']['release_date']
        top_songs_simplified.append({
            'artists': artists,
            'track_name': track_name,
            'track_id': track_id,
            'track_link': track_link,
            'track_image_640': track_image_640,
            'track_image_300': track_image_300,
            'track_image_64': track_image_64,
            'track_release_date': track_release_date
        })
    return top_songs_simplified 

def simplify_top_artists(top_artists):
    top_artists_simplified = []
    for artist in top_artists:
        # artist name
        artist_name = artist['name']
        # artist id
        artist_id = artist['id']
        # artist link
        artist_link = artist['external_urls']['spotify']
        #artist genres
        artist_genres = ', '.join(artist['genres'])
        # artist popularity
        artist_popularity = artist['popularity']
        # artist followers
        artist_followers = artist['followers']['total']
        # artist image 640 x 640
        artist_image_640 = artist['images'][0]['url']
        # artist image 300 x 300
        artist_image_300 = artist['images'][1]['url']
        # artist image 64 x 64
        artist_image_64 = artist['images'][2]['url']
        top_artists_simplified.append({
            'artist_name': artist_name,
            'artist_id': artist_id,
            'artist_link': artist_link,
            'artist_genres': artist_genres,
            'artist_popularity': artist_popularity,
            'artist_followers': artist_followers,
            'artist_image_640': artist_image_640,
            'artist_image_300': artist_image_300,
            'artist_image_64': artist_image_64
        })
    return top_artists_simplified



stats = MySpotifyStats()
stats_model = SpotifyStatsModel("http://192.168.1.130:8090")


# get dates for beginning of last year and end of last year
start_date = dt.date(dt.datetime.now().year - 1, 1, 1)
end_date = dt.date(dt.datetime.now().year - 1, 12, 31)
year = int(dt.datetime.now().year - 1)
token = stats.get_access_token()

# # update total minutes listened to
total_ms_listened = stats.get_total_listening()
stats_model.update_total_ms_listened(total_ms_listened)

# update total minutes listened to last year
total_ms_listened_last_year = stats.get_total_listening(start_date, end_date)
stats_model.update_total_ms_listened_last_year(total_ms_listened_last_year)

# # update average minutes listened to
average_ms_listened = stats.get_average_listening(start_date, end_date)
stats_model.update_average_ms_listened(average_ms_listened)

# update top 5 songs listened to
top_5_songs_recent_raw = stats.get_top_tracks(token)
top_5_songs_recent = simplify_top_songs(top_5_songs_recent_raw)
stats_model.update_top_5_songs_recent(top_5_songs_recent)

# update top 5 artists listened to
top_5_artists_recent_raw = stats.get_top_artists(token)
top_5_artists_recent = simplify_top_artists(top_5_artists_recent_raw)
stats_model.update_top_5_artists_recent(top_5_artists_recent)

# # update month over month listening stats
month_over_month_listening_stats = stats.get_total_listening_by_month(year)
stats_model.update_mom_ly_ms_listened(month_over_month_listening_stats)

# # update listening clock for the year
listening_clock = stats.get_hour_listened(start_date, end_date)
stats_model.update_listening_clock_ly(listening_clock)
