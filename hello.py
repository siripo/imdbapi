from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello():
	response = requests.get('http://www.imdb.com/title/tt0111161')
	html = response.text
	return html

