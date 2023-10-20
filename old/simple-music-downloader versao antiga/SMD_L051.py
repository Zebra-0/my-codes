from pytube import YouTube, Playlist
#import sys
import os
from moviepy.audio.io.AudioFileClip import AudioFileClip
import json
from tkinter import filedialog
#import threading
import pyperclip
import re
# Notas da versão:
# melhorar verificador de links

class Tratar:
    def __init__(self):
        self.configuracoes = config_inicial().read_json_config()


    def verificar_duplicados(self, title, pasta):  # verificar se arquivo já existe
        arquivos = os.listdir(self.configuracoes['PastaUsuarioPadrao'])
        nome_arq = title
        nome_arquivo = f"{nome_arq}"
        print("conferindo nome", nome_arquivo)
        print("conferindo arquivos", arquivos)
        print(arquivos.count(nome_arquivo))
        teste = arquivos.count(nome_arquivo)
        if teste >= 1:
            print("Arquivo já existe, pulando download...")
            return False
        else:
            return True

    # verificando se o link é válido ✔
    def validador_de_link(self, link):
        if "youtube.com/" in link or "youtu.be/" in link:
            if "youtube.com/playlist" in link:
                msg4 = "link validado - Playlist encontrada"
                print(msg4)
                validador = "Playlist"
                return validador
            else:
                msg0 = "Link validado"
                print(msg0)
                validador = "único"
                return validador

        else:
            msg1 = "Link inválido, favor verificar"
            print(msg1)
            validador = False
            # print("Fechando programa")
            return validador

    def validar_link_youtube(self, link):
        try:
            # Verifica se o link é um URL válido do YouTube
            if re.match(r'https?://(www\.)?youtube\.com/watch\?v=.{11}', link):
                # O link é um vídeo único
                YouTube(link)
                return "único"
            elif re.match(r'https?://(www\.)?youtube\.com/playlist\?list=.{34}', link):
                # O link é uma lista de reprodução
                Playlist(link)
                return "Playlist"
            elif re.match(r'https?://(www\.)?youtube\.com/embed/.{11}', link):
                # O link é um URL de incorporação
                return "único"
            else:

                return "Link inválido"
        except Exception as e:
            # Ocorreu uma exceção, o link é inválido
            return "Link inválido, favor verificar"
    def mudar_origem_mp4(self):
        self.origemmp4 = filedialog.askdirectory(initialdir=f""
        f"{self.configuracoes['PastaUsuarioMp3Origem']}", title="Converter desta pasta")
        self.origemmp4 = self.origemmp4.replace("/", "\\")
        self.configuracoes["PastaUsuarioMp3Origem"] = self.origemmp4 + "\\"
        with open('presets.json', 'w') as arquivo:
            json.dump(self.configuracoes, arquivo, indent=4)

    def mudar_destino_mp3(self):
        self.destino_mp3 = filedialog.askdirectory(initialdir=f"{self.configuracoes['PastaUsuarioMp3Convertido']}", title="Converter desta pasta")
        self.destino_mp3 = self.destino_mp3.replace("/", "\\")
        self.configuracoes["PastaUsuarioMp3Convertido"] = self.destino_mp3 + "\\"
        with open('presets.json', 'w') as arquivo:
            json.dump(self.configuracoes, arquivo, indent=4)

    def conversor_mp4(self):
        self.autoconvert = True
        arquivos = os.listdir(self.configuracoes["PastaUsuarioMp3Origem"])
        destino = os.listdir(self.configuracoes["PastaUsuarioMp3Convertido"])
        arquivos_mp4 = []
        destinos_mp3 = []
        try:
            for suspeito in arquivos:
                if ".mp4" in suspeito:
                    arquivos_mp4.append(self.configuracoes["PastaUsuarioMp3Origem"] + suspeito)
            for destinar in destino:
                if ".mp3" in destinar:
                    destinos_mp3.append(self.configuracoes["PastaUsuarioMp3Convertido"] + destinar)
            if self.autoconvert:
                for mp4 in arquivos_mp4:
                    destino_mp3 = mp4.replace(self.configuracoes["PastaUsuarioMp3Origem"],
                                              self.configuracoes["PastaUsuarioMp3Convertido"])
                    arquivo_mp3 = destino_mp3.replace(".mp4", ".mp3")
                    if not arquivo_mp3 in destinos_mp3:
                        mp4_mp3(mp4, arquivo_mp3)
                        #converter = threading.Thread(target=mp4_mp3(mp4, arquivo_mp3))
                        #converter.start()
                        #converter.join()
                    else:
                        print(f"{arquivo_mp3.replace(self.configuracoes['PastaUsuarioMp3Convertido'],'')} já existe no destino")
        except Exception as e:
            print(f"Verifique se há arquivos para converter \n{e}")

        self.autoconvert = False

    def get_copiar(self):
        conteudo_copiado = str(pyperclip.paste())
        return conteudo_copiado

class config_inicial:
    def assegurar_arquivo(self, relative_path):
        """ Get absolute path to resource """
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def read_json_config(self):
        with open(self.assegurar_arquivo('presets.json'), "r") as f:
            config = json.load(f)
            # print(config)
        return config

    def new_pc_json(self):
        configs = self.read_json_config()
        if configs["timesopen"] == 0:
            new_pc = True
            user_music_folder = os.path.expanduser("~" + os.sep + "Music")
            # Define o novo caminho para as pastas no JSON
            data = {
                "PastaUsuarioPadrao": user_music_folder,
                "PastaUsuarioMp3Origem": user_music_folder,
                "PastaUsuarioMp3Convertido": user_music_folder,
                "timesopen": 1
            }
            # Atualiza o arquivo JSON com os novos caminhos
            with open("presets.json", "w") as json_file:
                json.dump(data, json_file, indent=4)
            print("Caminhos atualizados no arquivo JSON.")
            return new_pc

def mp4_mp3(mp4, mp3):
    para_converter = AudioFileClip(mp4)
    para_converter.write_audiofile(mp3)
    para_converter.close()

# organizar entre formato de vídeo e áudio
# opção manual de download (escolher)
# opção automática para download
# verificar se há tracklist e separar arquivos.
# ________________________________________________________________________
# inicializando programa

# insira um link do youtube ✔
# print("Bem-vindo ao SMD!")

# link = input("Insira o link: ")
# if not validador_de_link(link):
#    quit()
# configs = config_inicial().read_json_config()
# baixar_audio(link)
''' def mudar_origem_mp4(self):
        origemmp4 = self.configuracoes["PastaUsuarioMp3Origem"]
        self.origemmp4 = filedialog.askdirectory(initialdir=f"{origemmp4}", title="Converter desta pasta")
        self.origemmp4 = self.origemmp4.replace("/", "\\")
        self.configuracoes["PastaUsuarioMp3Origem"] = self.origemmp4 + "\\"
        with open('presets.json', 'w') as arquivo:
            json.dump(self.configuracoes, arquivo, indent=4)'''