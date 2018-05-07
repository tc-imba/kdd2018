import json
import csv
import datetime
import model
import getopt
import sys

try:
    options, args = getopt.getopt(sys.argv[1:], "c:s:", ["city=", "station="])
except getopt.GetoptError:
    sys.stderr.write('error: getopt')
    sys.exit()

city = None
station = None
for name, value in options:
    if name in ("-c", "--city"):
        city = value
    elif name in ("-s", "--station"):
        station = value

if city == 'beijing':
    city_alias = 'bj'
    predict_arr = [1, 2, 5]
elif city == 'london':
    city_alias = 'ld'
    predict_arr = [1, 2]
else:
    sys.stderr.write('error: city %s is not defined' % city)
    sys.exit()

stations = json.load(open('%s.json' % city))
if station:
    if station in stations:
        stations = [station]
    else:
        sys.stderr.write('error: station %s is not defined' % station)
        sys.exit()

city_data = {}
for station in stations:
    city_data[station] = []

reader = csv.reader(open('%s_recent_aq_fixed.csv' % city))
for row in reader:
    if city_data.__contains__(row[1]):
        arr = [x and float(x) or 0 for x in row[3:]]
        city_data[row[1]].append([row[2]] + arr)

# Load calculated data
submission_data = {}
for station in json.load(open('beijing.json')):
    submission_data[station] = []
for station in json.load(open('london.json')):
    submission_data[station] = []
for station in submission_data:
    for i in range(48):
        submission_data[station].append([0, 0, 0])
try:
    f = open('submission.csv')
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 0:
            pos = row[0].find('#')
            station = row[0][0:pos]
            if submission_data.__contains__(station):
                index = int(row[0][pos + 1:])
                # print(station, index)
                submission_data[station][index] = row[1:]
    f.close()
except FileNotFoundError:
    pass

time_format = '%Y-%m-%d %H:%M:%S'
end_datetime = datetime.datetime.strptime(city_data[stations[0]][-1][0], time_format)
predict_start = end_datetime  # + datetime.timedelta(hours=1)
submission_start = datetime.datetime.combine(end_datetime.date(), datetime.time.min) \
                   + datetime.timedelta(hours=24)
predict_end = submission_start + datetime.timedelta(hours=47)

station_index = 0
for station in stations:
    station_index += 1
    print('Processing %s - %s (%d/%d)' % (city, station, station_index, len(stations)))
    data = list(zip(*city_data[station]))
    for i in range(len(predict_arr)):
        # if all data is zero, the model gg
        not_zero = 0
        for j in data[predict_arr[i]]:
            if j > 0:
                not_zero += 1
        if not_zero < len(data[predict_arr[i]]) / 3:
            for index in range(48):
                submission_data[station][index][i] = 0
            continue

        predict = model.analyze(data[predict_arr[i]], data[0], predict_start, predict_end)
        index = 0
        for j in range(len(predict.index)):
            if predict.index[j] >= submission_start:
                # print(predict.index[j], predict[j])
                submission_data[station][index][i] = max(predict[j], 0)
                index += 1

f = open('submission.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerow(['test_id', 'PM2.5', 'PM10', 'O3'])

for station in submission_data:
    for i in range(len(submission_data[station])):
        writer.writerow([station + '#' + str(i)] + submission_data[station][i])

f.close()
