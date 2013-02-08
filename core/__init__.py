# coding=utf-8
"""
Core classes.
"""

from collections import Iterator

class Tracks(Iterator):
    """
    Abstract track collection.
    """
    def __init__(self, limit, **kwargs):
        self.limit = limit

    def __next__(self):
        raise NotImplementedError

class Track():
    """
    Abstract track interface
    """
    def __init__(self, title, artist, **kwargs):
        self.title = title
        self.artist = artist

    def __repr__(self):
        return "{artist} {title}".format(
            artist=self.artist,
            title=self.title)

    def search(self):
        raise NotImplementedError

    def add(self):
        raise NotImplementedError
