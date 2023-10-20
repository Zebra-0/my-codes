"""
Esse projeto encontra sites compatíveis e faz uma garimpagem dos dados procurando pelo código e
respeitando as regras da tarefa.
Aprendi muito com esse projeto e fortaleceu alguns conhecimentos.

"""

import logging
import re
import subprocess
import pyautogui as p
import time
import json
import requests
import scraper
import pyperclip
import random
import procurar_imagem
import threading
from loguru import logger
import datetime
p.PAUSE = 1


class Comandos():
    """Comando básicos para o controle do bot."""
    def __init__(self):
        pass
    def new_key(self, id, chave, conteudo, file="dados_trabalho.json"):
        # Carregar o JSON
        with open(file, "r") as f:
            data = json.load(f)
        # Adicionar a nova chave
        ids = list(data.keys())
        if id in ids:
            # atualiza o id
            try:
                data[id].update({chave: conteudo})
            except KeyError as key:
                key = str(key).replace("'","")
                data = {f'{key}': {chave: conteudo}}
        else:
            # adiciona o id
            try:
                data[id] = {chave: conteudo}
            except Exception as erro:
                logger.error(f'não foi possivel adicinar chave :{id}\nERRO\n{erro}')
        # Salvar o JSON atualizado
        with open(file, "w") as f:
            json.dump(data, f, indent=4)
    def keys_json(self, file='dados_trabalho.json'):
        """retorna a lista com todas as chaves primárias"""
        with open(file, 'r') as trabalhos:
            dados = json.load(trabalhos)
        todas_as_chaves = list(dados.keys())
        return todas_as_chaves
    def read_json(self, nome_arquivo):
        '''retorna os dados do json especificado.'''
        with open(nome_arquivo, 'r') as trabalhos:
            dados = json.load(trabalhos)
        return  dados
    def abrir_chrome(self, anonimo=True):
        '''Coloque False para abrir a janela normal.'''
        try:
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if anonimo:
                subprocess.Popen([chrome_path, "--incognito"])
            else:
                subprocess.Popen([chrome_path])
        except Exception as e:
            print(f"Erro ao abrir a janela anônima: {e}")
    def clicar_na_url(self, digitar=None):
        """clica no campo da url no navegador padrao:tela cheia"""
        if digitar==None:
            p.click(x=600, y=49)
        else:
            p.click(x=600, y=49)
            self.selecionar_tudo('apagar')
            pyperclip.copy(digitar)
            p.hotkey('ctrl', 'v')
            p.press('enter')
    def selecionar_tudo(self, acao='copiar'):
        """Literalmente copia tudo. Mas o campo deve ser selecionado antes."""
        p.hotkey('ctrl', 'a')
        time.sleep(1)
        if acao=='copiar':
            p.hotkey('ctrl', 'c')
            return pyperclip.paste()
        elif acao=='apagar':
            p.press('backspace')
    def fechar_aba(self):
        p.hotkey('ctrl', 'w')
    def copy_source(self):
        """abre a copia o código fonte da página"""
        p.hotkey('ctrl', 'u')
        time.sleep(1)
        p.hotkey('ctrl', 'a')
        p.hotkey('ctrl', 'c')
        p.hotkey('ctrl', 'w')
        return pyperclip.paste()
    def link_id(self,link):
        """Retorna o id do link para trabalhar.."""
        id_link = link.find('Id=') + 3
        return link[id_link:]
    def salvar_trabalho(self, trabalho):
        """Salva no arquivo txt abaixo o trabalho um trabalho para filtrar depois"""
        with open("trabalhos.txt", "a") as arquivo:
            arquivo.write(trabalho + "\n")
    def ler_trabalhos(self):
        """Retorna a lista de trabalhos para o bot"""
        with open("trabalhos.txt", "r") as arquivo:
            trabalho = arquivo.readlines()
        linhas = [linha.strip() for linha in trabalho]  # remove o \n
        return linhas
    def simulate_reading_movement(self, velocidade=200, start=(500, 500), end=(1400, 800), duration=None):
        logger.debug('Iniciando leitura...')
        try:
            x_start, y_start = start
            x_end, y_end = end
            move_speed = velocidade
            start_time = time.time()
            #p.press('space',presses=6, interval=4)
            while duration is None or (time.time() - start_time) < duration:
                distance = ((x_end - x_start) ** 2 + (y_end - y_start) ** 2) ** 0.5
                move_duration = distance / move_speed
                p.moveTo(x_end, y_end, duration=move_duration, tween=p.easeInOutQuad)
                time.sleep(random.uniform(1, 3))
                p.moveTo(x_start, y_start, duration=move_duration, tween=p.easeInOutQuad)
                time.sleep(random.uniform(1, 3))
                #p.press('space', presses=1)
                #schedule.run_pending()
                y_start = y_start + 40
                y_end = y_end + 40
                #p.press('down',presses=10,interval=0.3)
            logger.success('Leitura concluída.')
        except KeyboardInterrupt:
            print("Movimento de leitura interrompido pelo usuário.")
    def run_simulation_for_x_seconds(self, tempo, funcao):
        try:
            if funcao == 'leitura':
                thread = threading.Thread(target=self.simulate_reading_movement, args=(300, (500, 500), (1400, 500), tempo))

            else:
                thread = threading.Thread(target=funcao)
            thread.start()
            time.sleep(tempo)
            thread.join()
        except Exception as erro:
            print('Erro ao rodar a função\n', erro)
        except KeyboardInterrupt:
            print('Parando de rodar a função.')
    def filtro(self):
        time.sleep(2)
        p.click(x=741, y=527)
        time.sleep(0.5)
        p.click(x=663, y=642)
        time.sleep(0.5)
        p.click(x=841, y=833)
        time.sleep(2)
    def press_space(self, intervalo=4.33, vezes=3):
        press = threading.Thread(target= lambda: p.press('space', interval=intervalo, presses=vezes))
        #press.start()
        return press
class Verificar():
    def __init__(self):
        self.dados = Comandos().read_json('dados_trabalho.json')
    def trabalhos(self):
        # todo: filtrar melhor o tipo de trabalho antes de coletar o código fonte.
        """abre o site e escanea o código fonte pelos links. depois salva em trabalhos.txt"""
        try:
            site = "https://sproutgigs.com/jobs.php"
            Comandos().abrir_chrome(anonimo=False)
            time.sleep(2)
            Comandos().clicar_na_url(site)
            time.sleep(2)
            #Comandos().filtro()
            codigo_fonte = Comandos().copy_source()
            links = scraper.procurar_jobs(codigo_fonte)
            logger.success(f'{len(links)} trabalhos encontrados.')
            for trabalhos in links:
                if trabalhos != None:
                    Comandos().salvar_trabalho(trabalhos)
        except Exception as erro:
            logging.error('erro ao verificar os links do trabalho' + erro)
    def get_dados(self,link='', parse=True, id_job=False):
        """pega os dados e filtra."""
        if parse:
            Comandos().clicar_na_url(link)
            time.sleep(3)
            dados_da_pagina = Comandos().selecionar_tudo()
            if 'Ooops! Page not found' in dados_da_pagina:
                return None
            id = Comandos().link_id(link)
            dados =  dados_da_pagina[:dados_da_pagina.find('Referral Program')]
        else:
            if id_job:
                dados = Comandos().read_json('dados_trabalho.json')
                dados = dados[id_job]['dados_job']['raw_data']
                id = id_job
        if self.bons_trabalhos(dados) and dados != None:
            Comandos().new_key(id, "dados_job", {'raw_data': dados})
            instrucoes = self.instrucoes(id)
            Comandos().new_key(id, 'instrucoes', instrucoes)
            link_tarefa = self.link_para_tarefa(id)

            Comandos().new_key(id, 'link_tarefa', link_tarefa)

            Comandos().new_key(id, 'link_job', link)
            Comandos().new_key(id, 'pendente', 'True')
            self.paginas(id)
            self.tempo(id)
            self.dica(id)
            self.hint_site(id)
            logger.success(f'adicionando trabalho compatível. Id={id}')
        else:
            if dados==None:
                logger.error('impossível recuperar os dados. dados == None')
            logger.info(f'trabalho incompatível. Id={id}')
    def verifica_codigo(self, id_site):
        # todo: se encontrar um timer, aguardar alguns segundos e checar novamente.
        '''verifica se a dica fornecida é encontrada no site.'''
        conteudo = Comandos().selecionar_tudo('copiar')
        p.moveTo(x=1890, y=670, duration=1.535)
        p.click(x=1890, y=670)  # clica no cantinho do lado da barra de rolagem ao meio.
        time.sleep(1)
        #p.press('end')
        try:
            pattern = self.dados[id_site]['submit_provas']['pattern']
            dica = re.search(pattern, conteudo)
            if dica:
                dica = dica.group(0)
                Comandos().new_key(id_site, 'code_found', dica)
                logger.success('codigo encontrado.')
        except:
            pass
        return conteudo
    def link_para_tarefa(self, id_link):
        """verifica os dados do site e retorna o link para fazer a tarefa"""

        instrucoes = self.instrucoes(id_link)
        link1 = instrucoes.find('https://')
        link1 = instrucoes[link1:]
        barra_n = link1.find(r'Visit')
        link = link1[:barra_n]
        return link
    def instrucoes(self, id_link):
        """verifica os dados do site e retorna o link para fazer a tarefa"""
        dados = Comandos().read_json('dados_trabalho.json')
        #conteudo_job = dados[id_link]['dados_job']
        conteudo_job = dados[id_link]['dados_job']['raw_data']
        task = conteudo_job.find('What is expected from workers?')
        ate_instrucao = conteudo_job.find('Read the instruction')
        instrucoes = conteudo_job[task:ate_instrucao]
        return instrucoes
    def tempo(self, id):
        try:
            instrucoes = self.instrucoes(id)
            tempo = re.search(r'\d+\d+ Second', instrucoes)
            tempo = str(tempo.group(0))
            tempo = tempo.replace(' Second', '')
            tempo = int(tempo)
            Comandos().new_key(id, 'code_time', tempo)
            #logger.success('tempo')
        except Exception as erro:
            logging.error(f'Id {id}: não foi possivel obter o tempo do codigo.'
                          f' colocando tempo padrão 20 sec.\nsyserr:\n{erro}')
            Comandos().new_key(id, 'code_time', 20)

            #print(erro)
    def bons_trabalhos(self, conteudo):
        if 'https://alistudio.tiny.us/DotCom' in conteudo:
            return True
        elif 'https://cutt.ly/uwcEazBb' in conteudo:
            return True
        elif 'https://cutt.ly/AwrgGbna' in conteudo:
            return True
        else:
            return False
    def pagina_redirecionamento(self):
        p.click(x=1856, y=477)
        time.sleep(1)
        pagina = Comandos().selecionar_tudo('copiar')
        if 'Aviso de redirecionamento' in pagina:
            p.press("tab")
            p.press("enter")
            time.sleep(1)
        else:
            p.hotkey('ctrl', 'r')
            time.sleep(1)
            p.press('end')
            time.sleep(1)
    def click_read(self):
        try:
            procurar_imagem.click_reademe()
            #Comandos().press_space()
            time.sleep(1)
        except:
            time.sleep(0.3)
            p.hotkey('ctrl','f')
            time.sleep(0.3)
            read = pyperclip.copy('read more')
            time.sleep(0.3)
            Comandos().selecionar_tudo('apagar')
            time.sleep(0.3)
            p.hotkey('ctrl', 'v')
            time.sleep(0.3)
            p.press('esc')
            procurar_imagem.click_reademe(end=False)
            # se ainda sim não surgir vai subir um Except pulando a tarefa.
    def se_passou(self, id):
        # todo: melhorar verificação.
        logger.debug('verificando se passou pelo read more')
        dados = Comandos().read_json('dados_trabalho.json')
        dados = dados[id]['site_pattern']
        passou = procurar_imagem.passou_pelo_read_me()
        if passou:
            logger.debug('estamos no google, verificando onde clicar')
            procurar_imagem.change_click_ong()
            time.sleep(2)
        else:
            logger.debug('não passou pelo google, verificando onde estamos.')
            Comandos().clicar_na_url()
            link = Comandos().selecionar_tudo('copiar')
            logger.debug('Verificando se o site é compatível com a dica.')
            try:
                url_find = re.search(dados, link)
                logger.debug(f'{url_find}')
                if url_find != None:
                    url = url_find.group(0)
                    logger.success('Estamos no site certo!')
                else:
                    logger.error('Estamos no site errado.')
                    raise Exception
            except:
                raise Exception
            # pulando para próxima tarefa.
    def hint_site(self, id_job):
        #try:
        dados = Comandos().read_json('dados_trabalho.json')
        conteudo = dados[id_job]['instrucoes']
        hint_site_loc = conteudo.find(r'(my website')
        hint_site_raw = conteudo[hint_site_loc:]
        hint_site_loc_end = conteudo.find(r')')
        hint_site_raw = hint_site_raw[:hint_site_loc_end]
        site = re.search(r'\((.*?)\)', hint_site_raw)
        site = site.group(0)
        site = site[13:]
        site = site.replace(')','')
        if ' ' in site:
            site = site.replace(' ', '')
        #print(site)
        Comandos().new_key(id_job, 'site_hint', str(site))
        try:
            site_pattern = site
            site_pattern = site_pattern.replace("*", "[a-z0-9]+")
            Comandos().new_key(id_job, 'site_pattern', str(site_pattern))
            #print(site_pattern)
        except Exception as erro:
            logger.error(f'não foi possível obter o padrão do site.\nsyserr\n{erro}')
            Comandos().new_key(id_job, 'site_hint', 'Verificar')
    def site(self, id_job):
        # todo: colocar pra fazer a verificação no google. e depois.
        # verificar se a url do site é compatível com a url do trabalho.
        dados = Comandos().read_json('dados_trabalho.json')
        pattern = dados[id_job]['site_pattern']
        #re.search(pattern, )
        time.sleep(2)
        Comandos().clicar_na_url()
        url = Comandos().selecionar_tudo('copiar')
        try:
            validacao = re.search(pattern, url)
            validacao = validacao.group(0)
            logger.debug(f'site encontrado: {validacao}')
            Comandos().new_key(id_job, 'site_check', validacao)
            return True
        except:
            logger.error(f'não foi possível validar o site.')
            return False
    def primeiro_artigo(self):
        '''busca o primeiro artigo do site e acessa'''
        Comandos().clicar_na_url()
        url = Comandos().selecionar_tudo('copiar')
        link1 = scraper.melhores_links(url)[1]
        Comandos().clicar_na_url(digitar=link1)
    def numero_artigo(self, texto):
        '''busca o número atual do artigo procurando pelo botão Next'''
        conteudo = texto
        # Padrões para encontrar o número do artigo
        patterns = ['Next \d+', 'Next to \d+', 'Next \d+\d+', 'Next to \d+\d+',
                    'NEXT \d+', 'NEXT to \d+', 'NEXT \d+\d+', 'NEXT to \d+\d+',
                    'NEXT \d+', 'NEXT TO \d+', 'NEXT \d+\d+', 'NEXT TO \d+\d+']
        # Pesquisa o número do artigo no texto
        match = None
        for pattern in patterns:
            match = re.search(pattern, conteudo)
            if match:
                break
        # Extrai o número do artigo da correspondência
        if match:
            numero = match.group(0)
            #print(numero)
            numero = re.sub(r'\D', '', numero)
            numero = int(numero) - 1
            #if numero == 0:

            #print(numero)
        else:
            #page = re.search(r'page', conteudo)

            return None
        # Retorna o número do artigo
        return numero
    def paginas(self, id_job):
        '''retorna uma lista das páginas [primera, última, onde_aparece_o_codigo]'''
        #todo: lidar com random pages.
        dados = Comandos().read_json('dados_trabalho.json')
        instrucoes = dados[id_job]['instrucoes']
        try:
            primeira = re.search(r'\d+st', instrucoes)
            primeira = str(primeira.group(0))
            segunda = re.search(r'\d+th', instrucoes)
            segunda = str(segunda.group(0))
            ultima = re.search(r'\d+th POST', instrucoes)
            ultima = str(ultima.group(0))

            paginas = [primeira, segunda, ultima]
            primeira = primeira.replace('st', '')
            segunda = segunda.replace('th','')
            ultima = ultima.replace('th POST','')

            primeira = int(primeira)
            segunda = int(segunda)
            ultima = int(ultima)
            Comandos().new_key(id_job, 'paginas',
                               {'1st': primeira,
                                            'last': segunda,
                                            'codigo': ultima,
                                            })
        except Exception as erro:
            logging.error(f'erro ao verificar as páginas para o bot. syserr:{erro}')
            Comandos().new_key(id_job, 'paginas', 'Verificar')
    def ultima_pagina(self, id):
        # todo: adicionar ao get dados
        p.press('end')
        nome = f'provas\\{self.momento()} id {id}.png'
        p.screenshot(nome)
        dados_pagina = Comandos().selecionar_tudo('copiar')
        souce_pagina = Comandos().copy_source()
        Comandos().clicar_na_url()
        link = Comandos().selecionar_tudo('copiar')
        conteudo = {
            'content': dados_pagina,
            'source': souce_pagina,
            'link': link
            }
        Comandos().new_key(id, "last_page", conteudo)
        logger.success(f'id {id} conteúdo coletado com sucesso.')
    def momento(self):
        '''retorna o momento atual em formato compativel com nome de arquivos.'''
        hora = str(datetime.datetime.now())
        hora = hora.replace(' ', '-')
        hora = hora.replace(':', '-')
        #print(hora[5:19])
        return hora[5:19]
    def provas(self, id, ad_link):
        link = scraper.pegar_url_principal_apenas(ad_link)
        try:
            if link != None:
                if not "https://" in link:
                    link = "https://" + link
                link_do_contato = scraper.procurar_correspondencia(link)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                if '.br#saiba-mais' in link_do_contato:
                    link_do_contato = link_do_contato.replace('.br#saiba-mais', r'.br/#saiba-mais')
                verificando = requests.get(url=link_do_contato, headers=headers)
                if verificando.status_code == 200:
                    Comandos().new_key(id, 'ad2_prova', link_do_contato)
                    logger.success(f'id {id}: Link do contato adquirido.')
                    #todo: depois usar o run x seconds para fechar o ad no tempo certo.
            else:
                logger.error(f'id {id}: Falha ao obter o link do contato. verifique manualmente para ter certeza')
                Comandos().new_key(id, 'ad2_prova', {'Verificar': link})
        except Exception as erro:
            Comandos().new_key(id, 'ad2_prova', {'Verificar': link})
            logger.error(f'id {id}: Falha ao verificar o link. syserr:\n {erro}')
    def dica(self, id_job):
        #try:
        dados = Comandos().read_json('dados_trabalho.json')
        conteudo =  dados[id_job]['dados_job']['raw_data']
        provas = conteudo.find('Required proof')
        conteudo = conteudo[provas:]
        #Comandos().nova_chave(id_job, 'submit_provas', {'pedido': conteudo})
        esqueda = -5
        direita = 10
        dica = conteudo.find('*')
        raw_dica = conteudo[esqueda + dica:dica+direita]
        #print(raw_dica)
        barran = raw_dica.find(r'\n')
        raw_dica = str(raw_dica[:barran])
        if ':' in raw_dica:
            dots = raw_dica.find(':')
            raw_dica = str(raw_dica[dots:])
            raw_dica = raw_dica.replace(':','')
        raw_dica = raw_dica.replace('\n','')
        raw_dica = raw_dica.replace('\r','')
        if ' 'in raw_dica:
            dica = raw_dica.replace(' ','')
        else:
            dica = raw_dica
        if '?' in dica:
            dica = dica.replace('?','')

        #print(dica)
        if dica != '':
            pattern = dica.replace("*", "[a-zA-Z0-9]+")
            #print(pattern)
            Comandos().new_key(id_job, 'submit_provas', {'hint': dica,
                                                                       'check': conteudo,
                                                                       'pattern': str(pattern)})
        #hint_codigo = conteudo.find('Hint : ')
        #print(hint_codigo)
    def read_me_page(self):
        self.pagina_redirecionamento()
        conteudo = Comandos().selecionar_tudo('copiar')
    def site_patter(self, id, texto):
        dados = Comandos().read_json('dados_trabalho.json')
        site_pattern = dados[id]['site_pattern']
    def resultado(self, id):
        dados = Comandos().read_json('dados_trabalho.json')
        codigo = dados[id]['code_found']
        pag_final = dados[id]['last_page']['content']
        prova1 = dados[id]['ad1_prova']
        prova2 = dados[id]['ad2_prova']
        Comandos().new_key(id, 'provas', {'codigo': str(codigo),
                                                            'prova1': str(prova1),
                                                            'prova2': str(prova2)})
        Comandos().new_key(id, 'pendente', 'False')
        # try:
        #     if codigo_pattern == '':
        #         resultado = re.search(codigo_pattern, pag_final)
        #         if resultado != None:
        #             resultado = resultado.group(0)
        #         else:
        #             resultado = 'Verificar'
        # except:
        #     logger.error('código não identificado.')
        #     resultado = 'Verificar'

        # if not 'Verificar' in resultado:

        #print(resultado)
    def check(self):
        dados = Comandos().read_json('dados_trabalho.json')
        keys = list(dados)
        for key in keys:
            print(key)
            Verificar().get_dados(parse=False, id_job=key)
    def no_next_number(self, texto):
        patterns = ['Next', 'next', 'NEXT', 'page', 'Page', 'PAGE']
        add = []
        for pattern in patterns:
            find = re.search(pattern, texto)
            if find != None:
                find = find.group(0)
                add.append(find)
        if len(add) >= 2:
            return True
        else:
            return False

class Trabalho():
    def __init__(self):
        self.debug = True
        self.page = None
        self.skip_time = 15
        self.read_time = 15
    def force_next(self, pagina):
        pagina = pagina+1
        p.hotkey('ctrl', 'f')
        pyperclip.copy(f'next {pagina}')
        p.hotkey('ctrl', 'v')
        time.sleep(1)
        force = ['imagens\\force_next.png', 'imagens\\force_next2.png']
        #force = ['imagens\\force_next.png']
        brute_force = len(force) * 5
        while brute_force !=0:
            for imagem in force:
                img = p.locateCenterOnScreen(imagem, confidence=0.8)
                if not img == None:
                    p.click(img)
                    logger.success('clicado em next via brute force')
                    brute_force = 0
                    break

            brute_force = brute_force - 1
    def ad_handle(self, id):
        Comandos().clicar_na_url()
        pagina_atual = Comandos().selecionar_tudo('copiar')
        procurar_imagem.click_ad(5)
        #procurar_imagem.clicar_no_ad()
        time.sleep(3)
        Comandos().clicar_na_url()
        just_check = Comandos().selecionar_tudo('copiar')

        while pagina_atual == just_check:
            time.sleep(1)
            logger.error('Não foi possível clicar no Ad... Recarregando página.')
            p.hotkey('ctrl', 'r')
            p.press('home')
            time.sleep(5)
            ad = procurar_imagem.click_ad(7)
            if ad == 'clicked':
                pass
            else:
                ad = procurar_imagem.clicar_no_ad()

            time.sleep(2)
            Comandos().clicar_na_url()
            just_check = Comandos().selecionar_tudo('copiar')
            if just_check != pagina_atual:
                logger.success(f'Clicado com sucesso no ad :{just_check}')
                Comandos().new_key(id, 'ad1_prova', just_check)
                return just_check
                break
        else:
            Comandos().new_key(id, 'ad1_prova', just_check)
            logger.success(f'Clicado com sucesso no ad :{just_check}')
            return just_check
    def next(self, target, id_site, pagina_atual=1):
        target = target - pagina_atual
        read_time = self.read_time
        p.moveTo(x=1890, y=670, duration=1.535)
        p.click(x=1890, y=670) #clica no cantinho do lado da barra de rolagem ao meio.
        time.sleep(1)
        tentativas = 0
        space = Comandos().press_space()
        # p.middleClick(x=908, y=596)
        # time.sleep(1)
        # p.rightClick(x=908, y=596)
        # time.sleep(0.5)
        # p.click(x=1437, y=11)
        # time.sleep(0.5)
        #p.press('tab', presses=2)
        space.start()
        Comandos().run_simulation_for_x_seconds(read_time, 'leitura')
        space.join()
        # poder ser que quebre a passagem
        #space = lambda: p.press('space', presses=5, interval=0.5)
        #pressing_space = threading.Thread(target=space)
        space2 = Comandos().press_space(vezes=4)
        time.sleep(1)
        procurar_imagem.next_page(tempo_procura=self.skip_time)
        time.sleep(1)
        logger.success('Passando página...')
        pagina_atual = pagina_atual + 1
        logger.debug(f'Pagina atual: {pagina_atual}')
        procurar_imagem.verificar_ad_popup()
        time.sleep(2)
        space2.start()
        target -= 1
        while target != 0:
            try:
                if target ==0:
                    break
                #pressing_space.start()
                Comandos().run_simulation_for_x_seconds(read_time, 'leitura')
                space2.join()
                space2 = Comandos().press_space(intervalo=5.43,vezes=4)
                Verificar().verifica_codigo(id_site)
                p.moveTo(x=1890, y=670, duration=1.535)
                p.click(x=1890, y=670)  # clica no cantinho do lado da barra de rolagem ao meio.
                time.sleep(1)
                procurar_imagem.next_page(tempo_procura=self.skip_time)
                time.sleep(1)
                logger.success('Passando página...')
                pagina_atual = pagina_atual + 1
                logger.debug(f'Pagina atual: {pagina_atual}')
                procurar_imagem.verificar_ad_popup()
                time.sleep(2)
                space2.start()
                target -= 1
            except KeyError:
                logger.error('Não foi posível passar a página, tentando novamente...')
                tentativas = tentativas + 1
                time.sleep(1)
                if tentativas/10 >= 1: #oficial a cada 10 tentativas
                #if tentativas >= 3: # para testes
                    #todo: colocar print nesse momento também para capturar o novo botão Next
                    logger.error('impossível avançar, seguir para o proximo ptrabalho')
                    logger.debug('forçando passagem de página.')
                    raise KeyError

            except p.FailSafeException:
                break
    def voltar_ou_avancar(self, pagina, total, id):
        if pagina > 1:
            logger.info('voltando páginas')
            voltando = threading.Thread(target=procurar_imagem.voltar_pagina(pagina))
            voltando.start()
            voltando.join()
            logger.info(f'terminado de voltar as páginas, agora avançando {total} páginas')
            #procurar_imagem.proxima_pagina(total)
            self.next(total, id)
        elif pagina == 1:
            logger.info(f'avançando paginas {total} páginas')
            self.next(total, id)

            #procurar_imagem.proxima_pagina(total)
    def filtrar_(self, just_data=True):
        if not just_data:
            Verificar().trabalhos()
        incompativel = Comandos().read_json('incompativel.json')
        incompativeis = list(incompativel.keys())
        trabalhos = Comandos().ler_trabalhos()
        quantidade = len(trabalhos)
        for trabalho in trabalhos:
            if not trabalho in incompativeis:
                try:
                    Verificar().get_dados(trabalho)
                except Exception as erro:
                    logger.error(f'Erro ao tratar trabalho: {trabalho}\nsyserr:{erro}\n\nContinuando...')
                    continue
            else:
                logger.debug('pulando trabalho incompativel')
                Comandos().new_key(f'{trabalho}','motivo', 'tarefa não treinada.',
                                   file='incompativel.json')
                continue
    def fazer_lista(self):
        '''realiza as tarefas da lista'''
        ids = Comandos().keys_json()
        quantidade_trabalhos = len(ids)
        logger.debug(f'Trabalhos a fazer: {str(quantidade_trabalhos)}')
        dados = Comandos().read_json('dados_trabalho.json')
        erros = 0
        for id in ids:
            link = dados[id]['link_tarefa']
            pag_final = int(dados[id]['paginas']['last'])
            pag_codigo = int(dados[id]['paginas']['codigo'])
            tempo = int(dados[id]['code_time'])
            try:
                self.bot_config(link, id, pag_final, pag_codigo, tempo)
                if erros> 0:
                    # reseta os erros quando faz com sucesso.
                    erros = 0
            except:
                logger.error('não foi possivel concluir a tarefa')
                erros += 1
                if erros >=2:
                    logger.error('Paragem de segurança. multi triggres')
                    break
                # todo: colocar uma funcao para salvar o print

                continue
            #except Exception as erro:
            #    logger.error(f'Erro durante a execução da tarefa: id={id}\nsyserr:\n{str(erro)}')
            #    break
            #tarefa = chaves[id]['link_tarefa']
    def no_cliente(self, id, pagina_final, pagina_codigo):
        #todo: verificar bug quando não encontra.
        Verificar().primeiro_artigo()
        time.sleep(2)
        procurar_imagem.verificar_ad_popup()
        Comandos().clicar_na_url()
        time.sleep(1)
        p.press('tab',presses=5)
        time.sleep(1)
        conteudo = Comandos().selecionar_tudo('copiar')
        pagina_artigo = Verificar().numero_artigo(conteudo)
        if pagina_artigo == None:
            result = Verificar().no_next_number(conteudo)
            if result:
                pagina_artigo = 1
        logger.debug(f'pagina atual:{pagina_artigo}')
        if pagina_artigo == 0:
            pagina_artigo = pagina_final
        logger.debug(f'check... numero da página atual: {pagina_artigo}')
        self.voltar_ou_avancar(pagina_artigo, pagina_final, id)
        if self.debug:
            logger.debug('tirando print para debug')
            p.screenshot(f'debug\\{id} ultima pagina.png')
        if pagina_codigo > pagina_final:
            logger.debug(f'a página final não possui o código... Procurando nas próximas páginas. ')
            self.next(pagina_codigo, id, pagina_final)

        #elif pagina_codigo < pagina_artigo:
        # if pagina_final != pagina_codigo:
        #     logger.info('A página final não tem o código.')
        #     # pagina_atual = Verificar().numero_artigo()
        #     if pagina_codigo < pagina_final:
        #         logger.info('voltando para a página do código.')
        #         quantas_voltar = pagina_final - pagina_codigo
        #         procurar_imagem.voltar_pagina(pagina_codigo - pagina_final)
        #     if pagina_codigo > pagina_final:
        #         logger.info('Avançando para a página do código.')
        #         #quantas_avancar = pagina_codigo - pagina_final
        #         self.next(id, pagina_final)
        #         #procurar_imagem.proxima_pagina(quantas_avancar)
    def bot_config(self, link, id, pagina_final:int, pagina_codigo:int, esperar:int):
        logger.debug('abrindo chrome')
        Comandos().abrir_chrome()
        logger.debug('acessando url')
        Comandos().clicar_na_url(digitar=link)
        logger.debug('verificando redirecionamento')
        Verificar().pagina_redirecionamento()
        logger.debug('procurando pelo read me')
        Verificar().click_read()
        time.sleep(1)
        logger.debug('confirmando onde clicar')
        Verificar().se_passou(id)
        logger.debug('validando...')
        site_valido = Verificar().site(id)
        try:
            if site_valido:
                self.no_cliente(id, pagina_final, pagina_codigo)
                time.sleep(esperar)
                Verificar().ultima_pagina(id)
                ad_link = self.ad_handle(id)
                Verificar().provas(id, ad_link)
                Verificar().resultado(id)
            else:
                logger.error('site não pode ser validado')
                raise Exception
        except Exception as erro:
                logger.error(f'erro ao tratar o site. Id={id}\nsyseer:\n{erro}')

            #coletar os dados da ultima página
        # continuar processo
        #print(ids)
        #id = Comandos()
        #return dados
    def separar_conlcuidas(self):
        # Carregue os dados originais do arquivo JSON
        dados = Comandos().read_json('dados_trabalho.json')

        # Obtenha as chaves do JSON
        keys = Comandos().keys_json()

        # Crie uma lista para armazenar as chaves a serem removidas
        chaves_a_remover = []

        for key in keys:
            verify = dados[key]['pendente']
            if verify == "False":
                provas = dados[key]['provas']
                site = dados[key]['site_check']
                job_link = dados[key]['link_job']
                last_page = dados[key]['last_page']['link']

                insert = {'provas': provas, 'job': job_link, 'site': site, 'last_page': last_page}

                # Adicione os dados ao novo arquivo JSON 'concluidos.json'
                Comandos().new_key(key, 'resultado', insert, file='concluidos.json')

                logger.success(f'trabalho concluído adicionado a lista separada. Id: {key}')

                # Adicione a chave à lista de chaves a serem removidas
                chaves_a_remover.append(key)

        # Remova as chaves do dicionário original
        for chave in chaves_a_remover:
            del dados[chave]
            logger.debug(f'deletando concluida da lista de trabalhos. id: {chave}')
        # Converta o dicionário de volta para JSON
        dados_em_json = json.dumps(dados, indent=4)

        # Grave os dados atualizados no arquivo original
        with open('dados_trabalho.json', 'w') as arquivo:
            arquivo.write(dados_em_json)

if __name__ == "__main__":
    try:
        time.sleep(3)
        #Trabalho().filtrar_(False)
        #Trabalho().fazer_lista()
        #Trabalho().ad_handle()
        #Trabalho().separar_conlcuidas()
    except KeyboardInterrupt:
        print("Operação interrompida pelo usuário.")
    except Exception as erro:
        print(erro)



