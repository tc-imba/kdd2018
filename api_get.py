# coding: utf-8

import requests
import datetime
import getopt
import sys

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

# Get UTC Date
now = datetime.datetime.utcnow()
start_datetime = now + datetime.timedelta(days=-7)
start_date = start_datetime.strftime('%Y-%m-%d-00')
end_date = now.strftime('%Y-%m-%d-23')

print('Getting air quality of %s from %s to %s ...' % (city, start_date, end_date))

url = 'https://biendata.com/competition/airquality/%s/%s/%s/2k0d1d8' % (city_alias, start_date, end_date)
response = requests.get(url)
f = open('%s_recent_aq.csv' % city, 'w')
f.write(response.text.replace('\r', ''))
f.close()

print('Finished')
