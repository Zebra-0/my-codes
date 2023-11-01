import ftfy
import requests
import time
import json
from bs4 import BeautifulSoup
import re
import threading
from loguru import logger
def get_html(link):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    resposta = requests.get(link, headers=headers)
    resposta = resposta.text
    return resposta
def links_in_html(link, filtro=None):
    html = get_html(link)
    sopinha = BeautifulSoup(html, 'html.parser')
    links = sopinha.find_all('a')
    resultados = []
    for item in links:
        url = item.get('href')
        if not url in resultados:
            if filtro:
                if filtro in url:
                    resultados.append(url)
            else:
                resultados.append(url)
    return resultados
def resumir(html, max_words=16):
    """Pega o HTML da página e resume a descrição e o link de candidatura."""
    # vagas = links_in_html(link, filtro='/vagasrio/')
    # vaga = get_html(vagas[0])# até aqui é apenas para teste
    vaga = html
    find1 = vaga.find('Descrição da vaga')
    find2 = vaga.find('Vaga divulgada')
    vaga = vaga[find1:find2]
    link_pattern = 'href="([^"]+)"'
    link_vaga = re.search(link_pattern, vaga)
    link_vaga = link_vaga.group(0)
    link_vaga = link_vaga[+6:-1]
    #link = vaga.('href')
    #print(vaga)
    classe = 'class="job_description"><p>'
    find3 = vaga.find(classe)
    descricao = vaga[find3+len(classe):]
    descricao = descricao.replace('</p><p>','\n')
    descricao = descricao.replace('<br/>','\n')
    descricao = descricao.replace('</p></div><p>','\n')
    descricao = descricao.replace('\n\n','\n')
    linhas = descricao.split('\n')
    descricao = ftfy.fix_text(descricao)  # corrige possiveis erros no texto, tipo utf-8

    linhas_processadas = []

    for linha in linhas:
        palavras = linha.split()
        if len(palavras) > max_words:
            grupos = [palavras[i:i + max_words] for i in range(0, len(palavras), max_words)]
            for grupo in grupos:
                linhas_processadas.append(' '.join(grupo))
        else:
            linhas_processadas.append(linha)
    resumo = [link_vaga, descricao]
    return resumo
def vagas_from_page(link):
    #html = get_html(link)
    vagas = links_in_html(link, filtro='vagasrio/')
    dados = {}
    num_vaga = 1
    for vaga in vagas:
        #print(f'vaga:{vaga}')
        conteudo = get_html(vaga)
        #print(conteudo)
        data_horafinder = conteudo.find('>Publicado em  ')
        data_horafinder = conteudo[data_horafinder+len('>Publicado em  '):]
        data_horafinder2 = data_horafinder.find('</time>')
        data_hora = data_horafinder[:data_horafinder2]
        findsalario0 = 'class="salary">'
        findsalario2 = '</li></ul><div'
        findsalario = conteudo.find(findsalario0)
        findsalario = conteudo[findsalario+len(findsalario0):]
        findsalario2 = findsalario.find(findsalario2)
        salario = findsalario[:findsalario2]
        resumo = resumir(conteudo)
        dados[num_vaga] = {"link_vaga": vaga,
                           "link_candidatura": resumo[0],
                           "descricao": resumo[1],
                           "data-hora": data_hora,
                           "salario": salario
                           }
        num_vaga += 1
    return dados
def trabalhos(qnt_paginas=10):
    link_page = 'https://rjempregos.net/vagas/home-office/page/'
    contagem = 1
    pages = {}
    while qnt_paginas >= contagem:
        logger.debug(f'Analizando página: {contagem}')
        if contagem == 1:
            link = 'https://rjempregos.net/vagas/home-office/'
        else:
            link = f'{link_page}{contagem}/'
        vagas = vagas_from_page(link)
        pages[contagem] = vagas
        logger.success(f'Pagina {contagem} adicionada')
        contagem += 1
    save_json('vagasrio.json', conteudo=pages)
    #return pages
    #print(pages)
def background_trabalhos(timer=None, qnt_paginas=10):
    trabalhar = threading.Thread(target=trabalhos(qnt_paginas=qnt_paginas))
    trabalhar.start()
    if timer:
        time.sleep(timer)
        trabalhar.join()
def read_json(nome_arquivo):
    '''retorna os dados do json especificado.'''
    with open(nome_arquivo, 'r') as trabalhos:
        dados = json.load(trabalhos)
    return dados
def save_json(nome_arquivo, conteudo):
    #dados = read_json(nome_arquivo)
    with open(nome_arquivo, 'w', encoding="utf-8") as f:
        json.dump(conteudo, f, indent=4)

#print(get_html('https://rjempregos.net/vagasrio/desenvolvedor-php-pleno-superlogica-tecnologias-home-office/'))
#background_trabalhos()
#vagas = read_json("vagasrio.json")
#print(len(vagas["1"]))
#print(vagas["1"]["1"]['descricao'])
#link = 'https://rjempregos.net/vagas/home-office'
