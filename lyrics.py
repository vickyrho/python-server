from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
from urllib2 import * 
import re

app  = Flask(__name__)

CORS(app)


def scratchFromAz(link):
    formatted_text = ""
    html_page = urlopen(link)
    if html_page:
        html_soup = BeautifulSoup(html_page, 'html.parser')
        name_box = html_soup.find('div', attrs={'class': 'container main-page'}).div
        name = name_box.findAll('div')[9]
    return name.text

def scratchFromMetro(link):
    html_page = urlopen(link)
    if html_page:
        html_soup = BeautifulSoup(html_page, 'html.parser')
        lyric_box = html_soup.find('div', attrs={'id': 'lyrics-body-text'})

    return lyric_box.text

def scratchFromWikia(link):
    formatted_text = ""
    html_page = urlopen(link)
    if html_page:
        html_soup = BeautifulSoup(html_page, 'html.parser')
        print(html_soup)
        lyric_box = html_soup.find('div', attrs={'class' : 'lyricbox'})
        formatted_text = re.sub(r"(\w)([A-Z])", r"\1\n\2",lyric_box.text)

    return formatted_text


def construct_response(code, message, data):
    return {'code' : code, 'message': message, 'data': data}

@app.route('/fetch', methods=['POST'])
def hello_world():
        try:
            request_data = request.json['data']
            if request_data['link'] and request_data['domain']:
                link = request_data['link']
                domain = request_data['domain']
                if domain == 'www.lyrics.wikia.com':
                    lyrics = scratchFromWikia(link)
                    return jsonify(construct_response(200,'OK', lyrics))
                elif domain == 'www.metrolyrics.com':
                    lyrics = scratchFromMetro(link)
                    return jsonify(construct_response(200, 'OK', lyrics))
                elif domain == 'www.azlyrics.com':
                    lyrics = scratchFromAz(link)
                    return jsonify(construct_response(200, 'OK', lyrics))

        except Exception as e:
            return jsonify(construct_response(500, str(e), 0)), 500



