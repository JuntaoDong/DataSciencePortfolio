#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split(',')
    select = words[-5:]
    if select[0] == 'VEHICLE TYPE CODE 1':
        continue
    for word in select:
        if word != '':
            print '%s,%s' % (word, 1)