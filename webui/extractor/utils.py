import configparser
import os
import sys
from django.conf import settings
from .forms import LastFMSourceForm

sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, '../'))

from core.app import App
from lastfm import LastFmLovedTracks, LastFmLibraryTracks

config = configparser.ConfigParser()
config.read(os.path.join(settings.PROJECT_ROOT, '../config.ini'))

app = App()


class BaseMusicImporter(object):
    def get_playlists(self):
        raise Exception('Not Implemented')

    def get_songs(self):
        raise Exception('Not Implemented')


class LastFMImporter(BaseMusicImporter):
    name='lastfm'
    Form=LastFMSourceForm

    def __init__(self, data):
        self.data = data

    def get_playlists(self):
        return [('library', 'Library'),
                ('loved', 'Loved Tracks')]

    def get_songs(self):
        app.collection_importer = LastFmLibraryTracks
        app.collection_importer_params = {
            'api_key':    config['lastfm']['api_key'],
            'api_secret': config['lastfm']['api_secret'],
            'username':   self.data['username'],
            'limit':      int(self.data['limit']) or None
        }
        return list(app.collection())


_importers = {
    'lastfm': LastFMImporter
}

def get_importer(importer_name, default=False):
    if default:
        if importer_name is None:
            importer_name = 'lastfm'
    return _importers[importer_name]