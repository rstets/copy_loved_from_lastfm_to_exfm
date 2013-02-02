# coding=utf-8
"""
Ex.fm wrappers
"""

from core import Track

class ExFmClient():
    def __init__(self, username, password):
        self.username = username
        self.password = password


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

    def add(self):
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
