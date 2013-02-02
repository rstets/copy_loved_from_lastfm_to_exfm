# coding=utf-8
"""
Ex.fm wrappers
"""

import requests
import json

from core import Track, Tracks

class ExFmClient():
    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password

    def search_by_title(self, title):
        (t, a) = title.split(" - ")
        track = Track(title=t, artist=a)
        print("search: ", track)
        return self.search_by_track(track)

    def search_by_track(self, track):
        print("searching: " + repr(track))
        try:
            search_url = "http://ex.fm/api/v3/song/search/{term}"
            response = requests.get(search_url.format(
                term=track.title
            ))
            decoded = json.loads(response.text)
            songs = decoded['songs']
            if songs:
                for song in songs:
                    if song['artist'] == track.artist:
                        return song['id']
            else:
                print("not found!")
        except Exception as e:
            print("error: ", e)

    def add_to_loved_tracks(self, id):
        try:
            if id:
                love_url = "http://ex.fm/api/v3/song/{id}/love"
                response = requests.post(love_url.format(id=id), data={
                    'username': self.username,
                    'password': self.password
                })
                decoded = json.loads(response.text)
                if decoded['status_code'] != 200:
                    print("code: ", decoded['status_code'], "text: ", decoded['status_text'])
                else:
                    print("added: " + id)
        except Exception as e:
            print("error: ", e)

class ExFmTracks(Tracks, ExFmClient):
    """
    GrooveShark track collection.
    """
    def __init__(self, **kwargs):
        Tracks.__init__(self, **kwargs)
        ExFmClient.__init__(self, **kwargs)

    def create_track(self, **kwargs):
        return ExFmTrack(**kwargs)

    def search(self, track):
        """
        Search for track on exfm by 'artist - title'
        """
        id = self.search_by_track(track=track)
        if id:
            track.id = id
        return track

    def add(self, track):
        """
        Add a track to "loved" on ex.fm
        """
        self.add_to_loved_tracks(id=track.id)
        return track


class ExFmTrack(Track):
    def __init__(self, **kwargs):
        Track.__init__(self, **kwargs)
        self.id = None
