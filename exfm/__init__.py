# coding=utf-8
"""
Ex.fm wrappers
"""

import requests
import json

from core import Track

class ExFmClient():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def search_by_title(self, title):
        try:
            search_url = "http://ex.fm/api/v3/song/search/{term}"
            response = requests.get(search_url.format(
                term=title
            ))
            decoded = json.loads(response.text)
            return decoded['songs']
        except Exception as e:
            print("error: ", e)
            return []

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
                    print("love!")
        except Exception as e:
            print("error: ", e)

class ExFmTrack(Track, ExFmClient):
    def __init__(self, track, **kwargs):
        super(ExFmTrack, self).__init__(**kwargs)
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
        songs = self.search_by_title(title=repr(self))
        if songs:
            self.id = songs[0]['id']
            print("search: ", self, ". found id: ", self.id)
        return self

    def add(self):
        """
        Add a track to "loved" on ex.fm
        """
        self.add_to_loved_tracks(id=self.id)
        return self
