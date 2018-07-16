#!/usr/bin/env python3

#  Copyright (C) 2018 Jussi Pakkanen.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of version 3, or (at your option) any later version,
# of the GNU General Public License as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys
import time
from glob import glob
import platform

if platform.system() == 'Windows':
    fake_compiler = ['cl', '/?']
else:
    fake_compiler = ['gcc', '-v']

def get_globlist():
    globlist = []
    srcexts = ('.h', '.hh', '.hpp', '.H', '.c', '.cc', '.cpp', '.C')
    for root, dirs, files in os.walk('.'):
        cur_exts = {}
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            fext = os.path.splitext(f)[1]
            if fext in srcexts:
                cur_exts[fext] = True
        for e in cur_exts:
            globlist.append(os.path.join(root, '*' + e))
    return globlist

def do_globs(globlist):
    num_sources = 0
    for d in globlist:
        num_sources += len(glob(d))
    print('Total sources:', num_sources)

def scan_ten(fname, simulate_process_spawn=False):
    lines = 0
    if simulate_process_spawn:
        import subprocess
        subprocess.check_call(fake_compiler,
                              stdin=subprocess.DEVNULL,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    with open(fname, encoding='utf-8', errors='ignore') as f:
        for line in f:
            lines += 1
            if lines >= 10:
                return

def scan_and_glob(globlist):
    for i, g in enumerate(globlist):
        if i%1000 == 0:
            print('Scanning pattern', i)
        if g.endswith('.cpp') or g.endswith('.cc'):
            for m in glob(g):
                scan_ten(m, True)
        #for hglob in ('*.h', '*.hpp', '*.hh'):
        #    for m in glob(os.path.join(d, hglob)):
        #        scan_ten(m)

if __name__ == '__main__':
    starttime = time.time()
    globlist = get_globlist()
    print('Total glob patterns:', len(globlist))
    scantime = time.time()
    print('Basic scan took %ds.' % int(scantime-starttime))
    do_globs(globlist)
    globtime = time.time()
    print('Globbing took %ds' % int(globtime-scantime))
    scan_and_glob(globlist)
    endtime = time.time()
    print('Scanning took %ds' % int(endtime-scantime))
