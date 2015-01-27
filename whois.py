#!/usr/bin/env python3
from functools import partial
import datetime

import requests
import vlermv
import lxml.html

url = 'http://nic.io/cgi-bin/whois'

@vlermv.cache('~/.io-whois')
def get(domain):
    return requests.get(url, params = {'query': domain})

def _query_html(html, key):
    return str(html.xpath('//td[text() = "%s"]/following-sibling::td/text()' % key)[0])

def parse(response):
    html = lxml.html.fromstring(response.text)
    query = partial(_query_html, html)
    date = datetime.datetime.strptime(query('First Registered :'), '%Y-%m-%d').date()
    return {
        'domain-name': query('Domain Name :'),
        'first-registered': date,
    }
