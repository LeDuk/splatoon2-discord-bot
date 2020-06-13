'''
Created on Jun 13, 2020

@author: leduke
'''
import urllib
import json

def getJSON(url):
    req = urllib.request.Request(url, headers={ 'User-Agent' : 'Magic!' })
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode())
    return data