from pocketbase import PocketBase

class SpotifyStatsModel:
    def __init__(self, address ):
        
        self.collection_name = "spotify_stats"
        self.address = address
        self.pb = PocketBase(address)

        # authenticate with the PocketBase server
        user_data = self.pb.collection(self.collection_name).auth_with_password(
            email="test@email.com",
            password="password")
        
        if not user_data.is_valid:
            raise Exception("Failed to authenticate with PocketBase server. Check your credentials.")
        
        self.user_data = user_data


    def update_total_minutes(self, total_minutes):
        '''
        This function updates the total minutes listened to in the PocketBase database.
        
        Parameters:
        total_minutes (int): The total minutes listened to.
        
        Returns:
        None
        '''
        
        # Update the total minutes listened to in the PocketBase database
        self.pb.collection(self.collection_name).update(
            self.user_data.record.id,
            {
                "total_minutes": total_minutes
            }
        )
