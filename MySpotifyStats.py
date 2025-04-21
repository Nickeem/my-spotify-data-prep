import requests
import os
import pytz
import pandas as pd

class MySpotifyStats:
    client_id = None # Spotify API client ID
    client_secret = None # Spotify API client secret


    def __init__(self):
        self.setup()
        pass

    def setup(self):
        # This function retrieves the Spotify API credentials from environment variables.
        # Make sure to set these environment variables in your system or IDE.
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.streaming_history_path = os.getenv('SPOTIFY_STREAMING_HISTORY_PATH')

        if not self.client_id or not self.client_secret:
            raise Exception("Please set the SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")


        # get all files in directory like Streaming_History_Auddio in name
        streaming_history_files = [f for f in os.listdir(self.streaming_history_path) if 'Streaming_History_Audio' in f]
        
        # streaming history files list
        self.streaming_history_files = [os.path.join(self.streaming_history_path, f) for f in streaming_history_files]

        # stremaing history df
        self.streaming_history_df = pd.concat([pd.read_json(f) for f in self.streaming_history_files], ignore_index=True)

        # Convert the 'ts' column to datetime and add 'ts_bb' column
        self.streaming_history_df['ts'] = pd.to_datetime(self.streaming_history_df['ts'])
        barbados_tz = pytz.timezone('America/Barbados')
        self.streaming_history_df['ts_bb'] = self.streaming_history_df['ts'].dt.tz_convert(barbados_tz)
        self.streaming_history_df['ts_day_bb'] = self.streaming_history_df['ts_bb'].dt.date 

    def generate_spotify_api_token(self):
        # This function generates a Spotify API token using the client credentials flow.
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            raise Exception("Failed to generate Spotify API token. Check your credentials.")


    def get_top_item(self, token, content_type, time_range='short_term', limit=5):
        # This function retrieves the user's top tracks from Spotify.
        url = f"https://api.spotify.com/v1/me/top/{content_type}?time_range={time_range}&limit={limit}"
        headers = {
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("items")
        else:
            raise Exception("Failed to retrieve top tracks. Check your token and permissions.")
        
    def get_top_tracks(self, token, time_range='short_term', limit=5):
        # This function retrieves the user's top tracks from Spotify.
        return self.get_top_item(token, 'tracks', time_range, limit)
    
    def get_top_artists(self, token, time_range='short_term', limit=5):
        # This function retrieves the user's top artists from Spotify.
        return self.get_top_item(token, 'artists', time_range, limit)

    
    def spotify_artist_search(self, token, artist_name):
        '''
        This function searches for an artist on Spotify by name.
        It returns the first artist object found.
        
        Parameters:
        token (str): The Spotify API token.
        artist_name (str): The name of the artist to search for.
        
        Returns:
        dict: The first artist object found in the search results. Object contains the artist's name, id, images genres, uri etc. Reference https://developer.spotify.com/documentation/web-api/reference/search
        
        
        '''

        # This function searches for an artist on Spotify by name.
        url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
        headers = {
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            artist_obj = response.json().get("artists", {}).get("items", [])
        else:
            raise Exception("Failed to search for artist. Check your token and permissions.")
        
        return artist_obj[0] if artist_obj else None

        

    def get_total_listening(self, range_start=None, range_end=None):
        # Work on a copy of the DataFrame to avoid modifying the original
        df_copy = self.streaming_history_df.copy()

        if range_start is not None and range_end is not None:
            # Filter the DataFrame for the specified date range
            mask = (df_copy['ts_day_bb'] >= range_start) & (df_copy['ts_day_bb'] <= range_end)
            df_copy = df_copy.loc[mask]

        total_listening_ms = df_copy['ms_played'].sum()
        return total_listening_ms
    
    def get_total_listening_by_month(self, year=None):
        # Work on a copy of the DataFrame to avoid modifying the original
        df_copy = self.streaming_history_df.copy()

        if year is not None:
            # Filter the DataFrame for the specified yea
            df_copy = df_copy[df_copy['ts_bb'].dt.year == year]

        # Create column for end of month of date
        df_copy['end_of_month'] = df_copy['ts_bb'] + pd.offsets.MonthEnd(0)

        # Group by end of month and sum the ms_played column
        listening_month_df = df_copy.groupby(['end_of_month'])['ms_played'].sum().reset_index()
        return listening_month_df

    def get_average_listening(self, range_start, range_end):
        # Work on a copy of the DataFrame to avoid modifying the original
        df_copy = self.streaming_history_df.copy()

        if range_start is not None and range_end is not None:
            # Filter the DataFrame for the specified date range
            mask = (df_copy['ts_day_bb'] >= range_start) & (df_copy['ts_day_bb'] <= range_end)
            df_copy = df_copy.loc[mask]

        total_listening_ms = df_copy['ms_played'].sum()
        total_days = (df_copy['ts_day_bb'].max() - df_copy['ts_day_bb'].min()).days + 1
        average_listening_ms = total_listening_ms / total_days if total_days > 0 else 0
        return average_listening_ms

    def get_hour_listened(self, range_start=None, range_end=None):
        # Work on a copy of the DataFrame to avoid modifying the original
        df_copy = self.streaming_history_df.copy()

        if range_start is not None and range_end is not None:
            # Filter the DataFrame for the specified date range
            mask = (df_copy['ts_day_bb'] >= range_start) & (df_copy['ts_day_bb'] <= range_end)
            df_copy = df_copy.loc[mask]

        # Create a new column for the hour of the day
        df_copy['hour'] = df_copy['ts_bb'].dt.hour

        # Group by hour and sum the ms_played column
        listening_hour_df = df_copy.groupby(['hour'])['ms_played'].sum().reset_index()
        return listening_hour_df
    

    def get_artist_listening_time(self, artist_name, range_start=None, range_end=None):
        '''
        This function retrieves the total listening time for a specific artist within a specified date range.
        
        Parameters:
        artist_name (str): The name of the artist to search for.
        range_start (datetime.date): The start date of the range (inclusive).
        range_end (datetime.date): The end date of the range (inclusive).
        
        Returns:
        int: The total listening time in milliseconds for the specified artist within the date range.
        '''
        
        # Work on a copy of the DataFrame to avoid modifying the original
        df_copy = self.streaming_history_df.copy()

        if range_start is not None and range_end is not None:
            # Filter the DataFrame for the specified date range
            mask = (df_copy['ts_day_bb'] >= range_start) & (df_copy['ts_day_bb'] <= range_end)
            df_copy = df_copy.loc[mask]

        # Filter the DataFrame for the specified artist
        mask = df_copy['master_metadata_album_artist_name'].str.match(artist_name, case=False, na=False)
        df_artist = df_copy.loc[mask]

        # Calculate total listening time in minutes
        total_listening_ms = df_artist['ms_played'].sum()
        
        return total_listening_ms


