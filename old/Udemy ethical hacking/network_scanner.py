#!/usr/bin/env python3

import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_lists = []


    for element in answered_list:
        client_dict ={"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_lists.append(client_dict)
        # print(element[1].psrc + "\t\t" + element[1].hwsrc)
    return clients_lists
    # print(answered_list.summary())

def print_result(results_lists):
    print("IP\t\t\tMAC Address\n-----------------------------------------")
    for client in results_lists:
        print(client["ip"] + "\t\t" +client["mac"])

scan_result = scan("192.168.47.2/24")
print_result(scan_result)