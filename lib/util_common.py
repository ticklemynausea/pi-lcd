from time import time
from datetime import datetime
from urllib import request
import subprocess
import re
import json

def timestamp_ms():
  return int(round(time() * 1000))
  
def timestamp_hr():
  return datetime.strftime(datetime.now(), '%a %b %d %H:%M:%S %Y')
  
def ip_str():
  co = subprocess.Popen(['ifconfig'], stdout = subprocess.PIPE)
  ifconfig = co.stdout.read()
  ifconfig = str(ifconfig)
  ip_regex = re.compile('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-4]|2[0-5][0-9]|[01]?[0-9][0-9]?))')
  return " ".join([match[0] for match in ip_regex.findall(ifconfig, re.MULTILINE)])
 

def get_weather(city):
  f = request.urlopen("http://api.wunderground.com/api/%s/geolookup/conditions/q/IA/Matosinhos.json" % "0def10027afaebb7")
  json_string = f.read()
  json_string = json_string.decode("utf8")
  parsed_json = json.loads(json_string)
  location = parsed_json['location']['city']
  data = parsed_json['current_observation']
  
  return "%s %s°C, Wind %s %s" % (location, data['temp_c'], data['wind_string'], data['wind_dir'])
  
