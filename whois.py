#!/usr/bin/env python3
import datetime

import requests
import vlermv
import lxml.html

url = 'http://nic.io/cgi-bin/whois'

@vlermv.cache('~/.io-whois')
def get(domain):
    return requests.get(url, params = {'query': domain})

def parse(response):
    html = lxml.html.fromstring(response.text)
    rawdate = html.xpath('//td[text() = "First Registered :"]/following-sibling::td/text()')[0]
    return datetime.datetime.strptime(rawdate, '%Y-%m-%d').date()
