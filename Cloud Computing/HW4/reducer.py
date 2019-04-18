#!/usr/bin/env python

import sys

ctype = ''
ccount = 0
vtype = ''

for line in sys.stdin:
    line = line.strip()
    vtype,count = line.split(',')
    count = int(count)
    if ctype == vtype:
        ccount += count
    else:
        if ctype != '':
            print '%s\t%s' % (ctype, ccount)
        ctype = vtype
        ccount = count

if ctype == vtype:
    print '%s\t%s' % (ctype, ccount)