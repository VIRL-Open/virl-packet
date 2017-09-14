#!/usr/bin/env python3

"""Deploy a VIRL system on Packet identified by the provided UUID.

Usage:
  virl_packet_destroy -a <API_KEY> -u <UUID>  [ ( --q | --qq | --json ) ]

Arguments:
  -a <API_KEY>          An API key associated with your Packet account.
  -u <UUID>             The UUID of the system to destroy

Options:

  --q                   Display just the status, set exit-code
  --qq                  Display nothing, set exit-code
  --json                Display the full JSON response, set exit-code

"""

import sys
import requests
import json
import simplejson
from docopt import docopt

IPXE_URL = "http://packet.virl.info"
API_URL = "https://api.packet.net"
CONTENT_TYPE = "application/json"

associated_status = {204: "Success", 401: "Unauthorized", 422: "Unprocessable", 403: "Forbidden", 404: "Not Found"}

headers = {}

if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0rc3')

    # Form the request header
    headers.update({"content-type" : CONTENT_TYPE}) 
    headers.update({"X-Auth-Token" : arguments['-a']})

    # Form our URL with the Project-ID parameter
    url = ('{0}/devices/{1}'.format(API_URL,arguments['-u']))

    # Make the call to Packet
    try:
        r = requests.delete(url, headers=headers)
    except requests.ConnectionError:
        print ("An error occured while attempting to connect to Packet.")
        sys.exit(1)

    # Show some output, or not.
    if arguments['--q']:
        print(associated_status[r.status_code])
    elif arguments['--json']:
        print(simplejson.dumps(r.json(), sort_keys=True, indent=4))
 
    sys.exit(r.status_code)


