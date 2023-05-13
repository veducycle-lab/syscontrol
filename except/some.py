import nmap
import networkx as nx
import socket
import pystray

# Пример использования библиотеки nmap
nm = nmap.PortScanner()
nm.scan('192.168.0.1/24')
for host in nm.all_hosts():
    print('Host : %s (%s)' % (host, nm[host].hostname()))

