from bs4 import BeautifulSoup
import requests
from requests import exceptions
import re
import interval_timer
from time import sleep
import time
import sys


PLAYSTORE_URL = 'https://play.google.com/store/apps/details?id='
APP_NAME = 'com.iaa.mobile.IaaTow'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 ' \
             'Safari/537.36 '
HEADER = {'User-Agent': USER_AGENT}
TIMEOUT = 15
rt = None
# <div class="hAyfc"><div class="BgcNfc">Current Version</div><span class="htlgb"><div class="IQ1z0d"><span class="htlgb">7.7</span></div></span></div>

def get_app_version():
    url = PLAYSTORE_URL+APP_NAME
    is_not_timeout, soup = get_soup(url, None)
    if is_not_timeout:
        # print(soup)
        desc = []
        curr_version =''
        for de in soup.find_all('div', attrs={'class': 'hAyfc'}):
            #print(de.get_text().strip())
            if 'Current Version' in de.get_text().strip():
                curr_version = de.get_text()
            desc.append(de.get_text().strip())
        print(curr_version) 
        if str('7.8') in curr_version:
            print('version updtaed')
            rt.stop()
        


def get_soup(url, params):
    try:
        r = requests.get(url, headers=HEADER, timeout=TIMEOUT)
    except exceptions.Timeout as e:
        return False, 'timeout'
    except exceptions as b:
        return False, b
    else:
        return True, BeautifulSoup(r.text,"html.parser")



def request_validation_in_intervals():
    global rt
    rt = interval_timer.RepeatedTimer(1, get_app_version) # it auto-starts, no need of rt.start()
    
    try:
        sleep(10000) # your long-running job goes here...
    finally:
        rt.stop() # better in a try/finally block to make sure the program ends!

def execute_script():
    conn = pymssql.connect(
    host='PMOBSQLDB01',
    user='CORPORATE\RGautam',
    database='IAATow'
    )
    cursor = conn.cursor()
    cursor.execute('Select top 10 * from dbo.IAATow_Config ic  with (NOLOCK) WHERE Application_Name =%s', 'android')

    for row in cursor:
        print('row = %r' % (row,))
    conn.close()
# execute_script()
request_validation_in_intervals()