from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import URIForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt

@app.route('/')
@app.route('/index')

def index():
	user = {'username': 'Dan'}
	return render_template('index.html', title='Home', user=user)

@app.route('/uri/',  methods=['GET', 'POST'])

def uri():
	form = URIForm()
	if form.validate_on_submit():
		return redirect(url_for('processing', uri=form.uri.data))
	return render_template('URI.html', title='Spotify 2019', form=form)


@app.route('/processing/<uri>')
def processing(uri):
	
	# Time for Chef Dan's Grade A Python Spaghetti (CDGAPS)
	client_credentials_manager = SpotifyClientCredentials(app.config["SPOTIPY_CLIENT_ID"], app.config["SPOTIPY_CLIENT_SECRET"])
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #Configure request thing

	playlist_id = str(uri).split(':')[2]#isolate playlist identifier
	username='spotify'

	results = sp.user_playlist(username, playlist_id) #GET THEM TRACKS BOI
	tracks = results['tracks']

	# init a bunch of arrays
	id_list = []
	songlist = []
	i=1
	artist_id_list = []
	index = 0

	for track in tracks['items']: #Generating a comprehensive list of tracks

		track_id = track['track']['id'] # get track id
		id_list.append(track_id) # add to list of ids
		temp = [] # list of artists who worked on a song

		for artist in track['track']['artists']:
		    temp.append(artist['name'])
		    artist_id_list.append(artist['id']) #add to list of artists

		song = {
			'rank': i,
			'artists': temp,
			'title': track['track']['name'],
		}
		songlist.append(song)
		i += 1

	deets = []
	genres = {}

	while index < len(id_list):

		temp = sp.audio_features(id_list[index:index+50])
		for item in temp:
			if item is not None:
			    deets.append(item)


		temp = sp.artists(artist_id_list[index:index+50])
		for item in temp['artists']:
		    if item['name'] not in genres:
		        genres[item['name']] = item['genres']

		index += 50		    


	for i, item in enumerate(songlist):
		item['bpm'] = deets[i]['tempo']
		item['length'] = deets[i]['duration_ms']


	return	render_template('processing.html', songlist=songlist, genres=genres)



@app.route('/data')
def data():

	return render_template('data.html', title='Spotify 2019',)

