import platform,psutil
import cpuinfo
import subprocess
import csv

def get_os():
    sistema = []

    sistema = platform.system()
    winver = platform.win32_ver(release='')
    edition = platform.win32_edition()

    os = f"{sistema} {winver[0]} {edition}"
    return os

def get_hardware():
    info = cpuinfo.get_cpu_info()
    processador = info['brand_raw']
    RAM = info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))
    return f"processador: {processador}\nRAM:{RAM}GB"
# print(get_os())
# print(get_hardware())

# Nome do computador
#host = platform.node()
# print(host)
infodosistema = subprocess.check_output(["systeminfo","/FO","csv"])
print(str(infodosistema))
with open('systeminfo.csv', encoding='utf-8') as csvfile:

    csv.writer(csvfile, delimiter=',').writerow(["joão","30"])


