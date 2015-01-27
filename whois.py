import requests
import vlermv

url = 'http://nic.io/cgi-bin/whois'

@vlermv.cache('~/.io-whois')
def get(domain):
    return requests.get(url, params = {'query': domain})

def parse(response):

