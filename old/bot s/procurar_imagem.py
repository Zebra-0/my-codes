import random
import bot4
from loguru import logger
import time
import find_image
import pyautogui

pyautogui.PAUSE = 1
def limitar_pesquisa():
    try:
        img = pyautogui.locateCenterOnScreen('imagens\\limitar_google.png', confidence=0.7)
        if img.x !=0:
            #pyautogui.click(img.x,img.y)

            return True
    except:
        print("não encontrei limitar pesquisa para português")
        return False

def verificar_ad_popup():
    imagens = ['imagens\\check_ad_popup.png', 'imagens\\check_ad_popup2.png','imagens\\check_ad_popup2.png']
    try:
        for imagem in imagens:
            time.sleep(2)
            img = pyautogui.locateCenterOnScreen(imagem, confidence=0.7)
            if not img == None:
                pyautogui.click(img.x,img.y)
                print("fechando ad popup")
    except:
        #return False
        print("não encontrei ad pop up")

def next_page(tempo_procura):
    imagens = ['imagens\\Next cinza.png','imagens\\Next cinza2.png', 'imagens\\Next azul.png',
               'imagens\\Next azul2.png','imagens\\next white green.png',
                'imagens\\next white green2.png', 'imagens\\Next amarelo.png',
               'imagens\\Next verde.png','imagens\\Next red.png','imagens\\Next red2.png',
                'imagens\\Next azul selected.png', 'imagens\\Next azul3.png'
               ]

    pyautogui.press('end')
    time.sleep(1)
    clique = encontre(imagens, tempo=tempo_procura, click=True)
    time.sleep(1)
    if not clique == 'cliked':
        logger.error('não foi possível passar páginas.')
        raise KeyError


def proxima_pagina(paginas: int, frequencia=0.1, esperar=10):
    paginas = paginas - 1
    erros = 0
    imagens = ['imagens\\Next cinza.png', 'imagens\\Next azul.png',
               'imagens\\Next azul2.png', 'imagens\\Next amarelo.png',
               'imagens\\Next verde.png','imagens\\next white green.png',
               'imagens\\next white green2.png', 'imagens\\Next red.png',
               'imagens\\Next azul selected.png'
               ]

    while paginas != 0:
            try:
                for imagem in imagens:
                    try:
                        verificar_ad_popup()
                    except:
                        pass
                    #time.sleep(frequencia)
                    pyautogui.press('end')
                    time.sleep(frequencia)
                    img = pyautogui.locateCenterOnScreen(imagem, confidence=0.7)
                    if not img == None:
                        if paginas == 0:
                            break
                        logger.debug(f'indo para a próxima página. restam: {str(paginas)}')
                        pyautogui.click(img.x, img.y)
                        bot4.Comandos().run_simulation_for_x_seconds(tempo=esperar, funcao='leitura')
                        paginas -= 1
                        #time.sleep(1)
                    else:
                        try:
                            if paginas ==0:
                                break
                            pyautogui.hotkey('ctrl', 'f')
                            pyautogui.write('Next')
                            next_boss = ['imagens\\Next boss.png', 'imagens\\Next boss2.png']
                            for boss in next_boss:
                            #next_boss = 'imagens\\Next boss.png'
                                time.sleep(1)
                                next_loc = pyautogui.locateCenterOnScreen(boss, confidence=0.7)
                                if not next_loc == None:
                                    x, y =  next_loc
                                    pyautogui.click(x, y)
                                    logger.success(f'Passando para a próxima página.')
                                    paginas -= 1
                                    bot4.Comandos().run_simulation_for_x_seconds(tempo=esperar, funcao='leitura')
                                #else:
                                    #pyautogui.press('enter')
                                    #pyautogui.press('esc')

                        except Exception as erro:
                            logger.error(f'erro ao localizar imagem next boss\n{erro}')
                        erros += 1
                        #check = erro/10%0
                        if erros == 10:
                            pyautogui.screenshot('erros\\ultimo_erro.png')
                            print('tirando print da causa do travamento')
                        #print('erro ao encontrar a imagem na tela.')
                else:
                    continue
            except:
                print('ocorreu um erro ao clicar em next, talvez não tenha esse botão na lista ainda.')
                #break
def encontre(caminhos, tempo, click=False):

    inicio = time.time()
    tempo_passado = 0
    while tempo_passado <= tempo:
        fim = time.time()
        tempo_passado = fim - inicio
        for caminho in caminhos:
            img = pyautogui.locateCenterOnScreen(caminho, confidence=0.7)
            if not img == None:
                pos = img.x, img.y
                if click:
                    logger.success(f'clicando x={img.x} y={img.y}')
                    pyautogui.click(pos)
                    time.sleep(0.3)
                    return 'cliked'
                    break
                else:
                    logger.success(f'prosicão encontrada x={img.x} y={img.y}')
                    return pos
                    break
                #print(pos)
        if tempo_passado >= tempo:
            time.sleep(0.3)
            return None
            break

def change_click_ong():
    traduzir = ['imagens\\traduza.png']
    procurar = True
    while procurar:
        localizacao = encontre(traduzir, 10)
        if not localizacao == None:
            x_traduzir, y_traduzir = localizacao
            pyautogui.click(252, y_traduzir)
            logger.success('acessando site')
            procurar = False

#change_click_ong()
def click_reademe(end=True):
    imagens = ['imagens\\read more red.png', 'imagens\\read more white.png',
               'imagens\\read more white red.png','imagens\\read more white red2.png',
               'imagens\\read more blue.png','imagens\\read more blue2.png',
               'imagens\\read more pink.png']
    #print(f'click_readme ,imagens: {str(len(imagens))}')
    contagem = len(imagens)
    if end:
        pyautogui.press('end')
    time.sleep(1)
    contar_imagens = len(imagens)
    tentativas = 0
    check = contar_imagens * 10 # 10 tentativas para encontrar cada uma das imagens
    while contagem != 0:
        try:
            for imagem in imagens:
                time.sleep(0.3)
                img = pyautogui.locateCenterOnScreen(imagem, confidence=0.7)
                if not img == None:
                    if contagem == 0:
                        break
                    contagem = 0
                    #logger.debug(f'clicando no read_me x={img.x}, y={img.y}')
                    pyautogui.click(img.x, img.y)
                    logger.success(f'read me encontrado. clicando... x={img.x}, y={img.y}')
                    break
                else:
                    tentativas = tentativas + 1
                    if tentativas >= check:
                        logger.error('depois de várias tentativas, não foi possível encontrar o read more pela imagem.')
                        raise Exception
                        break
                    else:
                        pass
                    #logger.debug('procurando botao read me')
        except:
            print('ocorreu um erro ao clicar em next, talvez não tenha esse botão na lista ainda.')
            raise Exception
            # break
def click_ad(tempo):
    imagens = ['imagens\\x ad.png','imagens\\left_banner ad.png', 'imagens\\x ad.png', 'imagens\\bottom ad.png']
    continuar = True
    inicio = time.time()
    tempo_passado = 0
    box_horizontal = {'x':1080,'y':250}
    box_vertical = {'x':180,'y':580}
    while tempo_passado <= tempo:
        fim = time.time()
        tempo_passado = fim - inicio
        img = pyautogui.locateCenterOnScreen('imagens\\x ad.png', confidence=0.8)
        if not img == None:
            random_xh = random.randint(90, box_horizontal['x'] - 190)
            random_yh = random.randint(50, box_horizontal['y'] - 20)
            random_xv = random.randint(50, box_vertical['x'] - 50)
            random_yv = random.randint(50, box_vertical['y'] - 50)
            # localizar um ad no fundo y > 500
            logger.debug(f'escolha aleatória dentro das box conhecidas....'
                         f'xh:{random_xh} '
                         f'yh:{random_yh} '
                         f'xv:{random_xv} '
                         f'yv:{random_yv} '
                         f'x:{img.x} '
                         f'y:{img.y} ')

            # banner topo x > 400 and x < 1550 and y <300:
            if img.x > 400 and img.x < 1550 and img.y <300:
                #banner topo
                x = img.x - random_xh
                y = img.y + random_yh
                logger.debug(f'clicando no ad do topo \nx: {x}\ny:{y}\n')
                pyautogui.click(x, y)

                return 'cliked'
                break
            # banner esquerda x <400 and y < 300
            elif img.x <= 400 and img.y <= 300:
                # banner esquerda
                x= img.x - random_xv
                y = img.y + random_yv
                logger.debug(f'clicando no ad da esquerda \nx: {x}\ny:{y}\n')
                pyautogui.click(x, y)
                return 'cliked'
                break
            # banner direita x >1550 and y<300
            elif img.x >= 1550 and img.y <= 300:
                # banner direita
                x = img.x - random_xv
                y = img.y + random_yv
                logger.debug(f'clicando no ad da direita\nx: {x}\ny:{y}\n')
                pyautogui.click(x, y)
                return 'cliked'
                break
            # banner fundo x > 400 and x < 1550 and y > 700:
            elif img.x > 400 and img.x < 1550 and img.y > 700:
                # banner fundo
                x = img.x - random_xh
                y = img.y + random_yh
                logger.debug(f'clicando no ad do fundo \nx: {x}\ny:{y}\n')
                pyautogui.click(x, y)
                return 'cliked'
                break

        if tempo_passado > tempo:
            #return None
            #logger.debug('não foi possível clicar no anúncio.')
            break


def clicar_no_ad():
    try:
        img = pyautogui.locateCenterOnScreen('imagens\\hide ad.png', confidence=0.7)
        y = img.y - 530
        pyautogui.click(img.x, y)
    except:
        print('não foi possivel encontrar o ad.')
def trabalho_feito():
    try:
        img = pyautogui.locateCenterOnScreen('imagens\\link ja feito.png', confidence=0.7)
        if img == None:
            #print("imagem não encontrada")
            return True
        else:
            #print("imagem encontrada, pular esse trabalho")
            return False
    except:
        #print("link ainda não foi feito.")
        return True

def passou_pelo_read_me():
    try:
        img = pyautogui.locateCenterOnScreen('imagens\\passar pelo google.png', confidence=0.7)
        if img:
            logger.debug('Estamos no google.')
            return True
        else:
            return False
    except:
        print('algum problema em passou_pelo_read_me')
def voltar_artigos(artigo):
    imagens = ['imagens\\previous azul.png', 'imagens\\previous red.png']
    try:
        for imagem in imagens:
            img = pyautogui.locateCenterOnScreen(imagem, confidence=0.7)
            if not img == None:
                while artigo != 1:
                    time.sleep(1)
                    verificar_ad_popup()
                    time.sleep(1)
                    pyautogui.press('end')
                    pyautogui.click(img.x, img.y)
                    artigo -= 1
                return 'terminei'
    except:
        print('algo inesperado aconteceu ao voltar os artigos. verifique se tem imagem correspondente.')

def procurar_timer():
    try:
        img = pyautogui.locateCenterOnScreen('imagens\\timer.png', confidence=0.7)
        print(img.x, img.y)
        if not img == None:
            print(img.x, img.y)
            print('timer encontrado, aguardar por código')
            return True
        else:
            print('timer ainda não foi encontrado.')
            return False
    except:
        print('erro ao verificar pelo timer')
def voltar_pagina(paginas_total: int):
    paginas = paginas_total - 1
    imagens = ['imagens\\previous azul.png', 'imagens\\previous azul2.png', 'imagens\\previous red.png']
    erros = 0
    while paginas != 0:
            try:
                for imagem in imagens:
                    time.sleep(1)
                    try:
                        verificar_ad_popup()
                    except:
                        pass
                    pyautogui.press("end")
                    time.sleep(1)
                    img = pyautogui.locateCenterOnScreen(imagem, confidence=0.7)
                    if not img == None:
                        if paginas == 0:
                            print('passou paginas com sucesso.')
                            break
                        paginas -= 1
                        print('indo para a página anterior. restam: ', paginas)

                        pyautogui.click(img.x, img.y, )
                        time.sleep(1)

                    else:
                        erros += 1
                        if erros == 10:
                            pyautogui.screenshot('erros\\ultimo_erro.png')
                            print('tirando print da causa do travamento')
                        print('erro ao encontrar a imagem na tela.')
                else:
                    continue
            except:
                print('ocorreu um erro ao clicar em previos, talvez não tenha esse botão na lista ainda.')
                #break









