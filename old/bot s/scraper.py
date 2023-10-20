
from urllib.request import urlopen
import bot4
import pyperclip
from bs4 import BeautifulSoup
import requests
import re
import html
import webbrowser
import os
from loguru import logger

def extract_site(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    bonito = soup.prettify()
    expressoes_regulares = [r'href="https://bit.ly/([^"]+)"', r'href="https://www.google.com/search.?q=(.*?)"']
    #expressoes_regulares2 = {r'href="https://bit.ly/([^"]+)"': "https://bit.ly/",}
    for padrao in expressoes_regulares:
        correspondencia = re.search(padrao, html)
        if correspondencia:
            link = correspondencia.group(1)
            logger.debug("Link encontrado com a expressão regular:" + padrao)
            if "bit.ly" in padrao:
                link = "https://bit.ly/" + link
            logger.debug("Link encontrado:", link)
            break
    else:
        logger.debug("Nenhuma correspondência encontrada com as expressões regulares.")

def melhores_links(url_link):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
        #expressao = f'href="{url_link}(.*?)./"'
        response = requests.get(url_link, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        #bonito = soup.prettify()
        #link = re.findall(expressao, bonito)
        #link = soup.findall('a')['href']
        links = soup.find_all('a')
        #print(links)
        melhores = []
        # Extraia os URLs associados a esses elementos
        for link in links:
            url = link.get('href')
            #melhores.append(url)
            if "/category/" in url or "page" in url:
                continue
            elif url in melhores:
                continue
            elif not "https://" in url:
                continue
            elif "wp-admin" in url:
                continue
            else:
                melhores.append(url)

            #print("Link encontrado:", url)
        #melhores = melhores.pop(url)
        #print(melhores)
        return melhores
    except:
        logger.debug('falha ao encontrar os melhores links')

def procurar_contato():
    try:

        # Abra o arquivo txt
        with open("exemplos.txt", "r") as f:
            # Leia cada linha do arquivo
            linhas = f.readlines()
        # Crie uma lista para armazenar os exemplos
        exemplos = []

        # Adicione cada exemplo à lista
        for linha in linhas:
            if not linha in exemplos:
                exemplos.append(linha.rstrip("\n"))
            else:
                continue
        # Imprima a lista
        return exemplos
    except:
        logger.debug('falha ao encontrar o contato')
def procurar_correspondencia(url_link):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    padrao = r'href="([^"]+)"'
    exemplos = procurar_contato()
    if not 'https://' in url_link:
        url_link = 'https://' + url_link + '/'
    #print(url_link)
    response = requests.get(url_link, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    #bonito = soup.prettify()
    #link = re.findall(expressao, bonito)
    #link = soup.findall('a')['href']
    links = soup.find_all('a')
    #print(links)
    resultado = []
    try:
        for link in links:
            #print(link)
            url = link.get('href')
            #print(url)
            if url == None:
                continue
            elif url in resultado:
                continue
            #elif not "https://" in url:
            #    continue
            else:
                for contato in exemplos:
                    if contato in url and url not in resultado:
                        #print(url)
                        #print(contato)
                        resultado.append(url)
                        #print(resultado)
                        if not 'https://' in resultado[0]:
                            resultado[0] = url_link + resultado[0]
        return resultado[0]
    except Exception as erro:
        logger.debug("sem página de contato -- verifique manualmente.\n", erro)
        return 'Verificar'
#print(procurar_correspondencia('https://software.com.br'))
def pegar_url_principal_apenas(link):
    if "https://" in link:
        link = link.replace('https://', '')
        barra = link.find('/')
        return link[:barra]
    else:
        barra = link.find('/')
        return link[:barra]
def procurar_jobs(texto):
    padrao = r'href="([^"]+)"'
    soup = BeautifulSoup(texto, 'html.parser')
    links = soup.find_all('a')
    lista = []
    for link in links:
        print(link)
        if not 'Go to job' in link:
            url = link.get('href')
            if "Id" in url:
                print(f'------------------------- url id\n{url}')
                lista.append("https://sproutgigs.com" + url)

    return lista
def extrair_codigo(codigo):
    ''' Extrai o codigo apenas da página da sproutgigs '''
    #codigo = pyperclip.paste()
    try:
        dica = re.search(r'Hint: ........', codigo)
        dica = dica.group(0)
        dica = dica.replace('Hint: ', '')
        return dica
    except:
        pass
        #dica = re.search(r'**.', codigo)
        #dica = dica.group(0)

def instrucoes(texto):
    instrucoes_tratadas = []
    try:
        for instrucao in re.findall(r'<li class="py-1">(?P<instrucao>.*?)</li>', texto):
            instrucao_tratada = instrucao.strip().replace('<br />', '\n')
            instrucoes_tratadas.append(instrucao_tratada)

        relacao = {1: instrucoes_tratadas[0],
                   2: instrucoes_tratadas[1],
                   3: instrucoes_tratadas[2],
                   4: instrucoes_tratadas[3],
                   5: instrucoes_tratadas[4],
                   6: instrucoes_tratadas[5],
                   }
        return relacao
    except Exception as e:
        logger.debug("trabalho não reconhecido. indo para o próximo")
        return False
def find_code_hint(html_code, code_length):
  """
  Encontra a dica de um código em HTML.

  Args:
    html_code: O código HTML que contém o código a ser analisado.
    code_length: O comprimento do código, incluindo os caracteres ocultos.

  Returns:
    A dica do código, ou None se não for encontrada.
  """

  # Encontra todas as ocorrências do código no HTML.
  code_occurrences = re.findall(r"<code>(.*?)</code>", html_code)

  # Itera sobre as ocorrências do código, procurando pela dica.
  for code_occurrence in code_occurrences:
    code = code_occurrence.strip()

    # Se o código tiver o comprimento esperado, então é possível que seja o código correto.
    if len(code) == code_length:
      # Tenta encontrar o início do código oculto.
      start_of_hint = code.find("*")

      # Se o início do código oculto for encontrado, então o código é o correto.
      if start_of_hint != -1:
        return code[:start_of_hint]

  return None

def pegar_url_principal_apenas2(html_code):
    """
    Pega apenas o link principal da página.

    Args:
        html_code: O código HTML da página.

    Returns:
        O link principal da página.
    """

    # Encontra a tag `<a>` com o atributo `href` mais próximo do início da página.
    main_link_tag = next(
        tag for tag in BeautifulSoup(html_code, "html.parser").find_all("a")
    )

    # Pega apenas a parte da URL sem os parâmetros.
    main_link = main_link_tag["href"]
    corresponde = re.search(r"(https://[^/]+)/", main_link)
    return corresponde.group()


