# coding=utf-8
#!/usr/bin/env python3
"""
Dependencies: python3, requests
"""

if __name__ == "__main__":
    import argparse
    import configparser

    from core.app import App
    from lastfm import LastFmLovedTracks, LastFmLibraryTracks
    from exfm import ExFmTracks
    # from grooveshark import GrooveSharkTracks

    config = configparser.ConfigParser()
    config.read('config.ini')


    app = App()
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source", dest = "source", default = "loved", help="Last.fm track source")
    # parser.add_argument("-d", "--dest", dest = "dest", default = "exfm", help="Track destination: exfm. Default exfm")
    parser.add_argument("-l", "--limit", dest = "limit", default = None, help="Number of tracks to process")
    parser.add_argument("-r", "--resume", dest = "resume", default = True, help="Resume import from the same page.")
    args = parser.parse_args()

    source = args.source
    # dest = args.dest
    limit = args.limit
    resume = args.resume
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
        'limit': int(limit or 0) or None,
        'resume': resume
    }

    # if dest == "grooveshark":
    #     app.collection_exporter = GrooveSharkTracks
    #     app.collection_exporter_params = {
    #         'api_key': config['grooveshark']['api_key'],
    #         'api_secret': config['grooveshark']['api_secret'],
    #         'username': config['grooveshark']['username'],
    #         'password': config['grooveshark']['password'],
    #         'limit': None
    #     }
    # else:
    app.collection_exporter = ExFmTracks
    app.collection_exporter_params = {
        'username': config['exfm']['username'],
        'password': config['exfm']['password'],
        'limit': None
    }

    app.run()