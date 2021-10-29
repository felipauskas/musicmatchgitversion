import requests

class SpotifyAPI:
    def __init__(self):
        spotify_end_point = 'https://accounts.spotify.com/api/token'
        # refresh_token = Token
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': f'{refresh_token}',
        }
        response = requests.post(url=spotify_end_point, auth=("""Token"""), data=payload)
        data = response.json()
        refreshed_access = data['access_token']
        self.token = f'{refreshed_access}'
        self.headers = {'Authorization':f'Bearer {self.token}'}

    def search_music(self, music):
        """ It requires one argument = music. It's searches for a music within Spotify API and returns a nested dict
        containing id = {artist:music)"""
        search_endpoint = 'https://api.spotify.com/v1/search'
        params = {
            'query':f'{music}',
            'type':'track',
            'limit': '3',
        }
        response = requests.get(url=search_endpoint, params=params, headers=self.headers)
        data = response.json()
        tracks = {}
        variable = 1
        for i in data['tracks']['items']:
            tracks[variable] = {'id': i['id'], 'track': f'{i["name"]} - {i["artists"][0]["name"]}', 'artist': i["artists"][0]["name"], 'song': i["name"],
                                'artistid': i["artists"][0]['id']}
            variable = variable + 1
        return tracks

    def get_music_details(self, id):
        def get_audio_features():
            search_endpoint = f'https://api.spotify.com/v1/audio-features/{id}'
            response = requests.get(url=search_endpoint, headers=self.headers)
            data = response.json()
            track_details = {'danceability':data['danceability'], 'energy':data['energy'],
                             'acousticness':data['acousticness'], 'valence':data['valence']}
            return track_details

        def get_music():
            search_endpoint = f'https://api.spotify.com/v1/tracks/{id}'
            response = requests.get(url=search_endpoint, headers=self.headers)
            data = response.json()
            image = data['album']['images'][0]['url']
            return image
        return get_audio_features, get_music

    def get_genre(self, id):
        # ID refer to the Artist ID
        search_endpoint = f'https://api.spotify.com/v1/artists/{id}'
        response = requests.get(url=search_endpoint, headers=self.headers)
        data = response.json()
        genre = data['genres']
        genre = [i.split()[0] for i in genre]
        return genre
