#!/usr/bin/env python3
import socket,struct,textwrap,os
from datetime import datetime
import matplotlib.pyplot as plt

def find_pack():
	conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
	broadcast = 0
	count = 0
	future = (datetime.now().second + 2) % 60
	while True:
		raw_data, addr = conn.recvfrom(65536)
		dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
		if dest_mac == 'FF:FF:FF:FF:FF:FF':
			broadcast += 1
		if dest_mac!='00:00:00:00:00:00' and src_mac!='00:00:00:00:00:00':
			count += 1
		
		print('Destination: {}, Source:{}, broadcast: {}'.format(dest_mac, src_mac, broadcast),end='\r')
		if datetime.now().second >= future:
			return (broadcast/count) * 100


# unpack ethernet frame
def ethernet_frame(data):
    dest_mac, src_mac, proto = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac), get_mac_addr(src_mac), socket.htons(proto), data[13:]

# return properly formatted MAC address
def get_mac_addr(bytes_addr):
    bytes_str = map('{:01x}'.format, bytes_addr)
    return ':'.join(bytes_str).upper()


fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()
i = 0
x, y = [], []

try:
	while True:
		
		x.append(i)
		y.append(find_pack())
		ax.plot(x, y, color='b')
		fig.canvas.draw()
		ax.set_xlim(left=max(0, i-50), right=i+50)
		i += 5
except KeyboardInterrupt:	
	plt.close()
	exit()
