import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'test'
	SPOTIPY_CLIENT_ID=os.environ.get('SPOTIPY_CLIENT_ID') or 'a8c591798f314db6a80acaaa3a2460d8'
	SPOTIPY_CLIENT_SECRET=os.environ.get('SPOTIPY_CLIENT_SECRET') or '1a7cb23b790744b38018cd581bbe16a0'
