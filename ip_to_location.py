"""
Written by Dan Ngo

Python script to lookup Geolocation data of an IP address using Freegeoip.net

Install the requests library using "pip install requests"
"""

# Import libraries
import requests
import argparse
import sys
import os
import json

# Set up CLI arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Find Geolocation data from IP address")
    parser.add_argument('ipv4address', nargs='?')
    parser.add_argument('-f', '--file', nargs='?', required=False, action='store', dest='fileoutput', help='Absolute path to file output', type=argparse.FileType('wb'))
    args = parser.parse_args()
    return args

def main():
    # Check arguments for IP address and options from the command line input
    args = parse_arguments()

    # Grab the results from FreeGeoIP
    results = requests.get('https://freegeoip.net/json/{}'.format(args.ipv4address))

    # Check if we get a result back and either print the result or output to file
    if results.status_code == 200:
        data = results.json()
        if args.fileoutput:
            print args.fileoutput
            args.fileoutput.write(str(data))
        else:
            print data
    else:
        if results.status_code == 404:
            print "404: Couldn't reach FreeGeoIP.net"
        elif results.status_code == 403:
            print "403: Lookup limit exceeded"
        else:
            print "Uknown error"

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
