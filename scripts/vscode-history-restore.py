import os
import json
import shutil

lookfor = 'file:///media/k7fos/0056-E500/workspace/electrified/'

DIR = '/home/k7fos/Documents/vscode-history'


for file in os.listdir(DIR):
    file = os.path.join(DIR, file)
    if os.path.isdir(file):
        entryfile = os.path.join(file, 'entries.json')
        if os.path.exists(entryfile):
            with open(entryfile, 'r') as fh:
                entry = json.load(fh)
                if lookfor in entry['resource']:
                    entries = sorted(entry['entries'], key=lambda e:e['timestamp'], reverse=True)

                    current_location = os.path.join(file, entries[0]['id'])
                    new_location = os.path.join(DIR, '_from-backup/', entry['resource'][len(lookfor):])
                    new_folder = new_location[:new_location.rfind('/')]

                    print(current_location)
                    print(new_location)
                    print(new_folder)
                    print('')
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder, 777)
                    shutil.copy2(current_location, new_location)
