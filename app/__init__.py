from flask import Flask
from config import Config
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
app.config.from_object(Config)
from app import routes


