from .forms import LastFMSourceForm

class LastFMImporter(object):
    name='lastfm'
    Form=LastFMSourceForm

    def __init__(self, data):
        self.data = data


_importers = {
    'lastfm': LastFMImporter
}

def get_importer(importer_name, default=False):
    if default:
        if importer_name is None:
            importer_name = 'lastfm'
    return _importers[importer_name]