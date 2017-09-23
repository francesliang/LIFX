### This script requires arp-scan to be installed on host machine

import os, sys
from subprocess import Popen, PIPE
import socket 


def list_net_devices(ip_prefix):
	'''
	ip_prefix is the prefix of the local network IP address, e.g: 10.0.0.x
	'''
	process = Popen(['arp-scan', '-l'], stdout=PIPE)
	output, err = process.communicate()

	res = []
	if err is None:
		outputs = output.split('\n')
		for out in outputs:
			if not out.startswith(ip_prefix):
				continue
			ip, mac, name = out.split('\t')
			res.append((ip, mac, name))

	return res


def check_device_in_net(mac_addr):
	local_ip = get_local_ip()
	ip_prefix = local_ip.rpartition('.')[0]
	print 'ip prefix', ip_prefix
	device_list = list_net_devices(ip_prefix)

	all_mac_addr = [i[1] for i in device_list]
	print 'all mac address', all_mac_addr

	return (mac_addr in all_mac_addr)


def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	return s.getsockname()[0]