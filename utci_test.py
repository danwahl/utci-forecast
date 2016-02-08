# -*- coding: utf-8 -*-
"""

"""

import requests
import utci
import utci_keys
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter
from numpy import arange
#import json

from Adafruit_IO import Client

aio = Client(utci_keys.aio_key)

#lat = 41.977295
#lon = -87.693851

lat = 41.8369
lon = -87.6847

r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=%s' % (str(lat), str(lon), ow_key))
data = r.json()
#print rj

utci_forecast = []
temp_forecast = []
dt = []

d = datetime.datetime.now()
dt.append(datetime.datetime.now())
Ta = data['main']['temp'] - 273.15
RH = data['main']['humidity']
va = data['wind']['speed']
cr = data['clouds']['all']/100.0

#print Ta, va, RH, cr

temp_forecast.append(Ta)
utci_forecast.append(utci.get_utci(Ta, va, RH, lat, lon, cr, d))

r = requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=%s' % (str(lat), str(lon), utci_keys.ow_key))
data = r.json()
#print data

cnt =  data['cnt']
for i in range(cnt):
    d = datetime.datetime.fromtimestamp(data['list'][i]['dt'])
    dt.append(d)
    Ta = data['list'][i]['main']['temp'] - 273.15
    RH = data['list'][i]['main']['humidity']
    va = data['list'][i]['wind']['speed']
    cr = data['list'][i]['clouds']['all']/100.0
    #print Ta, RH, va, cr
    temp_forecast.append(Ta)
    utci_forecast.append(utci.get_utci(Ta, va, RH, lat, lon, cr, d))

fig, ax = plt.subplots()
ax.plot(dt, utci_forecast, dt, temp_forecast)

ax.set_xlim(dt[0], dt[-1])

ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()

plt.show()

for i in range(1, len(utci_forecast)):
    print dt[i], utci.get_name(utci.get_cat(utci_forecast[i]))
    #print utci.get_cat(utci_forecast[i])

#data = Data(value = 0)
#aio.create_data('welcome-feed', data)

# Get list of groups.
#groups = aio.groups()

# Print the group names and number of feeds in the group.
#for g in groups:
#    print('Group {0} has {1} feed(s).'.format(g.name, len(g.feeds)))

#feed_name = 'utci-now'
#base_url='https://io.adafruit.com'
#path = "api/feeds/{0}/data/send".format(feed_name)
#url = '{0}/{1}'.format(base_url, path)
#data = json.dumps({'value': utci_now})
#print url

#print requests.post(url, headers={'X-AIO-Key': aio_key,'Content-Type': 'application/json'}, proxies=None, data=data)

#aio.send('utci-now', utci_now)