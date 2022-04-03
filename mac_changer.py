#!usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="your MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use -h or --help for more information")
    elif not options.new_mac:
        parser.error("[-] Please specify a mac adress you want to change to, use -h or --help for more information")

    return options

def change_mac(interface, new_mac):
    str(new_mac)
    print("[+] Changing the MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_shearch_result = re.search(br"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_shearch_result:
        return mac_address_shearch_result.group(0)
    else:
        print("[-] Could not find MAC address")

# Checking your MAC
options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))

# Changing & checking your new MAC
change_mac(options.interface, options.new_mac)
new_mac = options.new_mac
current_mac = get_current_mac(options.interface)
if current_mac == new_mac:
    print("[+] MAC address was successfully changed to " + new_mac)
else:
    print("[-] MAC address did not get changed")
