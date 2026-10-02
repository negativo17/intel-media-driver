#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2026 Simone Caronni <negativo17@gmail.com>
# Licensed under the GNU General Public License Version or later

import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("usage: %s <extracted tarball> com.intel.media_driver.metainfo.xml" % sys.argv[0])
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

    appstream_xml = ElementTree.parse(sys.argv[2])
    root = appstream_xml.getroot()
    provides = ElementTree.SubElement(root, "provides")

    for pid in sorted(pids):
        vid = 0x8086
        modalias = ElementTree.SubElement(provides, "modalias")
        modalias.text = "pci:v%08Xd%08Xsv*sd*bc*sc*i*" % (vid, pid)

    ElementTree.indent(root, space="  ", level=0)
    # appstream-util validate requires the xml header
    appstream_xml.write(sys.argv[2], encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()
