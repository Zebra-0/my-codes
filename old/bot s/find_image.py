import time

import pyautogui
import cv2
import numpy as np
#time.sleep(5)
# Carregar a imagem que você deseja procurar

def click_on_image(imagem, just_loc=False):
    imagem_alvo = cv2.imread(imagem)
    captura = pyautogui.screenshot()
    time.sleep(1)
    imagem_da_tela = np.array(captura)
    resultado = cv2.matchTemplate(imagem_da_tela, imagem_alvo, cv2.TM_CCOEFF_NORMED)
    if resultado.size == 0:
        print("A imagem alvo não foi encontrada na captura da tela.")
    else:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
        print("min loc: ",min_loc,"max loc: ", max_loc)
        coordenadas = max_loc
        if just_loc:
            return coordenadas
        else:
            pyautogui.click(coordenadas)

read_more_imagens = ['imagens\\read more red.png', 'imagens\\read more white.png']

def click_read_more():
    imagem_alvo = cv2.imread('imagens\\read more red.png')
    # Capturar a tela
    captura = pyautogui.screenshot()
    # Converter a captura em uma imagem numpy para processamento com OpenCV
    imagem_da_tela = np.array(captura)
    # Procurar a imagem alvo na captura da tela
    resultado = cv2.matchTemplate(imagem_da_tela, imagem_alvo, cv2.TM_CCOEFF_NORMED)
    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
    # Obter as coordenadas do canto superior esquerdo da imagem encontrada
    #coordenadas = max_loc
    # Clicar nas coordenadas
    #pyautogui.click(coordenadas)
    # Verificar se a matriz de resultados está vazia
    if resultado.size == 0:
        print("A imagem alvo não foi encontrada na captura da tela.")
    else:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
        coordenadas = max_loc
        # Clicar nas coordenadas
        pyautogui.click(coordenadas)

def redirecionamento():
    imagem_alvo = cv2.imread('imagens\\redirecionamento.png')
    # Capturar a tela
    captura = pyautogui.screenshot()
    # Converter a captura em uma imagem numpy para processamento com OpenCV
    imagem_da_tela = np.array(captura)
    # Procurar a imagem alvo na captura da tela
    resultado = cv2.matchTemplate(imagem_da_tela, imagem_alvo, cv2.TM_CCOEFF_NORMED)
    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
    # Obter as coordenadas do canto superior esquerdo da imagem encontrada
    #coordenadas = max_loc
    # Clicar nas coordenadas
    #pyautogui.click(coordenadas)
    # Verificar se a matriz de resultados está vazia
    if resultado.size == 0:
        print("A imagem alvo não foi encontrada na captura da tela.")
        return False
    else:
        return True

# Lista de imagens alvo
imagens_alvo = ['imagens\\Next cinza.png', 'imagens\\Next azul.png', 'imagens\\Next amarelo.png']

def click_em_imagens_alvo():
    # Capturar a tela
    captura = pyautogui.screenshot()
    # Converter a captura em uma imagem numpy para processamento com OpenCV
    imagem_da_tela = np.array(captura)

    for imagem_alvo_path in imagens_alvo:
        # Carregar a imagem alvo atual
        imagem_alvo = cv2.imread(imagem_alvo_path)
        # Procurar a imagem alvo na captura da tela
        resultado = cv2.matchTemplate(imagem_da_tela, imagem_alvo, cv2.TM_CCOEFF_NORMED)
        # Verificar se a matriz de resultados não está vazia
        if resultado.size != 0:
            # Encontrou a imagem alvo, obter as coordenadas do canto superior esquerdo
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
            coordenadas = max_loc
            # Clicar nas coordenadas
            pyautogui.click(coordenadas)
            print(f"Clicou na imagem: {imagem_alvo_path}")
            # Pausa opcional para evitar múltiplos cliques na mesma imagem
            # pyautogui.sleep(1)

def click_em_read_me():
    # Capturar a tela
    pyautogui.press("end")
    captura = pyautogui.screenshot()
    # Converter a captura em uma imagem numpy para processamento com OpenCV
    imagem_da_tela = np.array(captura)

    for imagem_alvo_path in read_more_imagens:
        # Carregar a imagem alvo atual
        imagem_alvo = cv2.imread(imagem_alvo_path)
        # Procurar a imagem alvo na captura da tela
        resultado = cv2.matchTemplate(imagem_da_tela, imagem_alvo, cv2.TM_CCOEFF_NORMED)
        # Verificar se a matriz de resultados não está vazia
        if resultado.size != 0:
            # Encontrou a imagem alvo, obter as coordenadas do canto superior esquerdo
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
            coordenadas = max_loc
            # Clicar nas coordenadas
            pyautogui.click(coordenadas)
            print(f"Clicou na imagem: {imagem_alvo_path}")
            # Pausa opcional para evitar múltiplos cliques na mesma imagem
            # pyautogui.sleep(1)


def skip_ad():
    try:
        imagem_alvo = cv2.imread('imagens\\check_ad_popup.png')
        captura = pyautogui.screenshot()
        imagem_da_tela = np.array(captura)
        # Procurar a imagem alvo na captura da tela
        resultado = cv2.matchTemplate(imagem_da_tela, imagem_alvo, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)
        # Obter as coordenadas do canto superior esquerdo da imagem encontrada
        coordenadas = max_loc
        #print(coordenadas.index(0))
        #print(coordenadas.index(1))
        #print(coordenadas)
        # Clicar nas coordenadas
        pyautogui.click(coordenadas)
    except Exception as e:
        print("popup não encontrado, ou de erro:",e)
#def
# Chame a função para clicar nas imagens alvo
#click_em_imagens_alvo()