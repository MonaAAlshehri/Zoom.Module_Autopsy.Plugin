# Zoom.Module_Autopsy.Plugin
This ingest module used to decrypt Zoom database and process Zoom artifacts.
## the project has two scripts:

•	The first tool for retrieving the keys called zoom_keys.py.
The remote key part was based by the following tool 
script used code written by” Alba Mendez” https://github.com/mildsunrise/protobuf-inspector.git . 
To run, with Python 3.7 is needed with the following Python modules installed: dpapick3, Crypto, pathlib, blackboxprotobuf, configparser, hashlib, os,requests, sys, urllib.

•	The second tool in the repository composes the add-on modules. Downloading and placing it in the appropriate directory is all that's needed (the ingest module that run on Autopsy Version 4.18.0).
