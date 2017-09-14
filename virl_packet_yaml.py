#!/usr/bin/env python3

"""Create userdata for use in deploying VIRL via the Packet portal.

Usage:
  virl_packet_yaml -o OUTPUT_FILE [ -v VIRL_PW ] [ -u UWM_PW ] [ -g GUEST_PW ] [ -l LICENSE_FILE ] 

Arguments:
  -o <OUTPUT_FILE>      The output file
  -s <SERVER_NAME>      The desired system / server name.

Options:

  -v VIRL_PW            VIRL account password
  -u UWM_PW             UWM account password.
  -g GUEST_PW           Guest account password.
  -l LICENSE_FILE       License file (format: id.domain.tld.pem)

"""

import sys
import os
from docopt import docopt

# Let's get started
if __name__ == '__main__':
	arguments = docopt(__doc__, version='1.0.0rc3')

	# See if we have anything to do.  If so build the cloud-config / userdata.
	if arguments['-v'] or arguments['-u'] or arguments['-g'] or arguments['-l']: 

		# Open our output file.
		with open(arguments['-o'], "w") as yo:

		# Write our cloud-config marker
			yo.write("#cloud-config\n\n")

			# If we have a VIRL login password what is it?
			if arguments['-v']:
				yo.write("virl_password: " + arguments['-v'] + "\n\n")

			# If we have a UWM account password what is it?
			if arguments['-u']:
				yo.write("uwm_password: " + arguments['-u'] + "\n\n")

			# If we have a Guest account password what is it?
			if arguments['-g']:
				yo.write("virl_password: " + arguments['-v'] + "\n\n")

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
				yo.write("license_file: " + arguments['-l'] + "\n\n")        

				# Add the license PEM to cloud_config.  Read a line at a time
				# and indent so we get proper YAML multi-line data.

				yo.write("license_pem: |\n") 

				with open(arguments['-l'], "r") as pem:
					for line in pem:
						yo.write("  " + line)

	else:

		# Nope, Nothing to do.
		print("No arguments were provided so there's nothing to do.")

	# Done.

	sys.exit(0)


