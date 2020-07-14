# API-Import-Manager
API Import Manager <BR>for cisco Cisco Unified Contact Center Enterprise
# Use Case Description
Utility helps to work with outbound option imports for campaigns created via API (upload new contacts to campaign and download current contacts status to file).<BR>
Because it's impossible to do this with standard configuration manager.<BR>
After you entered connections settings in "Connection\Settings" tab, API-Import-Manager encrypt this data and store to file. This file could be opened & decrypted only on the same PC and for same user 
# OS Compatibility
This tool currently tested only on Windows OS. But it should work on all workstations where python is installed.
# Installation
There are 2 choices:
1) You could install packages:<BR>
	Python: https://www.python.org/downloads/ <BR>
	PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5 <BR>
	requests: https://github.com/psf/requests <BR>
	cryptography: https://github.com/pyca/cryptography <BR>
After that copy ImportManager.py, im_GUI.py, vi_utils.py and logo.JPG to your local PC and runImportManager.py<BR>
For installation guide look this sources:<BR>
https://wiki.python.org/moin/BeginnersGuide/Download<BR>
https://packaging.python.org/tutorials/installing-packages<BR>
2) Also there is ImportManager.exe - utility's version compiled for Windows, you could try to use it. It doesn't need installation.
# Presets
This utility no need any presets. All necessary data configuring in "Connection\Settings" window.
![Screenshot](screen.jpg?raw=true "Screenshot")
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/Viktor-84e/API-Import-Manager)
