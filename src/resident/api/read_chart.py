""" Implement the cmd1 command.

"""
from ..core import logger
from bs4 import BeautifulSoup
import requests

CHART_URL = "https://www.residentadvisor.net/dj/{artist_id}/top10?chart={chart_id}"
ARTIST_CHARTS_URL = "https://www.residentadvisor.net/dj/{artist_id}/top10"

class Label():
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name or ''

class Artist():
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __str__(self):
        return self.name or ''

class Track():
    def __init__(self, cover, artist, title, label, label_release, url):
        self.cover = cover
        self.artist = artist
        self.title = title
        self.label = label
        self.label_release = label_release
        self.url = url

    def __str__(self):
        return self.title or ''

class Chart():
    def __init__(self, artist, date, url):
        self.artist = artist
        self.date = date
        self.tracks = {}
        self.url = url

    def addTrack(self, index, track):
        self.tracks[index] = track

    def printAll(self):
        keys = sorted(self.tracks.keys())
        for index in keys:
            track = self.tracks[index]
            print u'{index}: {artist} - {title} [{label} {label_release}]'.format(
                index=index,
                title=track.title,
                artist=track.artist,
                label=track.label,
                label_release=track.label_release or ''
            )

def parse_chart(parsed, url):
    try:
        artist = parsed.find('div', id='sectionHead').h1.get_text()
    except Exception:
        artist = parsed.find('section', id='featureHead').h1.get_text()

    date = ''
    chart = Chart(artist, date, url)

    lines = parsed.article.find_all('li')
    index = 1

    for line in lines:
        try:    line.find('div', class_='heading').clear()
        except: pass

        cover = line.find('div', class_='cover').img['src']

        artist = line.find('div', class_='artist').get_text(' ')
        artist_url = None
        try:    artist_url = line.find('div', class_='artist').a['href']
        except: pass

        track = line.find('div', class_='track').get_text(' ')
        track_url = None
        try:    track_url = line.find('div', class_='track').a['href']
        except: pass

        label = None
        label_release = None
        label_contents = line.find('div', class_='label').find_all(string=True)
        if isinstance(label_contents, list):
            if len(label_contents) > 0: label = label_contents[0]
            if len(label_contents) > 1: label_release = label_contents[1]
        label_url = None
        try:    label_url = line.find('div', class_='label').a['href']
        except: pass

        track = Track(
            cover = cover,
            artist = Artist(artist, artist_url),
            title = track,
            url = track_url,
            label = Label(label, label_url),
            label_release=label_release
        )

        chart.addTrack(index, track)
        index += 1
    chart.printAll()
    return chart

def parse_artist_charts(parsed, artist_id, url):
    try:
        artist = parsed.find('div', id='sectionHead').h1.get_text()
    except Exception:
        artist = parsed.find('section', id='featureHead').h1.get_text()

    drop_down = parsed.find('ul', class_='content-list').div(class_='dropdown')[0].ul
    lines = drop_down.find_all('li')

    charts = []

    print 'Charts for {artist}'.format(artist=artist)

    for line in lines:
        chart_id = line['data-id']
        date = line.string

        print '\n== {date} ({chart_id}) =='.format(date=date, chart_id=chart_id)
        chart = read_chart(artist_id, chart_id)


def read_chart(artist_id, chart_id):
    actual_url = CHART_URL.format(artist_id=artist_id, chart_id=chart_id)
    result = requests.request('GET', actual_url)

    if result.ok:
        content = result.content
        parsed = BeautifulSoup(content, 'html.parser')
        parse_chart(parsed, actual_url)

def list_charts(artist_id):
    actual_url = ARTIST_CHARTS_URL.format(artist_id=artist_id)
    result = requests.request('GET', actual_url)

    if result.ok:
        content = result.content
        parsed = BeautifulSoup(content, 'html.parser')
        parse_artist_charts(parsed, artist_id, actual_url)

def main(chart_id):
    """ Execute the command.
    
    """
    logger.debug("executing cmd1 command")
    print("Hello, {:s}!".format(chart_id))
    return
