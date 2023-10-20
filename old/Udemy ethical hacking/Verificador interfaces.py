import ifcfg
for nome, interface in ifcfg.interfaces().items():
    print(interface['device'])
    print(interface['inet'])
    print(interface['inet4'])
    print(interface['inet6'])
    print(interface['netmask'])
    print(interface['broadcast'])
    print(interface['broadcasts'])
