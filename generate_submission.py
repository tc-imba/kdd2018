import json
import csv

beijing_stations = json.load(open('beijing.json'))
london_stations = json.load(open('london.json'))

writer = csv.writer(open('submission.csv', 'w'))

writer.writerow(['test_id', 'PM2.5', 'PM10', 'O3'])

for station in beijing_stations:
    for i in range(48):
        writer.writerow([station + '#' + str(i), 0, 0, 0])

for station in london_stations:
    for i in range(48):
        writer.writerow([station + '#' + str(i), 0, 0, 0])
