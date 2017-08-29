#!/usr/bin/env python3.5

import csv
import sys
from collections import OrderedDict

status = OrderedDict()

with open(sys.argv[1]) as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        status_type, status_number, *content = row
        status[status_type.strip().upper(), int(status_number)] = tuple(content)

with open(sys.argv[2]) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        status_types, status_number, _, _, descr, detail, action = row
        for status_type in status_types.split():
            key = status_type.strip().upper(), int(status_number)

            try:
                cat = status[key][0]
            except KeyError:
                cat = "N/A"

            status[key] = (cat.strip(), descr.strip(), detail.strip(), action.strip())


print("\nTRACKING_STATUS = {")
for key in sorted(status, key=lambda k: (k[1], k[0])):
    value = status[key]
    print("    {!r}: {!r},".format(key, value))
print("}")
