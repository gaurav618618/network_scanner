#!/usr/bin/env python3
import socket,struct,textwrap,os
import time
import matplotlib.pyplot as plt
from networking.ipv4 import IPv4

from networking.icmp import ICMP
from networking.tcp import TCP

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

def find_pack():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    broadcast = 0
    multicast = 0
    unicast = 0
    count = 0
    future = time.time() + 5
    while True:
        raw_data, addr = conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        if dest_mac == 'FF:FF:FF:FF:FF:FF':
            broadcast += 1
        elif dest_mac[:2] == '01':
            multicast += 1
        else:
            unicast += 1
        if dest_mac!='00:00:00:00:00:00' and src_mac!='00:00:00:00:00:00':
            count += 1
        print('Destination: {}, Source:{}, broadcast: {},total : {}'.format(dest_mac, src_mac, broadcast,count))
        #IPV4
        if eth_proto == 8:
            ipv4 = IPv4(data)
            # ICMP
            if ipv4.proto == 1:
                icmp = ICMP(ipv4.data)
            # TCP
            elif ipv4.proto == 6:
                tcp = TCP(ipv4.data)
        if len(data) < 1:
            print(TAB_2 + 'No ehternet data')
        if time.time() >= future:
            brod_res = (broadcast/count) * 100
            multi_res = (multicast/count) * 100
            uni_res = (unicast/count) * 100
            return [brod_res,multi_res,uni_res]


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
x, y, z, w = [], [], [], []

try:
	while True:
            x.append(i)
            rn_res = find_pack()
            y.append(rn_res[0])
            z.append(rn_res[1])
            w.append(rn_res[2])
            ax.cla()
            ax.plot(x, y, label='broadcast')
            ax.plot(x, z, label='multicast')
            ax.plot(x,w, label='unicast')
            ax.legend(loc = 'upper right')
            fig.canvas.draw()
            ax.set_xlim(left=max(0, i-50), right=i+50)
            i += 5
except KeyboardInterrupt:	
	plt.close()
	exit()
