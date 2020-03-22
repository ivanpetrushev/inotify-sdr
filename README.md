# Info
inotify-sdr is auto-compressing tool for recordings saved from https://github.com/qualitymanifest/timestampSDR/

timestampSDR saves WAV audio in recording/ by default.

inotify-sdr tracks new files and does compression to MP3 + classification by date

Old WAV files are removed to save space

# Requirements
* timestampSDR (obviously) - https://github.com/qualitymanifest/timestampSDR/
* inotify Python module - https://pypi.org/project/inotify/

# Instructions
* run timestampSDR - recommended settings in start-timestampSDR.sh
* set SRC_DIR and DST_DIR in track_changes.py
* run `python3 track_changes.py`

# Troubleshooting
#### inotify.calls.InotifyError: Call failed (should not be -1): (-1) ERRNO=(0)

If you are on Ubuntu/Debian, you probably need to increase `fs.inotify.max_user_watches`:
> sudo sysctl fs.inotify.max_user_watches=524288  
> sudo sysctl -p 