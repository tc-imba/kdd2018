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

print('Fixing air quality of %s' % city)

reader = csv.reader(open('%s_recent_aq.csv' % city))
stations = json.load(open('%s_all.json' % city))
time_format = '%Y-%m-%d %H:%M:%S'

index = 0
col_names = None
city_data = {}
for station in stations:
    city_data[station] = {}

for row in reader:
    if not col_names:
        col_names = row
    else:
        station = row[1]
        time = row[2]
        if city_data.__contains__(station):
            arr = [x and float(x) or 0 for x in row[3:]]
            city_data[station][time] = row[0:3] + arr

# print(city_data)
f = open('%s_recent_aq_fixed.csv' % city, 'w', newline='')
writer = csv.writer(f)
writer.writerow(col_names)
for station, data in city_data.items():
    data = sorted(data.items(), key=lambda e: e[0])
    writer.writerow(data[0][1])
    for i in range(1, len(data)):
        row_start = data[i - 1][1]
        row_end = data[i][1]
        start = datetime.datetime.strptime(row_start[2], time_format)
        end = datetime.datetime.strptime(row_end[2], time_format)
        diff = int((end - start).seconds / 3600)
        for j in range(1, diff):
            row = ['0000000', station, (start + datetime.timedelta(hours=j)).strftime(time_format)]
            for k in range(3, len(row_start)):
                row.append(round(row_start[k] + (row_end[k] - row_start[k]) / diff * j, 2))
            writer.writerow(row)
        writer.writerow(data[i][1])
f.close()
