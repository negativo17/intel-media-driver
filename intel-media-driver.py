#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Simone Caronni <negativo17@gmail.com>
# Licensed under the GNU General Public License Version or later

import sys
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("usage: %s <extracted tarball>" % sys.argv[0])
        return 1

    pids = []

    for path in Path(sys.argv[1]).rglob('media_sysinfo_*.cpp'):

        f = open(path)
        for line in f.readlines():

            # Remove Windows and Linux line endings
            line = line.replace('\r', '')
            line = line.replace('\n', '')

            if len(line) > 0 and not line.startswith('    RegisterDevice'):
                continue

            # Empty line
            if len(line) == 0:
                continue

            # PCI ID
            pid = int(line[21:25], 16)
            if not pid in pids:
                pids.append(pid)

    for pid in sorted(pids):
        vid = 0x8086
        print("pci:v%08Xd%08Xsv*sd*bc*sc*i*" % (vid, pid))

if __name__ == "__main__":
    main()
