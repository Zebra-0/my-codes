from urllib.request import urlopen
#import time
#import threading
#import pyperclip


def titulo(url: str):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    title_index = html.find("<title>")
    start_index = title_index + len("<title>")
    end_index = html.find("</title>")
    title = html[start_index:end_index]
    if "- YouTube" in title:
        try:
            full_title = title.replace(" - YouTube", "")

        except:
            full_title = title.replace("- YouTube", "")

    return str(full_title)

# verificar por ytd-playlist-panel-renderer mix
# ytd-playlist-panel-video-renderer
def get_mix(url):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    title_index = html.find("<ytd-playlist-panel-video-renderer")
    start_index = title_index + len("<ytd-playlist-panel-video-renderer")
    end_index = html.find("</ytd-playlist-panel-video-renderer>")
    mix = html[start_index:end_index]
    #mix.find()
    print(mix)
#get_mix("https://www.youtube.com/watch?v=i4AXVFggAnk&list=RD3AnkfFcYxTw&index=2")
# print(titulo("https://youtu.be/NHffhGkpgFAA?list=RDAHukwv_VX9A"))
#href="/watch?v=3AnkfFcYxTw&list=RD3AnkfFcYxTw&index=1&pp=8AUB"
from bs4 import BeautifulSoup

html = """https://www.youtube.com/watch?v=i4AXVFggAnk&list=RD3AnkfFcYxTw&index=2"""

# Crie um objeto BeautifulSoup a partir do HTML
soup = BeautifulSoup(html, 'html.parser')

# Encontre o elemento com a classe específica
playlist_items = soup.find('ytd-playlist-panel-video-renderer', class_='style-scope ytd-playlist-panel-renderer')

# Encontre todos os elementos 'a' dentro do elemento encontrado
links = playlist_items.find_all('a')

# Itere sobre os links e imprima seus atributos href
for link in links:
    print(link.get('href'))