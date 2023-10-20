import platform,socket,psutil
def verificarSistema():
    info={}
    info['plataforma']=platform.system()
    info['platforma-release']=platform.release()
    info['platforma-versao']=platform.version()
    info['arquitetura']=platform.machine()
    info['hostname']=socket.gethostname()
    info['processador']=platform.processor()
    info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))
    print(info)

verificarSistema()
machine = input(str("insira o nome da máquina:"))