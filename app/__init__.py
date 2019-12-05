from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# replace requirements.txt mpld3= WITH

#-e git+https://github.com/javadba/mpld3@display_fix#egg=mpld3
app.config.from_object(Config)
from app import routes

bootstrap = Bootstrap(app)
