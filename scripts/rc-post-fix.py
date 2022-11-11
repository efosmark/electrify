# -*- coding: utf-8 -*-
import os
import sys
import re

if __name__ == '__main__':
    DIR = sys.argv[1]

    if not os.path.exists(DIR):
        raise Exception("Directory cannot be found. " + str(sys.argv[0]))

    for file in os.listdir(DIR):
        if re.match('^ui_(.+?)\.py$', file):
            with open("{}/{}".format(DIR, file), "r+") as ui_file:
                texts = ui_file.read()
                texts, n = re.subn(
                    r'import ([\w]+?)_rc',
                    r'from . import rc_\1',
                    texts
                )
                ui_file.seek(0)
                ui_file.write(texts)
                if n > 0:
                    print("File '{}' processed. {} replacement{} made.".format(file, n, 's' if n != 1 else ''))
