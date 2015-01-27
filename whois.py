#!/usr/bin/env python3
import csv
from functools import partial
import datetime

import requests
import vlermv
import lxml.html

url = 'http://nic.io/cgi-bin/whois'

@vlermv.cache('~/.io-whois/other')
def get_other(url):
    return requests.get(url)

@vlermv.cache('~/.io-whois/whois')
def get(domain):
    'Get a WHOIS record.'
    return requests.get(url, params = {'query': domain})

def _query_html(html, key):
    'Query the body of a WHOIS record.'
    return str(html.xpath('//td[text() = "%s"]/following-sibling::td/text()' % key)[0])

def parse(response):
    'Parse a whois response.'
    html = lxml.html.fromstring(response.text)
    query = partial(_query_html, html)
    date = datetime.datetime.strptime(query('First Registered :'), '%Y-%m-%d').date()
    return {
        'domain-name': query('Domain Name :'),
        'first-registered': date,
    }

def most_popular():
    'List the most popular .io domains, based on someone\'s idea of popularity.'
    response = get_other('http://hack.ly/articles/the-most-popular-dot-io-domains/')
    html = lxml.html.fromstring(response.text)
    return map(str, html.xpath('//div[@class="entry-content"]/descendant::a/text()'))

def main():
    import sys
    writer = csv.DictWriter(sys.stdout, ('domain-name', 'first-registered'))
    for domain in most_popular():
        response = get(domain)
        if not response.ok:
            sys.stderr.write('Error downloading "%s"\n' % domain)
            sys.exit(1)

        try:
            data = parse(response)
        except Exception as e:
            sys.stderr.write('Error parsing the "%s" record:\n%s\n' % (domain, e))
            sys.exit(2)

        writer.writerow(data)

if __name__ == '__main__':
    main()
