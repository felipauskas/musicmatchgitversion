import requests

class MusixMatchAPI:
    def __init__(self):
        # self.token = your token
        self.headers = {'Authorization':f'Bearer {self.token}'}

    def search_lyric(self, music, artist):
        endpoint = 'http://api.musixmatch.com/ws/1.1/track.search'
        params = {
            'apikey': self.token,
            'q_track': music,
            'q_artist': artist,
        }
        response = requests.get(endpoint,params=params)
        data = response.json()
        for i in data['message']['body']['track_list']:
            if i['track']['has_lyrics'] > 0:
                return i['track']['track_id']

    def get_lyric(self, id):
        endpoint = f'http://api.musixmatch.com/ws/1.1/track.lyrics.get'
        params = {
            'apikey': self.token,
            'track_id': id,
        }
        response = requests.get(endpoint, params=params)
        data = response.json()
        return data['message']['body']['lyrics']['lyrics_body']