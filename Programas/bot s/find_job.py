#objetivo: encontrar pelo tipo certo de trabalho
import find_image
import pyperclip
import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import pyautogui
import time
# puxar todas as urls do site
def abrir_codigofonte():
    webbrowser.open("https://sproutgigs.com/jobs.php")
    time.sleep(2)
    pyautogui.keyDown("ctrl")
    pyautogui.press("u")
    pyautogui.keyUp("ctrl")
links = []

def find_links():
    coordenadas = find_image.click_on_image("imagens\\href link.png", True)
    pyautogui.rightClick(coordenadas)
    time.sleep(2)
    find_image.click_on_image("imagens\\copy link.png")
    colar = pyperclip.paste()
    if not colar in links:
        links.append(colar)
        print(links)
        time.sleep(2)
        find_image.click_on_image("imagens\\next search.png")
    else:
        print("coordenadas não acharam o link certo: ", coordenadas)
# tentativas = 10
# while tentativas != 0:
#     time.sleep(1)
#     find_links()
#     tentativas -= 1
#
def nova_tentativa():
    pyautogui.keyDown("ctrl")
    pyautogui.press("a")
    pyautogui.press("c")
    pyautogui.keyUp("ctrl")
    html = pyperclip.paste()
    r = '"/jobs/submit-task\.php\?Id=([^"]+)"'
    correspondencias = re.findall(r, html)
    # O resultado será uma lista de IDs encontrados nos links
    links = []
    for id in correspondencias:
        print("ID encontrado:", id)
        links.append(f"https://sproutgigs.com/jobs/submit-task.php?Id={id}")
    return links
time.sleep(3)
nova_tentativa()
# abrir link por link
def filtro2():
    pass

# e verificar se tem o trabalho que eu quero
# salvar o link do trabalho.