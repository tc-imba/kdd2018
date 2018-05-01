import csv
import json
import getopt
import sys
import datetime

try:
    options, args = getopt.getopt(sys.argv[1:], "c:", ["city="])
except getopt.GetoptError:
    sys.stderr.write('error: getopt')
    sys.exit()

city = None
for name, value in options:
    if name in ("-c", "--city"):
        city = value

if city == 'beijing':
    city_alias = 'bj'
elif city == 'london':
    city_alias = 'ld'
else:
    sys.stderr.write('error: city %s is not defined' % city)
    sys.exit()

reader = csv.reader(open('%s_recent_aq.csv' % city))
stations = json.load(open('%s_all.json' % city))
time_format = '%Y-%m-%d %H:%M:%S'

index = 0
col_names = None
data = []
time = None

for row in reader:
    if not col_names:
        col_names = row
    else:
        if index == 0:
            time = datetime.datetime.strptime(row[2], time_format)
        if row[1] != stations[index]:
            print('Fix station name %s -> %s in' % (row[1], stations[index]), row)
            row[1] = stations[index]
        time_str = time.strftime(time_format)
        if row[2] != time_str:
            print('Fix timestamp %s -> %s in' % (row[2], time_str), row)
            row[2] = time_str
        data.append(row)
        index = (index + 1) % len(stations)


f = open('%s_recent_aq.csv' % city, 'w', newline='')
writer = csv.writer(f)
writer.writerow(col_names)
for row in data:
    writer.writerow(row)
f.close()
