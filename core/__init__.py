# coding=utf-8
"""
Core classes.
"""

from collections import Iterator

class Tracks(Iterator):
    """
    Abstract track collection.
    """
    def __next__(self):
        raise NotImplementedError

class Track():
    """
    Abstract track interface
    """
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def search(self):
        raise NotImplementedError

    def add(self):
        raise NotImplementedError
