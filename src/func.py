import json
import socket
import time
from time import mktime
from datetime import datetime, date

import os

import psutil
import requests
from pytz import timezone
from weather import Unit, Weather
import multiprocessing

import random
import parsedatetime as pdt

def get_ip(inputs = {}):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return {'ip' : IP}

def get_date(inputs = {}):
  today = date.today()
  month = today.strftime('%B')
  day = today.day

  if (3 < day < 21) or (23 < day < 31):
    suffix = 'th'
  else:
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    suffix = suffixes[day % 10]
  
  return {'day' : day, 'day_suffix' : suffix, 'month' : month}

def get_time(inputs = {'location' : ''}):

  place = ''
  if not len(inputs.items()) == 0:
    place = inputs['location']
  
  if place == '':
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%I %M %p')
    tTime = st.split(' ')
    t = str(int(tTime[0])) + ' ' + tTime[1] + ' ' + tTime[2]
    return {'time' : t}

  from tzwhere import tzwhere
  place = place.replace(' ', '+')
  search_details = 'https://geocoder.api.here.com/6.2/geocode.json?app_id=cb870QP7ugZzb4tWAcKI&app_code=d4xPcsr4E8fj_rzUNhkXgQ&searchtext=' + place

  resp = requests.get(url=search_details, params='')
  data = resp.json()
  

  tz = tzwhere.tzwhere()
  lat = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Latitude']
  lon = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']['Longitude']

  
  timeZoneStr = tz.tzNameAt(lat, lon)
  timeZoneObj = timezone(timeZoneStr)
  ts = datetime.now(timeZoneObj).strftime('%H:%M:%S')
  return {'time' : ts}

def get_cpu_max_process(inputs = {}):
  name = ''
  cpu = '0.0'
  CPU_CORE = float(multiprocessing.cpu_count())
  for _ in range(4):
      pro = {float(proc.cpu_percent(interval=None) / CPU_CORE) : str(proc.name()) for proc in psutil.process_iter()}
      cpu = max(pro.keys(), key=float)
      name = pro[cpu]
      #if not _name == 'pythonw.exe':
      #cpu = _cpu
      #name = _name
      #print(name, ' : ', cpu, '%')
  return {'name' : name, 'percent' : str(cpu) + '%'}

def get_weather_current(inputs = {'location' : ''}):
  
  location = ''
  if not len(inputs.items()) == 0:
    location = inputs['location']

  weather = Weather(unit=Unit.CELSIUS)
  
  if location == '':
    r = requests.get(url = 'https://ipinfo.io/loc', params = '').text
    lookup = weather.lookup_by_latlng(r.split(',')[0], r.split(',')[1])
  else:
    lookup = weather.lookup_by_location(location)
    
  condition = lookup.condition
  location = lookup.location
  forecast = lookup.forecast
  return {'condition' : condition.text, 'temp_current' : condition.temp, 'scale' : 'C', 'diff_location' : location.city + ', ' + location.country, 'temp_max' : forecast[0].high, 'temp_min' : forecast[0].low }

def get_weather_next_day(inputs = {'location' : ''}):
  
  location = ''
  if not len(inputs.items()) == 0:
    location = inputs['location']

  weather = Weather(unit=Unit.CELSIUS)
  
  if location == '':
    r = requests.get(url = 'https://ipinfo.io/loc', params = '').text
    lookup = weather.lookup_by_latlng(r.split(',')[0], r.split(',')[1])
  else:
    lookup = weather.lookup_by_location(location)
    
  condition = lookup.condition
  location = lookup.location
  forecast = lookup.forecast
  return {'condition' : forecast[1].text, 'diff_location' : location.city + ', ' + location.country, 'temp_max' : forecast[1].high, 'temp_min' : forecast[1].low }

def set_alarm(inputs = {'time' : '', 'date' : ''}):
  
  if not 'time' in inputs.keys():
    time = datetime.now()
  else:
    time = inputs['time'].replace('next', '+1')
  
  if not 'date' in inputs.keys():
    date = datetime.today().strftime('%m/%d/%Y')
  else:
      if inputs['date'] == 'today':
        date = datetime.today().strftime('%m/%d/%Y')
      else:
        date = inputs['date']
  name = 'alarm'
  str_dt = time + ' ' + date
  p = pdt.Calendar()
  _datetime = p.parse(str_dt)
  dt = datetime.fromtimestamp(mktime(_datetime[0]))
  time = str(dt.time())
  date = str(dt.strftime('%m/%d/%Y'))
  name = name + '|' + time + '|' + date
  name = name.replace(':', '').replace('/', '').replace('|', '')
  f = open('alarmList.txt', 'a')
  f.write(name + '|' + time + '|' + date + '\n')
  f.close()
  cwd = os.getcwd()
  print(cwd)
  comd = 'schtasks /create /tn \"' + name + '\" /tr ' + cwd + '\\alarm.bat /sc once /st ' + str(time) + ' /sd ' + str(date)
  os.system(comd)
  return {'weekday' : dt.strftime('%A'), 'hour' : dt.strftime('%I'), 'minute' : dt.strftime('%M'), 'am_pm' : dt.strftime('%p')}

def remove_alarm(inputs = {}):
    f = open('alarmList.txt', 'r')
    lines = f.readlines()
    f.close()
    names = [line.split('|')[0] for line in lines]
    template = 'schtasks /delete /tn '
    [os.system(template + name + ' /F') for name in names]
    f = open('alarmList.txt', 'w')
    f.write('')
    f.close()
    return {}

def list_alarm(inputs = {}):
    f = open('alarmList.txt', 'r')
    lines = f.readlines()
    f.close()
    names = [[line.split('|')[0], line.split('|')[1] + ' ' + line.split('|')[2]] for line in lines]
    p = pdt.Calendar()
    datetimelist = [(name[0], datetime.fromtimestamp(mktime(p.parse(name[1])[0]))) for name in names]
    datetimelist = [Adatetime for (name, Adatetime) in datetimelist if Adatetime > datetime.now()]
    datetimelist = [dt.strftime('%A, %d. %B %Y at %I:%M%p') for dt in datetimelist]
    datetimelist = ', '.join(datetimelist)
    if datetimelist == '':
        return {'alarms' : 'No Alarms Found'}
    return {'alarms' : datetimelist}

def why_skill_failed(inputs = {'skill' : ''}):
    f = open('error.log', 'r')
    lines = f.readlines()
    if lines == []:
        return {'skill' : '', 'error' : 'No Error Found'}
    if not inputs['skill'] == '':
        lines = [line for line in lines if line.split('|')[0] == inputs['skill']]
    error = lines[len(lines) - 1]
    f.close()
    return {'skill' : error.split('|')[0], 'error' : error.split('|')[1]}

def get_jokes(inputs = {}):
  joke=open('jokes.json').read()
  joke = json.loads(joke)
  jcount = joke.__len__()
  joke = str(joke[random.randint(0, jcount)]['body'])

  return {'joke' : joke}

