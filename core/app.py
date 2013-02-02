# coding=utf-8
class App():
    def __init__(self):
        self.collection_importer = None
        self.collection_importer_params = None
        self.track_exporter = None
        self.track_exporter_params = None

    def run(self):
        [self._track_factory(self.track_exporter, track, self.track_exporter_params).search().add() for track in self.collection()]

    def collection(self):
        return self._collection_factory(self.collection_importer, self.collection_importer_params)

    def _collection_factory(self, collection_class, params):
        return collection_class(**params)

    def _track_factory(self, track_exporter, track, params):
        pass
