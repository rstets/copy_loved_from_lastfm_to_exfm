# coding=utf-8
"""
Grooveshark wrappers
"""

from core import Track, Tracks
from grooveshark import api


class GrooveSharkClient():
    def __init__(self, api_key, api_secret, username, password, **kwargs):
        api.KEY = api_key
        api.SECRET = api_secret
        api.init()
        api.authenticate_user(username, password)

    def find_first_by_title(self, title):
        try:
            response = api.api_call('getSongSearchResults', {
                'query': title,
                'country': 'USA',
                'limit': 1,
            })
            songID = response['result']['songs'][0]['SongID']
            print("search: ", songID)
            return songID
        except Exception as e:
            print("search error: ", e, response)
            raise e

    def add_to_library(self, id):
        try:
            response = api.api_call('addUserFavoriteSong', {
                'songID': id,
            })
            print("add: ", response)
        except Exception as e:
            print("add error:", e)


class GrooveSharkTracks(Tracks, GrooveSharkClient):
    """
    GrooveShark track collection.
    """
    def __init__(self, **kwargs):
        Tracks.__init__(self, **kwargs)
        GrooveSharkClient.__init__(self, **kwargs)

    def create_track(self, **kwargs):
        return GrooveSharkTrack(**kwargs)

    def search(self, track):
        id = self.find_first_by_title(repr(track))
        if id:
            track.id = id
        return track

    def add(self, track):
        if track.id:
            self.add_to_library(track.id)
        return track

class GrooveSharkTrack(Track):
    def __init__(self, **kwargs):
        Track.__init__(self, **kwargs)
        self.id = None
