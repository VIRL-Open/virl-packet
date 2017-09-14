#!/usr/bin/env python3

"""Display the deployment status of a VIRL system identified by UUID.
Exit once the system is ready for use.

Usage:
  virl_packet_destroy -a <API_KEY> -u <UUID> [ -q | --qq ] 

Arguments:
  -a <API_KEY>  An API key associated with your Packet account.
  -u <UUID>     The UUID of the system to destroy

Options:

-q              No status, just exit with the IP of the deployed system
--qq            No output at all - just exit with 0 when the system is ready

"""

import sys
import requests
import json
import simplejson
from docopt import docopt
import time
import re

IPXE_URL = "http://packet.virl.info"
API_URL = "https://api.packet.net"
CONTENT_TYPE = "application/json"

associated_status = {200: "Success", 401: "Unauthorized", 422: "Unprocessable", 403: "Forbidden", 404: "Not Found"}

headers = {}
state = ""
last_body = ""

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0rc3')

    # Form the request header
    headers.update({"content-type" : CONTENT_TYPE}) 
    headers.update({"X-Auth-Token" : arguments['-a']})

    # Form our URL with the Project-ID parameter
    url = ('{0}/devices/{1}/events'.format(API_URL,arguments['-u']))

    print('\n')

    # Check the status in a loop until we see success
    while state != "succeeded":

      # Make the call to Packet
      try:
          r = requests.get(url, headers=headers)
      except requests.ConnectionError:
          print ("An error occured while attempting to connect to Packet.")
          sys.exit(1)

      # Test for a successfull response
      if r.status_code != 200:
        print(associated_status[r.status_code])
        sys.exit(r.status_code)

      # Grab the state and body elements from the returned JSON
      state = r.json()['events'][0]['state']
      body = r.json()['events'][0]['body']

      # See if the status has changed.  Wait if not, otherwise display the status
      if body == last_body:
        # Wait a bit.
        time.sleep(5)
      
      elif not arguments['-q'] and not arguments['--qq']:
        if state == "running" or state == "succeeded":
          # This is a normal run and we're out of provisioning, display the status
          print('{0}: {1}'.format(state.title(), body))
        else:
          print("Provisioning the system - please wait.")
      
      elif arguments['-q'] and state == "succeeded":
        # This is an IP-only run and the deployment is done.  Display the IP
        ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', body )
        print(ip[0])
        sys.exit(0)

      elif arguments['--qq'] and state == "succeeded":
        # This is a super-quiet run and the deployment is done.  Exit 0
        sys.exit(0)
 
      # Save the last status to check next time around.
      last_body = body

    #Done
    print('\n')
    sys.exit(r.status_code)


