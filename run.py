# coding=utf-8
#!/usr/bin/env python3
"""
Dependencies: python3, pylast, requests
"""
from collections import Iterable, Iterator
import pylast


class Tracks(Iterator):
    """
    Abstract track collection.
    """
    def __next__(self):
        raise NotImplementedError

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

    def __init__(self, options, **kwargs):
        super(LastFmTracks, self).__init__(**kwargs)
        self.collection = self.get_tracks(options)

    def __next__(self):
        raise NotImplementedError

    def get_tracks(self, options):
        """
        Abstract get track list.
        """
        raise NotImplementedError

    def _get_track(self):
        track = next(self)
        return Track(
            title=track.title,
            artist=track.artist.name if isinstance(track.artist, pylast.Artist) else track.artist
        )


class LastFmLovedTracks(LastFmTracks):
    def __init__(self, **kwargs):
        super(LastFmLovedTracks, self).__init__(**kwargs)

    def __next__(self):
        return next(self.collection).track

    def get_tracks(self, options):
        """
        Retrieve all loved tracks.
        """
        print("limit:", options['limit'])
        return self.user.get_loved_tracks(limit=options['limit'])

class LastFmLibraryTracks(LastFmTracks):
    def __init__(self, **kwargs):
        super(LastFmLibraryTracks, self).__init__(**kwargs)

    def __next__(self):
        return next(self.collection).item

    def get_tracks(self, options):
        """
        Retrieve all loved tracks.
        """
        print("limit:", options['limit'])
        return self.user.get_library().get_tracks(limit=options['limit'])

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
        """
        Search for track on exfm by 'artist - title'
        """
        # TODO: Make some kind of API client for exfm maybe?
        try:
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
        except Exception as e:
            print("error: ", e)
        return self

    def love(self):
        """
        Add a track to "loved" on ex.fm
        """
        try:
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
                else:
                    print("love!")
        except Exception as e:
            print("error: ", e)
        return self


class App():
    config = None

    @classmethod
    def load_config(cls):
        import configparser
        cls.config = configparser.ConfigParser()
        cls.config.read('config.ini')

    @classmethod
    def run(cls, args):
        cls.load_config()
        collection = App.collect_tracks(source=args.source, limit=args.limit)
        [ExFmTrack(track).search().love() for track in collection]

    @classmethod
    def collect_tracks(cls, source, limit=None):
        params = {
            'api_key': cls.config['lastfm']['api_key'],
            'api_secret': cls.config['lastfm']['api_secret'],
            'username': cls.config['lastfm']['username'],
            'options': {
                'limit': None
            }
        }

        if limit is not None:
            try:
                params['options']['limit'] = int(limit)
            except Exception as e:
                print("cast error:", e)

        if source == "loved":
            collection = cls._collection_factory(LastFmLovedTracks, params)
        elif source == "library":
            collection = cls._collection_factory(LastFmLibraryTracks, params)
        else:
            print("Set --source=loved|library")
            return []

        return collection

    @classmethod
    def _collection_factory(cls, collection_class, params):
        return collection_class(**params)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", dest = "source", default = "loved", help="Last.fm track source")
    parser.add_argument("-l", "--limit", dest = "limit", default = None, help="Number of tracks to process")
    args = parser.parse_args()

    App.run(args)