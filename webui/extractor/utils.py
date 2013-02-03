import configparser
import os
import sys
from django.conf import settings

sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, '../'))

from core.app import App
from lastfm import LastFmLovedTracks, LastFmLibraryTracks
from exfm import ExFmTracks
from .forms import LastFMSourceForm

config = configparser.ConfigParser()
config.read(os.path.join(settings.PROJECT_ROOT, '../config.ini'))


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
        app = App()
        app.collection_importer = LastFmLibraryTracks
        app.collection_importer_params = {
            'api_key':    config['lastfm']['api_key'],
            'api_secret': config['lastfm']['api_secret'],
            'username':   self.data['username'],
            'limit':      int(self.data['limit']) or None
        }
        return list(app.collection())

class ExFMExporter():
    name='exfm'

    def __init__(self, data):
        self.data = data

        app = App()
        app.collection_exporter = ExFmTracks
        app.collection_exporter_params = {
            'username': config['exfm']['username'],
            'password': config['exfm']['password'],
            'limit': None
        }
        self.exporter = app.collection_exporter(**app.collection_exporter_params)

    def search(self):
        song = self.data['song']
        return self.exporter.search_by_title(title=song)

    def export(self):
        id = self.data['id']
        return self.exporter.add_to_loved_tracks(id=id)


_importers = {
    'lastfm': LastFMImporter
}

def get_importer(importer_name, default=False):
    if default:
        if importer_name is None:
            importer_name = 'lastfm'
    return _importers[importer_name]

_exporters = {
    'exfm': ExFMExporter
}

def get_exporter(exporter_name, default=False):
    if default:
        if exporter_name is None:
            exporter_name = 'exfm'
    return _exporters[exporter_name]


