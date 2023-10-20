#!/usr/bin/env python3

import scapy.all as scapy
import subprocess
import optparse
import re


def search_ip():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Return list of IPs in the range")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an valid range of IP, use --help for more info")
    return options

def get_search():
    search_result = re.search("\w\w\w.\w\w\w.\w\w.\w.\w\w")
print()
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_lists = []

    for element in answered_list:
        client_dict ={"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_lists.append(client_dict)
    return clients_lists

def print_result(results_lists):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_lists:
        print(client["ip"] + "\t\t" +client["mac"])

options = search_ip()

current_mac = get_current_mac(options.target)
print("Current MAC = " + str(current_mac))

scan_result = scan("192.168.47.2/24")
print_result(scan_result)