import re
import requests
import time
import getpass
from pprint import pprint
from bs4 import BeautifulSoup

AIB_LOGIN_URL = 'https://aibinternetbanking.aib.ie/inet/roi/login.htm'

VERIFY_CERTIFICATE = True

GET_HEADERS = {
'Host': 'aibinternetbanking.aib.ie',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
'Accept-Encoding': 'gzip,deflate,sdch',
'Accept-Language': 'en-US,en;q=0.8'}

POST_HEADERS = dict(GET_HEADERS)
POST_HEADERS.update({
'Origin': 'https://aibinternetbanking.aib.ie',
'Content-Type': 'application/x-www-form-urlencoded',
'Referer': 'https://aibinternetbanking.aib.ie/inet/roi/login.htm',
    })

def login():
    s = requests.Session()
    firstPage = s.get(AIB_LOGIN_URL, verify=VERIFY_CERTIFICATE, headers=GET_HEADERS)
    soup = BeautifulSoup(firstPage.text)

    REGISTRATION_NUMBER = getpass.getpass('Registration Number: ')
    params = {
        'transactionToken': soup.find(id='transactionToken').get('value'),
        '_target1': 'true',
        'jsEnabled': 'FALSE',
        'regNumber': REGISTRATION_NUMBER
    }
    secondPage = s.post(AIB_LOGIN_URL, data=params, headers=POST_HEADERS, verify=VERIFY_CERTIFICATE)
    
    soup = BeautifulSoup(secondPage.text)
    PHONE_CHALLENGE = getpass.getpass('Last 4 digits of phone number: ')
    params = {
        'transactionToken': soup.find(id='transactionToken').get('value'),
        '_finish': 'true',
        'jsEnabled': 'FALSE',
        'challengeDetails.challengeEntered': PHONE_CHALLENGE
    }
    for i, digit_label in enumerate(soup.find_all('strong', text=re.compile('Digit \d'))):
        pac_index = int(digit_label.text[-1])
        params['pacDetails.pacDigit%s' % (i + 1)] = getpass.getpass('PAC Digit %s:' % pac_index)
    
    thirdPage = s.post(AIB_LOGIN_URL, data=params, headers=POST_HEADERS, verify=VERIFY_CERTIFICATE)
    
    import code; code.interact(local=locals())
    
if __name__ == '__main__':
    login()