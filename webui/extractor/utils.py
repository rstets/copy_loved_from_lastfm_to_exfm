from .forms import LastFMSourceForm


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
        return []


_importers = {
    'lastfm': LastFMImporter
}

def get_importer(importer_name, default=False):
    if default:
        if importer_name is None:
            importer_name = 'lastfm'
    return _importers[importer_name]