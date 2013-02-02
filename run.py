# coding=utf-8
#!/usr/bin/env python3
"""
Dependencies: python3, pylast, requests
"""

if __name__ == "__main__":
    import argparse
    import configparser

    from core.app import App
    from lastfm import LastFmLovedTracks, LastFmLibraryTracks
    from exfm import ExFmTrack

    config = configparser.ConfigParser()
    config.read('config.ini')


    app = App()
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", dest = "source", default = "loved", help="Last.fm track source")
    parser.add_argument("-l", "--limit", dest = "limit", default = None, help="Number of tracks to process")
    args = parser.parse_args()

    source = args.source
    limit = args.limit
    if source == "loved":
        app.collection_importer = LastFmLovedTracks
    elif source == "library":
        app.collection_importer = LastFmLibraryTracks
    else:
        print("Set --source=loved|library")
        raise Exception("Invalid argument: source. Should be loved|library")

    app.collection_importer_params = {
        'api_key': config['lastfm']['api_key'],
        'api_secret': config['lastfm']['api_secret'],
        'username': config['lastfm']['username'],
        'options': {
            'limit': None
        }
    }

    if limit is not None:
        try:
            app.collection_importer_params['options']['limit'] = int(limit)
        except Exception as e:
            print("invalid limit:", e)

    app.track_exporter = ExFmTrack
    app.track_exporter_params = {
        'username': config['exfm']['username'],
        'password': config['exfm']['password'],
    }

    app.run()