from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import URLForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import numpy as np
import mpld3
from collections import defaultdict
import sys
import math

@app.route('/', methods=['GET', 'POST'])
@app.route('/url/',  methods=['GET', 'POST'])

def url():
	form = URLForm()
	if form.validate_on_submit():
		return redirect(url_for('processing', input_url=form.input_url.data))
	return render_template('URL.html', title='Spotify 2019', form=form)


@app.route('/processing/<path:input_url>')
def processing(input_url):
	
	try:
		# Time for Chef Dan's Grade A Python Spaghetti (CDGAPS)
		client_credentials_manager = SpotifyClientCredentials(app.config["SPOTIPY_CLIENT_ID"], app.config["SPOTIPY_CLIENT_SECRET"])
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #Configure request thing

		if str(input_url).split('/')[3] == 'user':
			playlist_id = str(input_url).split('/')[6]
		else:
			playlist_id = str(input_url).split('/')[4]

		

		username='spotify'

		results = sp.user_playlist(username, playlist_id) #GET THEM TRACKS BOI
		tracks = results['tracks']
		title = results['name']

		# init a bunch of arrays
		id_list = []
		songlist = []
		i=1
		artist_id_list = []
		index = 0
		artwork = []
		row = []
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
				'image': track['track']['album']['images'][2]['url']
			}
			songlist.append(song)
			row.append(track['track']['album']['images'][2]['url'])
			
			if i % 10 is 0 and i is not 0:
				artwork.append(row)
				row = []

			i += 1

		# endfor
		artwork.append(row)
		deets = []
		genres = {}
		count = {}

		#get audio details
		while index < len(id_list):

			temp = sp.audio_features(id_list[index:index+50])
			for item in temp:
				if item is not None:
				    deets.append(item)


			temp = sp.artists(artist_id_list[index:index+50])
			for item in temp['artists']:
				if item['name'] not in genres:
					genres[item['name']] = item['genres']
					count[item['name']] = 1
				else:
					count [item['name']] += 1


			index += 50		    


		#Add bpm and song length to song object
		for i, item in enumerate(songlist):
			item['bpm'] = round(deets[i]['tempo'])
			#convert ms to m:ss
			length = deets[i]['duration_ms']
			seconds = round(length/1000)
			minutes = int(seconds/60)
			seconds -= (minutes*60)
			if seconds < 10:
				seconds = "0" + str(seconds)

			item['length'] = str(minutes) + ":" + str(seconds)






		#Generate graphs
		x = []
		y = []
		plots = []
		fig, ax = plt.subplots()
		labels= []
		#ranking vs BPM
		for song in songlist:
		    x.append(song['bpm'])
		    y.append(song['rank'])
		    temp = ""
		    for person in song['artists']:
		    	temp += person + " "

		    labels.append(song['title'] + " - " + temp + ", Rank:" + str(song['rank']) + ", BPM:" + str(song['bpm']) )

		#Plot[0] settings
		scatter = ax.scatter(x,y)
		plt.title(title)
		plt.ylabel('Ranking')
		plt.xlabel('Beats per minute')
		plt.xlim(60, 240)
		plt.ylim(len(y) + 1, -1)
		ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
		#plots[0] == ranking vs bpm
		tooltip = mpld3.plugins.PointLabelTooltip(scatter,labels=labels)
		mpld3.plugins.connect(fig,tooltip)
		plots.append(mpld3.fig_to_html(fig))
		
		# Artists bar Chart
		# more variables that I may or may not need
		num = []
		artist = []
		total = 0
		fig, ax = plt.subplots()
		maxcount = 0

		for item in count:
			if count[item] > 1:
				artist.append(item)
				num.append(count[item])
				total += count[item]
				if count[item] > maxcount:
					maxcount = count[item]

			else:
				total += 1

		ticks = []
		for i in range(1,maxcount+1):
			ticks.append(i)

		bar = plt.bar(artist,num,alpha = .75)
		plt.xticks(artist, artist)
		plt.ylabel('Appearances')
		plt.yticks(ticks)
		plt.title('Artist count')
		plots.append(mpld3.fig_to_html(fig))


		#genre percentages
		genrecounter = defaultdict(int)

		for person in count:
			for item in genres[person]:
				genrecounter[item] += count[person]*1

		genrelist = []
		genrecounts = []
		other = 0
		explode = []
		for item in genrecounter:
			if genrecounter[item] > 1:
				genrelist.append(item)
				genrecounts.append(genrecounter[item])
				explode.append(.01)

			else:
				other += 1

		explode.append(.01)
		genrelist.append('other')
		genrecounts.append(other)

		fig, ax = plt.subplots()
		pie = ax.pie(genrecounts, labels=genrelist, autopct='%1.1f%%', explode= explode, startangle=120)
		ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		plt.title('Genre percentages')
		plt.tight_layout()
		plots.append(mpld3.fig_to_html(fig))







		return	render_template('processing.html', songlist=songlist, genres=genres, count=count,plots=plots,id = playlist_id, artwork = artwork)

	except:
		return redirect(url_for('error', playlist_id = playlist_id))

@app.route('/instructions')
def instructions():

	return render_template('instructions.html', title='Spotify 2019',)


@app.route('/error')
def error():

	return render_template('error.html')