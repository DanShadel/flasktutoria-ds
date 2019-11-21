import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'test'
	SPOTIPY_CLIENT_ID=os.environ.get('SPOTIPY_CLIENT_ID')
	SPOTIPY_CLIENT_SECRET=os.environ.get('SPOTIPY_CLIENT_SECRET')
