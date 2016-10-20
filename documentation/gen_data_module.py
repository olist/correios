#!/usr/bin/env python3.5

import sys
import csv


print("TRACKING_STATUS = {")
with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print("    ({!r}, {!s}): ({!r}, {!r}, {!r}),".format(*row))
print("}")

