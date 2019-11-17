import os
import urllib
import urllib.parse
import json
import time
import requests
import pandas as pd
import logging
import sys
from fbchat import Client
from fbchat.models import *
from datetime import datetime

from keys import FB_USERNAME, FB_PASSWORD, ACCUWEATHER_API_KEY
from params import RAIN_THRESHOLD, SNOW_THRESHOLD, UPDATE_INTERVAL_HR, DELAY_TIME_HR, LOCATION_ID

url_page = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/" + \
    LOCATION_ID+"?apikey="+ACCUWEATHER_API_KEY+"&details=true&metric=true"

update_interval_sec = 60*60*UPDATE_INTERVAL_HR
delay_time_sec = 60*60*DELAY_TIME_HR

json_page = urllib.request.urlopen(url_page)
json_data = json.loads(json_page.read().decode())
json_df = pd.DataFrame(json_data)

# set maximum width, so the links are fully shown and clickable
pd.set_option('display.max_colwidth', -1)
json_df['Links'] = json_df['MobileLink'].apply(
    lambda x: '<a href='+x+'>Link</a>')

json_df['Real Feel (degC)'] = json_df['RealFeelTemperature'].apply(
    lambda x: x.get('Value'))
json_df['Weather'] = json_df['IconPhrase']
json_df['Percent_Rain'] = json_df['RainProbability']
json_df['Percent_Snow'] = json_df['SnowProbability']
