# Zoom.Module_Autopsy.Plugin
This ingest module used to decrypt Zoom database and process Zoom artifacts.
## the project has two scripts:

•	The first tool for retrieving the keys called zoom_keys.py.
The remote key part was based by the following tool 
script used code written by” Alba Mendez” https://github.com/mildsunrise/protobuf-inspector.git . 
To run, with Python 3.7 is needed with the following Python modules installed: dpapick3, Crypto, pathlib, blackboxprotobuf, configparser, hashlib, os,requests, sys, urllib.

•	The second tool in the repository composes the add-on modules. Downloading and placing it in the appropriate directory is all that's needed (the ingest module that run on Autopsy Version 4.18.0).
## Experimental Environment:
Devices/Tools	Introduction	Specification/Versions
VMware® Workstation 16 Pro	Virtual machine software	Version 16.1.2 build-17966106
Windows 10	Microsoft operation system	Windows 10 Pro, 64-bit 
(Build 19042.1165)
Zoom Application 	Zoom online virtual meetings, chat live, share screens, other communication features.	Version 5.7.4 (804)
| Devices/OS    | Specification/Versions |
| ------------- | ------------- |
| VMware® Workstation 16 Pro | Version 16.1.2 build-17966106  |
| Windows 10 | Windows 10 Pro, 64-bit (Build 19042.1165)|
| Zoom Application  | Version 5.7.4 (804)|
