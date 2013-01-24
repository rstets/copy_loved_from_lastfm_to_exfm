lastfm2exfm
===========

"Copy" last.fm loved tracks to ex.fm

Install dependencies:
====

* brew install python3 (for Mac OS X. for Linux must be "<some-pkg-mgr> install python3")
* pip3 install requests

Configure:
====

* mv ./config.ini.sample ./config.ini
* Fill in config.ini with "real" values (sorry about that for now, but you'll have to obtain last.fm api account here: http://www.last.fm/api/account/create)

Run:
====

* python3 ./move.py --source=loved|library --limit=42

TODOs:
====
* Refactoring
* Put it online (or add some kind of GUI)
* Something completely different
* More output
* Allow user to select a correct track from search results
* Skip/overwrite already processed tracks

