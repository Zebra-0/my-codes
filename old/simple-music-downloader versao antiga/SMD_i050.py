# organização do projeto smd. separando lógica da interface

import os
from tkinter import *
from tkinter import filedialog
from PIL.ImageTk import PhotoImage
from pytube import YouTube, Playlist
import simpleMusicDownloader as smd
import threading
import json
from webscraper import titulo
import webbrowser


# Notas da versão:
# opção para fixar a tela sempre no topo
# pequenos ajustes no código

# P/ outras da versões:
# aviso de que o arquivo já existe
# botão para interromper download
# evitar abrir a janela de configurações mais de uma vez
# *listinha de bug -- deixar pro final
# botões precisam parecer que estão sendo clicados
# adicionar report de downloads
# função para controlar as notificações
# adicionar botão de login
# aplicar para autenticação do google
#    raise exceptions.AgeRestrictedError(self.video_id)
# pytube.exceptions.AgeRestrictedError: wqnVzzJadTA is age restricted, and can't be accessed without logging in

# criar um identificador de música tocando real time <- MUIIITO COMPLEXO PRA FAZER AGORA
# mas o gravador de audio está funcional
# ouvir musica atual, identificar e procurar no youtube pra baixar - premium
# lista de download
# opção para baixar toda a lista
def assegurar_arquivo(relative_path):
    """ Get absolute path to resource """
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def read_json_config():
    with open(assegurar_arquivo('presets.json'), "r") as f:
        config = json.load(f)
        # print(config)
    return config

def new_pc_json():
    configs = read_json_config()
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
new_pc_json()
# removido min e max size para resizeble no final.

class Programa:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x200")
        # define imagem
        self.bg = PhotoImage(file=assegurar_arquivo("imagens\\background.png"))
        # criando um canvas, "desenho" dentro da janela
        self.canvas = Canvas(self.root, width=1000, height=200)
        self.canvas.pack(fill="both", expand=True)
        # selecionar imagem no canvas, ancorar nortwest para a imagem centralizar direito.
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")
        #  __botões__
        # __ Botão de down Música
        self.music_image = PhotoImage(file=assegurar_arquivo("imagens\\audio_btt.png"))
        self.music_button = self.canvas.create_image(99, 130, image=self.music_image, anchor="nw")
        self.canvas.tag_bind(self.music_button, "<Button-1>", self.func_btt_audio)

        # __ Botão down Vídeo
        self.video_image = PhotoImage(file=assegurar_arquivo("imagens\\video_btt.png"))
        self.video_button = self.canvas.create_image(326, 128, image=self.video_image, anchor="nw")
        self.canvas.tag_bind(self.video_button, "<Button-1>", self.func_btt_video)

        # __ botão selecionar pasta
        self.pasta_image = PhotoImage(file=assegurar_arquivo("imagens\\SelecionarPasta_btt.png"))
        self.pasta_button = self.canvas.create_image(585, 130, image=self.pasta_image, anchor="nw")
        self.canvas.tag_bind(self.pasta_button, "<Button-1>", self.func_btt_pasta)

        # __ botão de colar
        self.colar_image = PhotoImage(file=assegurar_arquivo("imagens\\colar_btt.png"))
        self.colar_button = self.canvas.create_image(560, 43, image=self.colar_image, anchor="nw")
        self.canvas.tag_bind(self.colar_button, "<Button-1>", self.func_btt_colar)

        # __ botão de limpar
        self.limpar_image = PhotoImage(file=assegurar_arquivo("imagens\\limpar_btt.png"))
        self.limpar_button = self.canvas.create_image(600, 40, image=self.limpar_image, anchor="nw")
        self.canvas.tag_bind(self.limpar_button, "<Button-1>", self.func_btt_limpar)

        # __ botão de baixar
        self.baixar_image = PhotoImage(file=assegurar_arquivo("imagens\\baixar_btt.png"))
        self.baixar_button = self.canvas.create_image(670, 39, image=self.baixar_image, anchor="nw")
        self.canvas.tag_bind(self.baixar_button, "<Button-1>", self.func_btt_baixar)

        # __ botão de donate
        self.donate_image = PhotoImage(file=assegurar_arquivo("imagens\\dontate_btt.png"))
        self.donate_button = self.canvas.create_image(922, 163, image=self.donate_image, anchor="nw")
        self.canvas.tag_bind(self.donate_button, "<Button-1>", self.func_btt_donate)

        # __ botão de informação
        self.info_image = PhotoImage(file=assegurar_arquivo("imagens\\info_btt.png"))
        self.info_button = self.canvas.create_image(963, 163, image=self.info_image, anchor="nw")
        self.canvas.tag_bind(self.info_button, "<Button-1>", self.func_btt_info)

        # __ botão de configurações
        self.config_image = PhotoImage(file=assegurar_arquivo("imagens\\configs_btt.png"))
        self.config_button = self.canvas.create_image(862, 46, image=self.config_image, anchor="nw")
        self.canvas.tag_bind(self.config_button, "<Button-1>", self.func_btt_config)
        # __END__
        # __ https image
        self.https_image = PhotoImage(file=assegurar_arquivo("imagens\\https.png"))
        self.https_place = self.canvas.create_image(5, 10, image=self.https_image, anchor="nw")

        # __ Input link
        self.link_input = Entry(self.root, font="Monserrat")
        self.link_input.place(x=93, y=53, width=456)

        # __ Mensagem de notificação meio
        self.notificacao_meio = self.canvas.create_text(97, 89, text="",
                                                        font=("Monserrat", 14), anchor="nw", fill="white")
        # __ variável para tipo de mídia
        self.midia = "Áudio"
        # self.midia = None

        # __ exibir mídia atual notificação inferior
        self.mostrar_midia = self.canvas.create_text(5, 180, text=f"Mídia: {self.midia}",
                                                     font=("Monserrat", 10), anchor="nw")

        # __ exibir título notificação superior
        self.notificacao_topo = self.canvas.create_text(300, 20, text="",
                                                        font=("Monserrat", 10), anchor="nw")
        # __ mostar porcentagem
        self.porcent = 0
        self.porcentagem = self.canvas.create_text(15, 89, text=f"",
                                                   font=("Monserrat", 14), anchor="nw", fill="white")
        # self.midia = None
        self.midia = "Áudio"
        # configurações carregadas
        self.configuracoes = read_json_config()
        # salvando os arquivos em
        # self.subpasta = self.configuracoes["PastaAdminPadrao"]
        self.pasta_usuario = self.configuracoes["PastaUsuarioPadrao"]
        # self.mp3_em = self.configuracoes["PastaUsuarioMp3Convertido"]
        # notificacao salvando
        self.notificar_pasta = self.canvas.create_text(590, 170, text=f"{self.pasta_usuario}",
                                                       font=("Monserrat", 7), anchor="nw")
        # Configura o temporizador para verificar a inatividade após 10 segundos
        self.inatividade_timer = None
        self.canvas.bind("<Motion>", self.reset_inatividade)
        self.iniciar_temporizador_inatividade()
        self.login = False
        self.manter_no_topo = False


    def autolimpar_tela(self):
        # self.canvas.itemconfig(self.notificar_pasta, text="")
        self.canvas.itemconfig(self.porcentagem, text="")
        self.canvas.itemconfig(self.notificacao_topo, text="")
        self.canvas.itemconfig(self.notificacao_meio, text="")

    def link_data(self, link):
        # data = YouTube(link, on_progress_callback=self.update_progresso)
        if self.login:
            self.youtube_login()
            data = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=self.update_progresso)
            return data
        if not self.login:
            data = YouTube(link, on_progress_callback=self.update_progresso)
            return data

    def update_progresso(self, stream, chunk, bytes_faltando):
        if stream:
            total_bytes = stream.filesize
            bytes_baixados = total_bytes - bytes_faltando
            self.porcent = (bytes_baixados / total_bytes) * 100
        self.canvas.itemconfig(self.porcentagem, text=f"{self.porcent:.0f}%")
        threading.Thread(target=lambda: root.update_idletasks())
        if self.porcent == 100:
            self.canvas.itemconfig(self.notificacao_meio, text="Concluído")

    def baixar_audio(self):
        print("func baixar audio iniciada")
        print(titulo(self.link_input.get()))
        title = titulo(self.link_input.get())
        self.canvas.itemconfig(self.notificacao_topo, text=f"{str(title)}")
        self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {str(title)}...")
        self.link_data(self.link_input.get()).streams.get_audio_only().download(output_path=self.pasta_usuario)

    def baixar_audio_playlist(self):
        audio_playlist = Playlist(self.link_input.get())
        print("Iniciando download da playlist")
        print("audio playlist: ", audio_playlist.title)
        self.canvas.itemconfig(self.notificacao_topo, text=f"Plalist: {str(audio_playlist.title)}...")
        for audio in audio_playlist.videos:
            self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {str(audio.title)}")
            self.link_data(audio.watch_url).streams.get_audio_only().download(output_path=self.pasta_usuario)

    def baixar_video(self):
        print("func baixar video iniciada")
        title = titulo(self.link_input.get())
        self.canvas.itemconfig(self.notificacao_topo, text=f"{str(title)}...")
        self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {str(title)}...")
        self.link_data(self.link_input.get()).streams.get_highest_resolution().download(output_path=self.pasta_usuario)

    def baixar_video_playlist(self):
        video_playlist = Playlist(self.link_input.get())
        print("Iniciando download da playlist")
        print("video playlist: ", video_playlist)
        self.canvas.itemconfig(self.notificacao_topo, text=f"Plalist: {str(video_playlist.title)}...")
        for video in video_playlist.videos:
            self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {str(video.title)}")
            self.link_data(video.watch_url).streams.get_highest_resolution().download(output_path=self.pasta_usuario)

    def func_btt_baixar(self, *args):
        print("Botão de baixar funcionando")
        tipo = smd.validador_de_link(str(self.link_input.get()))
        if not self.midia:
            pass
        elif self.midia == "Áudio":
            print("tipo:", tipo)
            if tipo == "único":
                download_thread = threading.Thread(target=self.baixar_audio)
                download_thread.start()
                # self.baixar_audio()
            if tipo == "Playlist":
                download_thread = threading.Thread(target=self.baixar_audio_playlist)
                download_thread.start()
        elif self.midia == "Video":
            if tipo == "único":
                download_thread = threading.Thread(target=self.baixar_video)
                download_thread.start()

            if tipo == "Playlist":
                download_thread = threading.Thread(target=self.baixar_video_playlist)
                download_thread.start()

    def func_btt_pasta(self, *args):
        print("selecionar pasta funcionando")
        self.pasta_caminho = filedialog.askdirectory(initialdir=f"{self.pasta_usuario}", title="Selecione uma pasta")
        if self.pasta_caminho:
            print("Pasta selecionada:", self.pasta_caminho)
            pasta_caminho = self.pasta_caminho.replace("/", "\\")
            self.configuracoes["PastaUsuarioPadrao"] = pasta_caminho + "\\"
            with open('presets.json', 'w') as arquivo:
                json.dump(self.configuracoes, arquivo, indent=4)
            self.canvas.itemconfig(self.notificar_pasta, text=f"{pasta_caminho}")

    def func_btt_audio(self, *args):
        print("A baixar: Áudio")
        self.midia = "Áudio"
        self.canvas.itemconfig(self.mostrar_midia, text=f"Mídia: {self.midia}")

    def func_btt_video(self, *args):
        print("A baixar: Vídeo")
        self.midia = "Video"
        self.canvas.itemconfig(self.mostrar_midia, text=f"Mídia: {self.midia}")

    def func_btt_colar(self, *args):
        print("botão colar funcionando")
        texto_copiado = root.clipboard_get()
        self.link_input.delete(0, END)
        self.link_input.insert(0, texto_copiado)

    def func_btt_limpar(self, *args):
        print("botão limpar funcionando")
        self.link_input.delete(0, END)
        self.autolimpar_tela()

    def func_btt_donate(self, *args):
        self.janela_donate = Toplevel(self.root)
        self.janela_donate.title("Donate")
        self.janela_donate.geometry("250x300")

        print("botão de donate funcionando")

    def func_btt_info(self, *args):
        self.janela_info = Toplevel(self.root)
        self.janela_info.title("Sobre o Programa")
        self.janela_info.geometry("250x300")
        print("botão de informações funcinando")

    def func_btt_config(self, *args):
        self.janela_config = Toplevel(self.root)
        self.janela_config.title("Configurações")
        self.janela_config.geometry("250x350")
        self.autoconvert = False
        # __ botões dentro da tela
        self.autoconvertmp4 = Button(self.janela_config, text="Auto Converter para mp3", command=self.conversor_mp4)
        self.autoconvertmp4.place(x=50, y=250)
        self.origemmp4_button = Button(self.janela_config, text="Origem MP4", command=self.mudar_origem_mp4)
        self.origemmp4_button.place(x=50, y=200)
        self.destinomp3_button = Button(self.janela_config, text="Destino MP3", command=self.mudar_destino_mp3)
        self.destinomp3_button.place(x=50, y=150)
        # botão de login
        #self.login_button = Button(self.janela_config, text="Login no Youtube")
        # __ botão de manter sempre janela fixada
        self.fixar_janela = Button(self.janela_config, text="Fixar Janela no topo", command=self.fixar_janela)
        self.fixar_janela.place(x=50, y=100)
        print("botão de configurações funcionando")

    def fixar_janela(self):
        skip = 0
        manter = bool(self.manter_no_topo)
        print("manter no topo: ", manter)
        if skip == 0:
            if manter == False:
                self.root.attributes('-topmost',True)
                self.manter_no_topo = True
                print("ativando always on top")
                self.fixar_janela.config(text="Desfixar janela no topo")
                skip = 1
        if skip == 0:
            if manter == True:
                # self.manter_no_topo = True
                self.root.attributes('-topmost',False)
                print("desativando always on top")
                self.manter_no_topo = False
                self.fixar_janela.config(text="Fixar janela no topo")
                skip = 1
        skip -= 1

        print("manter no topo: ", self.manter_no_topo)

    def mudar_origem_mp4(self):
        origemmp4 = self.configuracoes["PastaUsuarioMp3Origem"]
        self.origemmp4 = filedialog.askdirectory(initialdir=f"{origemmp4}", title="Converter desta pasta")
        self.origemmp4 = self.origemmp4.replace("/", "\\")
        self.configuracoes["PastaUsuarioMp3Origem"] = self.origemmp4 + "\\"
        with open('presets.json', 'w') as arquivo:
            json.dump(self.configuracoes, arquivo, indent=4)

    def mudar_destino_mp3(self):
        destino_mp3 = self.configuracoes["PastaUsuarioMp3Convertido"]
        self.destino_mp3 = filedialog.askdirectory(initialdir=f"{destino_mp3}", title="Converter desta pasta")
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

                        threading.Thread(target=smd.mp4_mp3(mp4, arquivo_mp3))
                    else:
                        print("arquivo já existe")
        except Exception as e:
            print(f"Verifique se há arquivos para converter \n{e}")

        self.autoconvert = False


if __name__ == "__main__":
    root = Tk()
    root.title("Simple Music Downloader - SMD 0.4.9")
    root.iconbitmap(assegurar_arquivo("imagens\\icon.ico"))
    root.resizable(width=False, height=False)
    app = Programa(root)
    root.mainloop()
