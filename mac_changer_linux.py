#!usr/bin/env python3
# This is a program that changes the MAC Address of any Linux Distro.
# MAC stands for Media Access Control.
# Pattern for execution: [Python version] [Program name] --interface[]  --mac[]
# Example: Python3 mac_changer_linux.py --interface eth0 --mac 00:11:22:33:44:55
#  OR
# Example: Python3 mac_changer_linux.py -i eth0 -m 00:11:22:33:44:55

import subprocess # This Library helps us to execute OS Specific Commands.
import optparse   # This Library helps us to handle User Options and Parameters.
import re         # This Library helps us to work with Regular Expressions.

# Function to get the parameters from the user.
def get_user_parameters():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Enter interface to change its value")
    parser.add_option("-m", "--mac", dest="mac_address", help="Enter value for New MAC")
    (options, arguments) =  parser.parse_args()

    if not options.interface and not options.mac_address:
        parser.error("Please specify an interface and the new MAC, use --help for more info.")
    elif not options.interface:
        parser.error("Please specify an interface, use --help for more info.")
    elif not options.mac_address:
        parser.error("Please specify the new MAC, use --help for more info.")
    return options

# Function that does the  actual job (Changing the MAC). 
def mac_changer(interface, mac_address):
    print("[+] Changing MAC Address of " + interface + " to " + mac_address)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])

# Function that gets the user's current MAC Address.
def get_current_mac(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    mac_adddress_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_adddress_search_result:
        return mac_adddress_search_result.group(0)
    else:
        print("[-] Could not read MAC Address")

options     = get_user_parameters()
current_mac = get_current_mac(options.interface)
print("Your current MAC Address is " + current_mac)
mac_changer(options.interface, options.mac_address)
current_mac = get_current_mac(options.interface)

# Comparing current MAC address after function execution.
if current_mac == options.mac_address:
    print("[+] Your MAC address was changed successfully")
else:
    print("[-] Your MAC Address was not changed.")


