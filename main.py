import time

import Config
from PyTGlu import PyTglu
from UniPy import Unifier
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument("-S", type=str, required=True,
#                    help="Please enter the site ID for the unifi site that you wish to get devices for")#
#8clj6gqlargs = parser.parse_args()

py = PyTglu(api=Config.ItgCreds.ITG_API, url=Config.ItgCreds.ITG_URL)
u = Unifier(host=Config.UnifiCreds.host, port=Config.UnifiCreds.port, user=Config.UnifiCreds.username,
            password=Config.UnifiCreds.password)

DEVICE_TYPES = {
    'uap': "1539382506324161",
    'ubb': "1539382506324161",
    'usw':  "1539382499475623",
    'ugw':  "1539382499279014"
                }


def make_serials(mac):
    serials = []
    new_string = ""
    for char in mac:
        if char == ':':
            pass
        else:
            new_string = new_string+char
    # print(new_string)
    serials.append(new_string)
    capital_new_string = ''
    for char in new_string:
        capital_new_string = capital_new_string + char.capitalize()
    serials.append(capital_new_string)
    serials.append(mac)
    capital_mac = ''
    for char in mac:
        capital_mac = capital_mac + char.capitalize()
    serials.append(capital_mac)
    print(serials)
    return serials


def main():

    # Get devices from unifi related to the site specified in the command line
    global location, organisation
    dev_ID = input("[?] Please enter the Unifi site identifier :")
    devices = u.get_devices(dev_ID)

    # Handle no devices
    if len(devices)<1:
        print("[!] ERROR : No devices found for this site : \n Exiting in 5 seconds")
        time.sleep(5)
        return -1

    # Handle devices
    else:
        print(f"[-] {len(devices)} Devices discovered :")
        print(f"[-]"*50, "\n")
        for d in devices:
            print(f"[-] {d['model']}\n")

        # Get the name of the ITGlue organisation relating to the unifi site
        name = input(f"[-] Please enter the name of the ITGlue organisation relating to the unifi site {dev_ID}: ")

        # Search itg organisations for the organisation specified
        orgs = py.getOrganisations()['data']

        # the length of possible matches determines if a match has been found and if it is a perfect match or a group of possible matches
        possible_matches = []
        for o in orgs:
            # if we find an exact match assign it to possible matches and break the loop
            if name.capitalize() == str(o['attributes']['name']).capitalize():
                possible_matches.append(o)
                print(f"match found for {name}")
                break

        # if no match is found
        # length of possible matches will be less than one
        if len(possible_matches)<1:

            # set test string
            if len(name) > 5:
                test_string = name[:3].capitalize()
            else:
                test_string = name.capitalize()

            # Search for possible matches
            for o in orgs:
                if str(o['attributes']['name']).capitalize().startswith(test_string):
                    possible_matches.append(o)

        # If there are still no matches found
        # Length of possible matches will be less than one
        if len(possible_matches)<1:

            # offer another attempt
            print("[!!] WARN: No matching organisations found!")
            again = input("[-] Would you like to try again? y/n ? : ")

            # if yes regress
            if again.capitalize() == "Y":
                main()

            # If no exit
            else:
                return -1

        # Length of possible_matches is more than 0
        # Display possible matches for selection by the user
        else:
            print(f"{len(possible_matches)} Possible matches found. \n")
            for p in possible_matches:
                print(f"[-] ({possible_matches.index(p)}) : {p['attributes']['name']}")
            organisation = None
            while not organisation:

                # Ask user to make selection
                index = input("[?] Please enter the number of the organisation to select it: ")

                # catch errors for invalid indexes
                try:
                    if int(index) < len(possible_matches):
                        organisation = possible_matches[int(index)]
                    else:
                        print("[!!] WARN: Selection out of bounds")
                except Exception as e:
                    print(f"[!!] ERROR: INDEX INVALID")
                    print(e)

            # organisation set
            print("organisation set")

            # Select Location
            locations = []
            for temp in py.getLocations(organisation['id'])['data']:
                locations.append(temp)
            location = None
            while not location:
                print(f"[?] Locations for {organisation['attributes']['name']} \n")
                for l in locations:
                    print(f"[-] ({locations.index(l)}) : {l['attributes']['name']}")
                index = input("[-] Please enter the number for the location you would like to use : ")
                try:
                    if int(index) < len(locations):
                        location = locations[int(index)]
                    else:
                        print("[!!] WARN: Selection out of bounds")
                except Exception as e:
                    print(f"[!!] ERROR: INDEX INVALID")
                    print(e)

        device_contexts = []

        # Build device context for each device
        for device in devices:
            context = py.buildITGConfigurationContext(name=device['name'],
                                                      config_type=DEVICE_TYPES[device['type']],
                                                      contactId=None,
                                                      ip=device['ip'],
                                                      mac=device['mac'],
                                                      serial_number=make_serials(device['mac'])[0],
                                                      installed_at=location['attributes']['name'],
                                                      organisation_id=organisation['id'],
                                                      location_id=location['id'])
            print(context)
            device_contexts.append(context)

        # Validate request to upload
        upload = input("\n[-] Context created for devices Would you like to upload? y/n :")
        if upload.capitalize() == "Y":
            for d in device_contexts:
                py.setConfigurations(organisation_id=organisation['id'], context=d)
        else:
            f = open("output.txt", 'w')
            for d in device_contexts:
                f.write(d)
                f.write("\n")
            f.close()
            print("[-] Contect output to file : output.txt in the application path. exiting")
            return 0
main()
