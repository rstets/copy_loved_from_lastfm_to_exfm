# coding=utf-8

class App():
    def __init__(self):
        self.collection_importer = None
        self.collection_importer_params = None
        self.collection_exporter = None
        self.collection_exporter_params = None

    def run(self):
        exporter = self.collection_exporter(**self.collection_exporter_params)
        for track in self.collection():
            track_params = {'title': track.title, 'artist': track.artist}
            track = exporter.create_track(**track_params)
            exporter.search(track)
            exporter.add(track)

    def collection(self):
        return self.collection_importer(**self.collection_importer_params)

    def _track_factory(self, track_exporter, **params):
        return track_exporter(**params)
