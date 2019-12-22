#!/usr/bin/env python3

import nmap,sys

nm_scan = nmap.PortScanner()
print("\n Running \n")

nm_scanner = nm_scan.scan(sys.argv[1],'80',arguments = '-O')

host_is_up = "The host is:" +nm_scanner['scan'][sys.argv[1]]['status']['state']+".\n"
port_open = "The port 80 is:" + nm_scanner['scan'][sys.argv[1]]['tcp'][80]['state']+".\n"
method_scan = "The method of scan is " + nm_scanner['scan'][sys.argv[1]]['tcp'][80]['reason']+".\n"
print(port_open)
