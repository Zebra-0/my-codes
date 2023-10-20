from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

base_url = "https://rjempregos.net/vagas/home-office/"
base_url_vaga = "https://rjempregos.net/vagasrio/"
header = "h2"


def request_data(link):
    response = requests.get(link)
    try:
        if response.status_code == 200:
            print("Acessando página... Colhendo informações")
    except:
        print("Pagina fora do ar ou link inválido")
    # print(f"resposta: {response}")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def url(link, find_header):
    soup = request_data(link)
    titles = soup.find_all(find_header)
    print("Organizando headers...")
    nomes_vagas = []
    blacklist = ['Navegação por posts', 'Ultimas Notícias', 'Veja Todas as Notícias']
    for title in titles:
        if not title.text in blacklist:
            nomes_vagas.append(title.text)
    return nomes_vagas

def nomes_vagas(num_da_pagina):
    vagas = []
    if num_da_pagina == 1:
        vagas.append(url(base_url, header))
        #print(vagas)
    else:
        url_pagina = f"{base_url}/page/{num_da_pagina}/"
        vagas.append(url(url_pagina, header))
        #print(vagas)
    return vagas
def links_vagas(link):
    data = request_data(link)
    links = data.find_all("a", href=re.compile(f"^{base_url_vaga}"))
    print("Organizando links...")
    bau = []
    for link in links:
        #print(link["href"])
        if not link["href"] in bau:
            bau.append(link["href"])
    #print(bau)
    return bau
def associar_nome_link(nomes, links):
    associacoes = {}
    print("associando nomes aos links...")
    for i in range(len(nomes)):
        for j in range(len(nomes[i])):
            associacoes[nomes[i][j]] = links[i]
    return associacoes


# for num_da_pagina in range(1, 169):
#     nomes_vagas(num_da_pagina)
nomes = nomes_vagas(1)
links = links_vagas(base_url)
associar = associar_nome_link(nomes, links)
print(associar)
