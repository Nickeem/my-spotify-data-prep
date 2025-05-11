from MySpotifyStats import MySpotifyStats
from SpotifyStatsModel import SpotifyStatsModel
import datetime as dt


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
top_5_songs_recent = stats.get_top_tracks(token)
stats_model.update_top_5_songs_recent(top_5_songs_recent)

# update top 5 artists listened to
top_5_artists_recent = stats.get_top_artists(token)
stats_model.update_top_5_artists_recent(top_5_artists_recent)

# # update month over month listening stats
month_over_month_listening_stats = stats.get_total_listening_by_month(year)
stats_model.update_mom_ly_ms_listened(month_over_month_listening_stats)

# # update listening clock for the year
listening_clock = stats.get_hour_listened(start_date, end_date)
stats_model.update_listening_clock_ly(listening_clock)
