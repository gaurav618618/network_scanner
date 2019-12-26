#!/usr/bin/env python3

import socket,struct,textwrap,os

def main():
	conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
	broadcast = 0
	while True:
		raw_data, addr = conn.recvfrom(65536)
		dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
		if dest_mac == 'FF:FF:FF:FF:FF:FF':
			broadcast += 1
		
		print('Destination: {}, Source:{}, broadcast: {}'.format(dest_mac, src_mac, broadcast),end='\r')


# unpack ethernet frame
def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[13:]

# return properly formatted MAC address
def get_mac_addr(bytes_addr):
    bytes_str = map('{:01x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()

main()
