import math
from iso_language_codes import *

from spotify import SpotifyAPI
from musixmatch import MusixMatchAPI
from langdetect import detect

spotify = SpotifyAPI()
lyrics = MusixMatchAPI()

def get_music(music_input):
    music1 = spotify.search_music(music_input)
    id1 = music1[1]['id']
    artist1 = music1[1]['artist']
    song1 = music1[1]['song']
    audio_features1, image1 = spotify.get_music_details(id1)
    try:
        song_lyrics1 = lyrics.get_lyric(lyrics.search_lyric(song1, artist1))
    except:
        song_language_iso = 'na'
    else:
        song_language_iso = detect(song_lyrics1)
    song_language1 = language(song_language_iso)
    genre = spotify.get_genre(music1[1]['artistid'])
    return artist1, song1, audio_features1(), image1(), song_language1['Name'], genre

def get_difference(a, b):
    difference = abs(a-b)
    formula = (1 - difference) * 100
    return formula

def return_final_score(music1, music2):
    """"This function is where I'm calculating the final score of the music comparison."""
    first_track = music1[2]
    second_track = music2[2]
    language1 = music1[4]
    language2 = music2[4]
    artist1 = music1[0]
    artist2 = music2[0]
    first_attributes = [x for x in first_track.values()]
    second_attributes = [x for x in second_track.values()]
    genre1 = music1[5]
    genre2 = music2[5]
    newlist = []
    if music1 == music2:
        newlist.append(100)
    else:
        for i in range(0,4):
            newvalue = get_difference(first_attributes[i], second_attributes[i])
            newlist.append(newvalue)
        if language1 == language2:
            newlist.append(100)
        else:
            newlist.append(30)
        if artist1 == artist2:
            newlist.append(150)
        else:
            newlist.append(50)
        if any(x in genre1 for x in genre2):
            newlist.append(100)
        else:
            newlist.append(-60)
    if math.ceil(sum(newlist) / len(newlist)) > 100:
        final = 96
    else:
        final = math.ceil(sum(newlist) / len(newlist))
    return final, newlist

attributes = {
    'danceability': 'Danceability describes how suitable a track is for dancing based on'
                    'a combination of musical elements including tempo, rhythm stability, beat strength,'
                    'and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable',
    'energy': 'Energy represents a perceptual measure of intensity and activity. '
              'Typically, energetic tracks feel fast, loud, and noisy',
    'acousticness': 'Acousticness describes how acoustic a song is. '
                    'A score of 1.0 means the song is most likely to be an acoustic one.',
    'valence': '“A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. '
               'Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric),'
               'while tracks with low valence sound more negative (e.g. sad, depressed, angry)”.'
}
