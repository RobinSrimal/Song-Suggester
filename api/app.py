from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def create_app():
    app = Flask(__name__)
    client_credentials_manager = SpotifyClientCredentials(client_id='69d7960353114a25ad479492dd0346eb', client_secret='6190f3b487b448d6b0d8340c01baf3ab')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    @app.route('/', methods=['GET'])
    def index():
        return 'Hi'

    @app.route('/song', methods=['GET'])
    def song_info():
        '''This route returns details about the specified song'''
        title = request.args.get('title')
        artist = request.args.get('artist')

        song = sp.search(f'{title} {artist}', type='track', limit=1)
        info = {'title': song['tracks']['items'][0]['name'],
                'artist': song['tracks']['items'][0]['artists'][0]['name'],
                'album': song['tracks']['items'][0]['album']['name']
                }
        return jsonify(info)

    @app.route('/suggestions', methods=['GET'])
    def suggest():

        title = request.args.get('title')
        artist = request.args.get('artist')

        song = sp.search(f'{title} {artist}', type='track', limit=1)
        song_id = song['tracks']['items'][0]['id']
        features = sp.audio_features([song_id])
        return features[0]
    return app