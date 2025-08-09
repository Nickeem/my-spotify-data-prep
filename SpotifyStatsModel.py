from pocketbase import PocketBase
import json

class SpotifyStatsModel:
    def __init__(self, address, collection_name, admin_email, admin_password):
        
        self.collection_name = collection_name
        self.address = address
        self.pb = PocketBase(address)
 
        # authenticate with the PocketBase server
        admin_data = self.pb.admins.auth_with_password(
            email=admin_email,
            password=admin_password, )
        
        if not admin_data.is_valid:
            raise Exception("Failed to authenticate with PocketBase server. Check your credentials.")
        
        self.admin_data = admin_data

        # Temporary Poketbase field keys. 
        # IMPLEMENTATION NOTE: These should be replaced and a more dynamic solution should be in place in the future.
        self.total_ms_listened_record_id = 'k79p34vx2t81ppm'  # total_ms_listened record id
        self.total_ms_listened_ly_record_id = 'g1u3v64la2ufpyx'
        self.average_ms_listened_record_id = 'cvcl26dhoq3698a'
        self.top_5_songs_recent_record_id = 'ncdzc3y1paeayj4'
        self.top_5_artists_recent_record_id = '3726130j114pzzm'
        self.mom_ms_listened_record_id = '723y18jg6z2srvx'
        self.listening_clock_ly_record_id = '7pc06xg3ix8c847'


    def update_stats(self, record_id, label, value):
        '''
        This function updates value of a stat
        
        Parameters:
        record_id (str): The record ID of the stat to update.
        value (int): The new value to set for the stat.
        
        Returns:
        None
        '''
        
        # Update the total minutes listened to in the PocketBase database
        self.pb.collection(self.collection_name).update(

            record_id, # total_ms_listened record id
            {
                "value": json.dumps({label:value})
            }
        )
    
    def update_total_ms_listened(self, total_ms_listened: int):
        '''
        This function updates the total minutes listened to in the PocketBase database.
        
        Parameters:
        total_minutes (int): The total minutes listened to.
        
        Returns:
        None
        ''' 
        # Update the total minutes listened to in the PocketBase database
        total_ms_listened_record_id = self.total_ms_listened_record_id # total_ms_listened record id
        label = 'total_ms_listened'
        self.update_stats(total_ms_listened_record_id, label, total_ms_listened)

    
    def update_total_ms_listened_last_year(self, total_ms_listened_last_year):
        '''
        This function updates the total minutes listened to last year in the PocketBase database.
        
        Parameters:
        total_ms_listened_last_year (int): The total minutes listened to.
        
        Returns:
        None
        ''' 
        # Update the total minutes listened to in the PocketBase database
        total_ms_listened_ly_record_id = self.total_ms_listened_ly_record_id
        label = 'total_ms_listened_last_year'
        self.update_stats(total_ms_listened_ly_record_id, label, total_ms_listened_last_year)

    def update_average_ms_listened(self, average_ms_listened):
        '''
        This function updates the average minutes listened to in the PocketBase database.
        
        Parameters:
        average_ms_listened (int): The average minutes listened to.
        
        Returns:
        None
        ''' 
        # Update the total minutes listened to in the PocketBase database
        average_ms_listened_record_id = self.average_ms_listened_record_id
        label = 'average_ms_listened'
        self.update_stats(average_ms_listened_record_id, label, average_ms_listened)

    def update_top_5_songs_recent(self, top_5_songs_recent):
        '''
        This function updates the top 5 songs listened to in the PocketBase database.
        
        Parameters:
        top_5_songs_recent (list): The list of top 5 songs listened to.
        
        Returns:
        None
        ''' 
        # Update the total minutes listened to in the PocketBase database
        top_5_songs_recent_record_id = self.top_5_songs_recent_record_id
        label = 'top_5_songs_recent'
        self.update_stats(top_5_songs_recent_record_id, label, top_5_songs_recent)

    def update_top_5_artists_recent(self, top_5_artists_recent):
        '''
        This function updates the top 5 artists listened to in the PocketBase database.
        
        Parameters:
        top_5_artists_recent (list): The list of top 5 artists listened to.
        
        Returns:
        None
        ''' 
        # Update the total minutes listened to in the PocketBase database
        top_5_artists_recent_record_id = self.top_5_artists_recent_record_id
        label = 'top_5_artists_recent'
        self.update_stats(top_5_artists_recent_record_id, label, top_5_artists_recent)

    def update_mom_ly_ms_listened(self, mom_ms_listened):
        '''
        This function updates the minutes listened to in the PocketBase database.
        
        Parameters:
        mom_ms_listened (int): The minutes listened to.
        
        Returns:
        None
        ''' 
        # Update the total minutes listened to in the PocketBase database
        mom_ms_listened_record_id = self.mom_ms_listened_record_id
        label = 'mom_ly_ms_listened'
        self.update_stats(mom_ms_listened_record_id, label, mom_ms_listened)

    def update_listening_clock_ly(self, listening_clock_ly):
        '''
        This function updates the listening clock in the PocketBase database.
        
        Parameters:
        listening_clock_ly (list): The list of listening clock.
        
        Returns:
        None
        ''' 
        # Update the total minutes listened to in the PocketBase database
        listening_clock_ly_record_id = self.listening_clock_ly_record_id
        label = 'listening_clock_ly'
        self.update_stats(listening_clock_ly_record_id, label, listening_clock_ly)

    
        

    
