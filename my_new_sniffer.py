import socket,struct
import time
import matplotlib.pyplot as plt
from general import *
from networking.ethernet import Ethernet
from networking.ipv4 import IPv4
from networking.icmp import ICMP
from networking.tcp import TCP

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '


def main():
    #pcap = Pcap('capture.pcap')
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    prob_ip = {}
    rset = 0
    no_data = 0
    syn_flg = 0
    total = 0
    end = time.time() + 5	
    while True:
        raw_data, addr = conn.recvfrom(65535)
        eth = Ethernet(raw_data)
        total += 1 
        
        print('\nEthernet Frame:')
        print(TAB_1 + 'Destination: {}, Source: {}, Protocol: {}'.format(eth.dest_mac, eth.src_mac, eth.proto))

        # IPv4
        if eth.proto == 8:
            ipv4 = IPv4(eth.data)
            # ICMP
            if ipv4.proto == 1:
                icmp = ICMP(ipv4.data)

            # TCP
            elif ipv4.proto == 6:
                tcp = TCP(ipv4.data)
                if tcp.flag_rst == 1:
                    rset += 1
                else :
                    rset += 0
                    
                    if ipv4.target in prob_ip:
                        prob_ip[ipv4.target] += 1
                    else :
                        prob_ip[ipv4.target] = 1
                 



                if len(tcp.data) > 0:
                    print(TAB_2 + 'Data is present')
                else :
                    no_data += 1
                    print(TAB_2+'No TCP DATA')

        if time.time() >= end :

            rset_p = (rset/total)*100 
            print('--------------------------------------------------- Return -------------------------------')
            no_data_p = ((no_data)/total)*100
            return [no_data_p,rset_p]



fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()
i = 0
x, y, z = [], [],[]

try:
	while True:
            x.append(i)
            j = main()
            y.append(j[0])
            z.append(j[1])
            ax.cla()
            ax.plot(x, y, label='No Data')
            ax.plot(x, z, label='Reset packets')
            ax.legend(loc = 'upper right')
            fig.canvas.draw()
            ax.set_xlim(left=max(0, i-50), right=i+50)
            i += 5
except KeyboardInterrupt:	
	exit()
