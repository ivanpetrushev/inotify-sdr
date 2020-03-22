# in case of  inotify.calls.InotifyError: Call failed (should not be -1): (-1) ERRNO=(0)
# increase max_user_watches:
# sudo sysctl fs.inotify.max_user_watches=524288
# sudo sysctl -p

import inotify.adapters
from glob import glob
import os
import subprocess
import re

SRC_DIR = '/home/ivanatora/Downloads/timestampSDR/recordings'
DST_DIR = '/home/ivanatora/Downloads/timestampSDR/recordings/mp3'
# for extracting the date portion of the filenames, for example "2020-03-21 22:13:07.891.wav"
# no need to change this if using the recommended dateFmt from start-timestampSDR.sh
DATE_REGEX = '\d{4}-\d{2}-\d{2}'

if not os.path.exists(DST_DIR):
    os.mkdir(DST_DIR)


def process_file(file_name):
    print('Checking', file_name)
    file_name_mp3 = file_name.replace('wav', 'mp3')
    match = re.search(DATE_REGEX, file_name)
    if match:
        date = match.group()
        if not os.path.exists(DST_DIR + '/' + date):
            print('Creating new date directory: ', date)
            os.mkdir(DST_DIR + '/' + date)
        print('Compressing: ', file_name)
        oldfile_path = SRC_DIR + '/' + file_name
        newfile_path = DST_DIR + '/' + date + '/' + file_name_mp3
        cmd_args = ['ffmpeg', '-y', '-i', oldfile_path, newfile_path]
        status = subprocess.run(cmd_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if status.returncode != 0:
            print('ERROR trying to convert file. Args were: ', cmd_args)
        else:
            os.remove(oldfile_path)
    else:
        print('Unrecognized file pattern: ', file_name)


def parse_existing():
    print('Processing already existing files...')
    for file_path in glob(SRC_DIR + '/*wav'):
        file_name = os.path.basename(file_path)
        process_file(file_name)


def track_new_files():
    print('Tracking for new files...')
    last_notified_file = None
    i = inotify.adapters.Inotify()

    i.add_watch(SRC_DIR)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, file_name) = event

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, file_name, type_names))
        if 'IN_CLOSE_WRITE' in type_names:
            # for some reason timestampSDR emits IN_CLOSE_WRITE twice after save, trigger only on second
            if file_name == last_notified_file:
                process_file(file_name)
            else:
                last_notified_file = file_name


if __name__ == '__main__':
    parse_existing()
    track_new_files()
