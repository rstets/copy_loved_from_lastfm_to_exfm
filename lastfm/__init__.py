# coding=utf-8
"""
Last.fm wrappers.
"""

from lastfm import pylast
from core import Track, Tracks

class LastFmClient():
    def __init__(self, api_key, api_secret, username, resume=True, **kwargs):
        self.network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret
        )
        self.user = pylast.User(user_name=username, network=self.network)
        self.resume = resume

    def get_loved_tracks(self, **kwargs):
        return self.user.get_loved_tracks(resume=self.resume, **kwargs)

    def get_library_tracks(self, **kwargs):
        return self.user.get_library().get_tracks(resume=self.resume, **kwargs)


class LastFmTracks(Tracks, LastFmClient):
    """
    Last.fm track collection.
    """
    def __init__(self, **kwargs):
        Tracks.__init__(self, **kwargs)
        LastFmClient.__init__(self, **kwargs)
        self.collection = self.get_tracks()

    def __next__(self):
        raise NotImplementedError

    def get_tracks(self):
        """
        Abstract get track list.
        """
        raise NotImplementedError

    def _get_track(self, track):
        return Track(
            title=track.title,
            artist=track.artist.name if isinstance(track.artist, pylast.Artist) else track.artist
        )


class LastFmLovedTracks(LastFmTracks):
    def __init__(self, **kwargs):
        super(LastFmLovedTracks, self).__init__(**kwargs)

    def __next__(self):
        return self._get_track(next(self.collection).track)

    def get_tracks(self):
        """
        Retrieve all loved tracks.
        """
        print("limit:", self.limit)
        return self.get_loved_tracks(limit=self.limit)

class LastFmLibraryTracks(LastFmTracks):
    def __init__(self, **kwargs):
        super(LastFmLibraryTracks, self).__init__(**kwargs)

    def __next__(self):
        return self._get_track(next(self.collection).item)

    def get_tracks(self):
        """
        Retrieve all loved tracks.
        """
        print("limit:", self.limit)
        return self.get_library_tracks(limit=self.limit)
