from __future__ import print_function

import csv
import requests
import sys

URL="http://localhost:9090"

def GetMetricNames(url):
    response = requests.get('{0}/api/v1/label/__name__/values'.format(url))
    names = response.json()['data']
    #Return metrix names
    return names

def main():
    mn = GetMetricNames(URL)
    print("\n".join(mn))

if __name__=="__main__":
    main()
