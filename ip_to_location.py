"""
Written by Dan Ngo

Python script to lookup Geolocation data of an IP address using Freegeoip.net

Install the requests library using "pip install requests"
"""

# Import libraries
import requests
import sys
import os
import json

# Definte a function to write the results to a JSON file
def file_output(fileoutput):
    """Output results to to a file"""
    with open(fileoutput, 'w') as outfile:
        json.dump(data, outfile)
        print('Results written to: ' + fileoutput)


def main():
    # Check arguments for IP address and options from the command line input
    args = sys.argv[1:]
    if not args:
        print "usage: [ip address] [-f abosolute path to file output]"
        sys.exit(1)

    # Set variables for the arguments
    if len(args) < 2:
        ipv4address = args[0]
    else:
        ipv4address = args[0]
        fileoutput = args[2]

    # Grab the results from FreeGeoIP
    results = requests.get('https://freegeoip.net/json/{}'.format(ipv4address))

    # Check if we get a result back and either print the result or output to file
    if results.status_code == 200:
        global data
        data = results.json()
        if fileoutput:
            file_output(fileoutput)
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
