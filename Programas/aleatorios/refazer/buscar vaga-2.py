from bs4 import BeautifulSoup
import requests
import re

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
    print(nomes, links)
    associacoes = {}
    print(f"associando nomes aos links...\n{associacoes}")
    for i in range(len(nomes)):
        print(i)
        for j in range(len(nomes[i])):
            associacoes[nomes[i][j]] = links[i]
    return associacoes
def fundir_dados():
    nomes_totais = []
    links_totais = []
    for i in range (1,5):
        nomes_pagina = nomes_vagas(i)
        links_pagina = links_vagas(f"{base_url}/page/{i}")
        nomes_totais += nomes_pagina
        links_totais += links_pagina
    associar = associar_nome_link(nomes_totais, links_totais)
    return associar
print(fundir_dados())