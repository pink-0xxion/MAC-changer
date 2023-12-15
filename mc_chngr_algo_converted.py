#!/usr/bin/python3
import subprocess
import optparse     #when its grey means optparse is not impemented <--SEE-IT
import re

def get_arguments():
		parser = optparse.OptionParser() 
		parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
		parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
		(options, arguments) = parser.parse_args()   #returning (options, arguments) 
		if not options.interface:
			parser.error("[-] Please specify an interface, use --help for more info.")  #we can also using print() and exit to exit the program
		elif not options.new_mac:
			parser.error("[-] Please specify an new mac, use --help for more info.")
		return options     #SEE-HERE, returning only options not arguments as there is need of options only in chaange_mac(), as it contains 2 values(SEE-IT) if this ran means user entered all correct

def change_mac(interface, new_mac):				#function defination
		print("[+] Changing MAC address for " + interface + " to " + new_mac)
		subprocess.call(["ifconfig", interface, "down"])
		subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
		subprocess.call(["ifconfig", interface, "up"])	

def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface])  #return the result of (ifconfig eth0) to variable ifconfig_result
	#print(ifconfig_result)  #to check its working fine

	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))  # r for RULE, re.search returns the array of matched patterns
	#print(mac_address_search_result.group(0))
	if mac_address_search_result:				# if re.search does not return any matches it will give error that only prgrmer can understnd so we r doing this for showing custom error message
		return mac_address_search_result.group(0)   # as mac_address_search_result can contain more than one match we are interested in first match, becarefull see there "group(0)"
	else:
		print("[-] Could not read MAC address.")	#if suppose user entered interface=lo and lo don't have MAC address

options = get_arguments()  #here only one variable as we only return one variable from get_arguments()

current_mac = get_current_mac(options.interface) 	#options.interface=eth0=interface
print("Current MAC = " + str(current_mac))			#type conversion/casting of current_mac as it can be NOTHING as well when it contain nothing so we are making it string so to concanate and avoid error, result: Current MAc = None

change_mac(options.interface, options.new_mac)     #function call

current_mac = get_current_mac(options.interface)	# here current_mac is over written with changed MAC address
if current_mac == options.new_mac:
	print("[+] MAC address was successfully changed to " + current_mac)
else:
	print("[-] MAC address did not get changed.")
