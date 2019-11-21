from flask import render_template, flash, redirect
from app import app
from app.forms import URIForm

@app.route('/')
@app.route('/index')

def index():
	user = {'username': 'Dan'}
	return render_template('index.html', title='Home', user=user)

@app.route('/uri/',  methods=['GET', 'POST'])

def uri():
	form = URIForm()
	if form.validate_on_submit():
		return render_template('processing.html', uri=form.uri.data)
	return render_template('URI.html', title='Spotify 2019', form=form)


@app.route('/processing')
def processing():
	return	render_template('processing.html',uri=uri)



@app.route('/data')
def data():

	return render_template('data.html', title='Spotify 2019',)