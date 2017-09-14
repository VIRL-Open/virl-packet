#!/usr/bin/env python3

"""Create a data-file for use with cURL when deploying VIRL to Packet

Usage:
  virl_packet_json -o OUTPUT_FILE -s <SERVER_NAME> ( -0 | -1 | -2 ) ( --nrt | --sjc | --ewr | --ams ) 
       [ -v VIRL_PW ] [ -u UWM_PW ] [ -g GUEST_PW ] [ -l LICENSE_FILE ] 

Arguments:
  -o <OUTPUT_FILE>         The output file
  -s <SERVER_NAME>         The desired system / server name.

Options:
  -0                    System type 0.
  -1                    System type 1.
  -2                    System type 2.
  --nrt                 Facility NRT1.
  --sjc                 Facility SJC1.
  --ewr                 Facility EWR1.
  --ams                 Facility AMS1.
  -v VIRL_PW            VIRL account password
  -u UWM_PW             UWM account password.
  -g GUEST_PW           Guest account password.
  -l LICENSE_FILE       License file (format: id.domain.tld.pem)

"""

import sys
import os
import requests
import json
import simplejson
from docopt import docopt
import time

# Some constants
BILLING = "hourly"
SYSTEM = "custom_ipxe"
IPXE_URL = "http://packet.virl.info"


# Initialize some dictionaries / variables
api_data = {}
cloud_config = "#cloud-config\n"


# Let's get started
if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0.0rc3')

    # What is the hostname?
    api_data.update({"hostname" : arguments['-s']})


    # What system type are we deploying?
    if arguments['-0']:
        type = "baremetal_0"

    elif arguments['-1']:
        type = "baremetal_1"
      
    elif arguments['-2']:
        type = "baremetal_2"

    api_data.update({"plan" : type })


    # What is the billing_cycle?
    api_data.update({"billing_cycle" : BILLING})

    # What facility are we deploying to?
    if arguments['--nrt']:
        facility = "nrt1"
    
    elif arguments['--sjc']:
        facility = "sjc1"
    
    elif arguments['--ewr']:
        facility = "ewr1"

    elif arguments['--ams']:
        facility = "ams1"

    api_data.update({"facility" : facility })


    # What is the operating system?
    api_data.update({"operating_system" : SYSTEM})


    # What is IPXE URL?
    api_data.update({"ipxe_script_url" : IPXE_URL}) 


    # If we have a VIRL login password what is it?
    if arguments['-v']:
        cloud_config += ("virl_password: " + arguments['-v'] + "\n")


    # If we have a UWM account password what is it?
    if arguments['-u']:
        cloud_config += ("uwm_password: " + arguments['-u'] + "\n")


    # If we have a Guest account password what is it?
    if arguments['-g']:
        cloud_config += ("guest_password: " + arguments['-g'] + "\n")


    # If a key-file was provided form the salt-id and domain from the file
    if arguments['-l']:

        # Make sure the file exists
        lic = arguments['-l']
        if not os.path.isfile(lic):
            print("The VIRL license file specified does not exist.\n")
            sys.exit(1)

        # Make sure it ends with .pem
        if not lic.endswith('.pem'):
            print("The VIRL license file must end in \".pem\".\n")
            sys.exit(1)

        #Add the license_file to cloud_config
        cloud_config += ("license_file: " + arguments['-l'] + "\n")

        # Add the license PEM to cloud_config.  Read a line at a time
        # and indents so we get proper YAML multi-line data.

        cloud_config += "license_pem: |\n"

        with open(arguments['-l'], "r") as pem:
            for line in pem:
                cloud_config += ("  " + line)


    # If we have cloud-config data add it to api_data
    if arguments['-v'] or arguments['-u'] or arguments['-g'] or arguments['-l']:
        api_data.update({"userdata" : cloud_config})

    # Convert api_data to a proper JSON-compatible double-quoted format
    
    with open(arguments['-o'], "w") as jo:
      jo.write(json.dumps(api_data))

 
    sys.exit(0)


