# coding=utf-8
#!/usr/bin/env python3
"""
Dependencies: python3, pylast, requests
"""
from collections import Sequence
import pylast


class Tracks(Sequence):
    """
    Abstract track collection.
    """
    pass

class LastFmClient():
    def __init__(self, api_key, api_secret, username):
        self.network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret
        )
        self.user = pylast.User(user_name=username, network=self.network)

class LastFmTracks(Tracks, LastFmClient):
    """
    Last.fm track collection.
    """

    def __init__(self, **kwargs):
        super(LastFmTracks, self).__init__(**kwargs)
        self.collection = self.get_tracks()

    def __getitem__(self, item):
        track = self.collection[item].track
        return Track(
            title=track.title,
            artist=track.artist.name if isinstance(track.artist, pylast.Artist) else track.artist
        )

    def __len__(self):
        return len(self.collection)

    def get_tracks(self):
        """
        Abstract get track list.
        """
        raise NotImplementedError


class LastFmLovedTracks(LastFmTracks):
    def __init__(self, **kwargs):
        super(LastFmLovedTracks, self).__init__(**kwargs)


    def get_tracks(self):
        """
        Retrieve all loved tracks.
        """
        return self.user.get_loved_tracks(limit=None)

class Track():
    """
    Abstract track interface
    """
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

class ExFmTrack():
    def __init__(self, track):
        self.track = track
        self.id = None

    def __repr__(self):
        return "{artist} - {title}".format(
            artist=self.track.artist,
            title=self.track.title)

    def search(self):
        import requests
        search_url = "http://ex.fm/api/v3/song/search/{term}"
        response = requests.get(search_url.format(
            term=repr(self)
        ))
        import json
        decoded = json.loads(response.text)
        songs = decoded['songs']
        if songs:
            self.id = songs[0]['id']
            print("search: ", self, ". found id: ", self.id)
        return self

    def love(self):
        if self.id:
            love_url = "http://ex.fm/api/v3/song/{id}/love"
            import requests
            response = requests.post(love_url.format(id=self.id), data={
                'username': App.config['exfm']['username'],
                'password': App.config['exfm']['password']
            })
            import json
            decoded = json.loads(response.text)
            if decoded['status_code'] != 200:
                print("code: ", decoded['status_code'], "text: ", decoded['status_text'])
        return self


class App():
    config = None

    @classmethod
    def load_config(cls):
        import configparser
        cls.config = configparser.ConfigParser()
        cls.config.read('config.ini')

    @classmethod
    def run(cls):
        cls.load_config()
        [ExFmTrack(track).search().love() for track in App.collect_tracks()]

    @classmethod
    def collect_tracks(cls):
        params = {
            'api_key': cls.config['lastfm']['api_key'],
            'api_secret': cls.config['lastfm']['api_secret'],
            'username': cls.config['lastfm']['username']
        }
        collection = cls._collection_factory(LastFmLovedTracks, params)
        return [track for track in collection]

    @classmethod
    def _collection_factory(cls, collection_class, params):
        return collection_class(**params)

if __name__ == "__main__":
    App.run()