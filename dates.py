# Short script to convert existing date and time values into ISO 8601 format
# Assumption is the olf format is M/D/YYYY for date, and HHMM for time, in separeate CSV fields

import csv
from datetime import datetime

out = open('output.txt', 'w')
f = open('dates.csv', 'r')
c = csv.reader(f)
for row in c:
    date = row[0].split("/")
    time = row[1]

    d = datetime(int(date[2]), int(date[0]), int(date[1]), (int(time[0:2]) - 9), 0, 0).isoformat()
    d += ".000Z"
    out.write(d + "\n")

out.close()
f.close()