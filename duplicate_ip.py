#!/usr/bin/env python3

import os
def find_duplicate():
	cmd = 'arp-scan -l > arp.txt'
	os.system(cmd)
	find_ip = 'grep -o -E "([0-9]{1,3}[\.]){3}[0-9]{1,3}" arp.txt > ip.txt'
	os.system(find_ip)
	find_mac = "grep -o -E '[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}$' arp.txt > mac.txt"
	os.system(find_mac)
	ip_file = open("ip.txt","r")
	mac_file = open("mac.txt","r")
	contents_ip = ip_file.readlines()
	contents_mac = mac_file.readlines()
	
	ip_dict={}
	mac_dict={}
	count = 0
	for ip in contents_ip:
		if ip[:len(ip)-1] in ip_dict:
			ip_dict[ip[:len(ip)-1]] = 'duplicate'
		else:
			ip_dict[ip[:len(ip)-1]] = 'unique'
		mac_dict[contents_mac[count][:len(contents_mac[count])-1]] = ip[:len(ip)-1]
		count += 1

		
	ip_file.close()
	mac_file.close()
	print(ip_dict)
	print(mac_dict)

find_duplicate()


