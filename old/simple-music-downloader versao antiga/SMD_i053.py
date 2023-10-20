# import os
# from tkinter import *
from tkinter import Canvas, END, Tk, Entry, Button, Toplevel, filedialog
from PIL.ImageTk import PhotoImage
from pytube import YouTube, Playlist
# import simpleMusicDownloader as smd
# import threading
from threading import Thread
import json
from webscraper import titulo
import SMD_L051 as smd
from loguru import logger
import time

# Notas da versão:
# algumas mudanças na função de download
# Melhoria de algumas mensagens para o usuário.
# Realizada pequena melhoria na biblioteca Tkinter
# por algum motivo o ambiente virtual está usando o python 3.10 ao compilar
# tamanho do arquivo executável reduzido considerávelmente após remover open-cv do 3.10
# P/ outras versões:
# Continuar a adicionar log de eventos.
# Botão para interromper download
# Adicionar report de downloads
# Adicionar notificações do windows.
# *listinha de bug -- deixar pro final
# botões precisam parecer que estão sendo clicados
# mover lógica do link e porcentagem.

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

smd.config_inicial().new_pc_json()


class Programa:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x200")
        # define imagem
        self.salvar_ao_compilar = smd.config_inicial().assegurar_arquivo
        self.bg = PhotoImage(file=self.salvar_ao_compilar("imagens\\background.png"))
        # criando um canvas, "desenho" dentro da janela
        self.canvas = Canvas(self.root, width=1000, height=200)
        self.canvas.pack(fill="both", expand=True)
        # selecionar imagem no canvas, ancorar nortwest para a imagem centralizar direito.
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")
        #  __botões__
        # __ Botão de down Música
        self.music_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\audio_btt.png"))
        self.music_button = self.canvas.create_image(99, 130, image=self.music_image, anchor="nw")
        self.canvas.tag_bind(self.music_button, "<Button-1>", self.func_btt_audio)

        # __ Botão down Vídeo
        self.video_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\video_btt.png"))
        self.video_button = self.canvas.create_image(326, 128, image=self.video_image, anchor="nw")
        self.canvas.tag_bind(self.video_button, "<Button-1>", self.func_btt_video)

        # __ botão selecionar pasta
        self.pasta_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\SelecionarPasta_btt.png"))
        self.pasta_button = self.canvas.create_image(585, 130, image=self.pasta_image, anchor="nw")
        self.canvas.tag_bind(self.pasta_button, "<Button-1>", self.func_btt_pasta)

        # __ botão de colar
        self.colar_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\colar_btt.png"))
        self.colar_button = self.canvas.create_image(560, 43, image=self.colar_image, anchor="nw")
        self.canvas.tag_bind(self.colar_button, "<Button-1>", self.func_btt_colar)

        # __ botão de limpar
        self.limpar_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\limpar_btt.png"))
        self.limpar_button = self.canvas.create_image(600, 40, image=self.limpar_image, anchor="nw")
        self.canvas.tag_bind(self.limpar_button, "<Button-1>", self.func_btt_limpar)

        # __ botão de baixar
        self.baixar_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\baixar_btt.png"))
        self.baixar_button = self.canvas.create_image(670, 39, image=self.baixar_image, anchor="nw")
        self.canvas.tag_bind(self.baixar_button, "<Button-1>", self.func_btt_baixar)

        # __ botão de donate
        self.donate_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\dontate_btt.png"))
        self.donate_button = self.canvas.create_image(922, 163, image=self.donate_image, anchor="nw")
        self.canvas.tag_bind(self.donate_button, "<Button-1>", self.func_btt_donate)

        # __ botão de informação
        self.info_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\info_btt.png"))
        self.info_button = self.canvas.create_image(963, 163, image=self.info_image, anchor="nw")
        self.canvas.tag_bind(self.info_button, "<Button-1>", self.func_btt_info)

        # __ botão de configurações
        self.config_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\configs_btt.png"))
        self.config_button = self.canvas.create_image(862, 46, image=self.config_image, anchor="nw")
        self.canvas.tag_bind(self.config_button, "<Button-1>", self.func_btt_config)
        # __ botçao de parar download
        self.stopdown_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\StopDownload_btt.png"))
        # self.stopdownload_button = self.canvas.create_image(92,89,image=self.stopdown_image, anchor="nw")
        # __END__
        # __ https image
        self.https_image = PhotoImage(file=self.salvar_ao_compilar("imagens\\https.png"))
        self.https_place = self.canvas.create_image(5, 10, image=self.https_image, anchor="nw")

        # __ Input link
        self.link_input = Entry(self.root, font="Monserrat")
        self.link_input.place(x=93, y=53, width=456)

        # __ Mensagem de notificação meio
        self.notificacao_meio = self.canvas.create_text(120, 89, text="",
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
        self.configuracoes = smd.config_inicial().read_json_config()
        # salvando os arquivos em
        self.pasta_usuario = self.configuracoes["PastaUsuarioPadrao"]
        # notificacao salvando
        self.notificar_pasta = self.canvas.create_text(590, 170, text=f"{self.pasta_usuario}",
                                                       font=("Monserrat", 7), anchor="nw")
        # Carregando variáveis de controle
        self.config_aberta = False
        self.stream = None
        self.login = False
        self.manter_no_topo = False
        self.fixar_on_top = "Fixar Janela no topo"
        self.janela_config = None

    def set_notif(self, mensage: str = None, var_posicao=None, preset=None):
        repetidas = preset
        mensagem = mensage
        posicao = var_posicao
        self.canvas.itemconfig(posicao, text=f"{mensagem}")
        if preset == 1:
            pass

    def baixar_audio(self):
        link = self.link_input.get()
        title = titulo(link)
        validado = smd.Tratar().verificar_duplicados(title, self.pasta_usuario)
        if not validado:
            self.set_notif(var_posicao=self.notificacao_meio, mensage=f"{str(title)} Arquivo já existe")
        else:
            logger.debug("função baixar audio iniciada")
            logger.debug(titulo(link))
            self.canvas.itemconfig(self.notificacao_topo, text=f"{str(title)}")
            self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {str(title)}...")
            self.stream = self.link_data(self.link_input.get()).streams.get_audio_only()
            self.stream.download(output_path=self.pasta_usuario, filename=f"{title}.mp4")
            logger.info(f"arquivo salvo {title}, em: {self.pasta_usuario}")

    def baixar_video(self):
        logger.debug("função baixar video iniciada")
        link = self.link_input.get()
        title = titulo(link)
        validado = smd.Tratar().verificar_duplicados(title, self.pasta_usuario)
        if not validado:
            self.canvas.itemconfig(self.notificacao_meio, text=f"{str(title)} Arquivo já existe")
        else:
            self.canvas.itemconfig(self.notificacao_topo, text=f"{str(title)}...")
            self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {str(title)}...")
            self.link_data(self.link_input.get()).streams.get_highest_resolution().download(
                output_path=self.pasta_usuario, filename=f"{title}.mp4")
            logger.info(f"arquivo salvo {title}, em: {self.pasta_usuario}")

    def baixar_audio_playlist(self):
        audio_playlist = Playlist(self.link_input.get())
        logger.debug("Iniciando download da playlist")
        logger.debug("audio playlist: ", audio_playlist.title)
        self.canvas.itemconfig(self.notificacao_topo, text=f"Plalist: {str(audio_playlist.title)}...")
        for audio in audio_playlist.videos:
            validado = smd.Tratar().verificar_duplicados(audio.watch_url, self.pasta_usuario)
            if not validado:
                self.canvas.itemconfig(self.notificacao_meio, text=f"{str(titulo(audio.watch_url))} Arquivo já existe")
            else:
                title = titulo(audio.watch_url)
                self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {title}")
                self.link_data(audio.watch_url).streams.get_audio_only().download(output_path=self.pasta_usuario,
                                                                                  filename=f"{title}.mp4")
                logger.info(f"arquivo salvo {title}, em: {self.pasta_usuario}")

    def baixar_video_playlist(self):
        video_playlist = Playlist(self.link_input.get())
        # logger.debug("Iniciando download da playlist")
        logger.debug("Iniciando download da playlist : ", video_playlist)
        self.canvas.itemconfig(self.notificacao_topo, text=f"Plalist: {str(video_playlist.title)}...")
        for video in video_playlist.videos:
            validado = smd.Tratar().verificar_duplicados(video.watch_url, self.pasta_usuario)
            if not validado:
                self.canvas.itemconfig(self.notificacao_meio, text=f"{str(titulo(video.watch_url))} Arquivo já existe")
            else:
                title = titulo(video.watch_url)
                self.canvas.itemconfig(self.notificacao_meio, text=f"Baixando: {str(video.title)}")
                self.link_data(video.watch_url).streams.get_highest_resolution().download(
                    output_path=self.pasta_usuario, filename=f"{title}.mp4")
                logger.info(f"arquivo salvo {title}, em: {self.pasta_usuario}")

    def desativar_downloads(self, *args):
        prlogger.debug("desativar download pressionado")
        self.desativar_download = True
        # self.stream.stopdownload

    def func_stop_down(self):
        self.stopdownload_button = self.canvas.create_image(92, 89, image=self.stopdown_image, anchor="nw")
        self.canvas.tag_bind(self.stopdownload_button, "<Button-1>", self.desativar_downloads)

    def func_btt_baixar(self, *args):
        logger.debug("Botão de baixar funcionando")
        upgrade_tipo = smd.Tratar().validar_link_youtube(str(self.link_input.get()))
        logger.debug("validando link: ", upgrade_tipo)
        if upgrade_tipo == "Link inválido":
            self.canvas.itemconfig(self.notificacao_meio, text="Link inválido, Favor verificar")
        elif upgrade_tipo == "único":
            if self.midia == "Áudio":
                download_thread = Thread(target=self.baixar_audio)
                download_thread.start()
            elif self.midia == "Video":
                download_thread = Thread(target=self.baixar_video)
                download_thread.start()
        elif upgrade_tipo == "Playlist":
            if self.midia == "Áudio":
                download_thread = Thread(target=self.baixar_audio_playlist)
                download_thread.start()
            elif self.midia == "Video":
                download_thread = Thread(target=self.baixar_video_playlist)
                download_thread.start()

    def func_btt_pasta(self, *args):
        logger.debug("selecionar pasta funcionando")
        self.pasta_caminho = filedialog.askdirectory(initialdir=f"{self.pasta_usuario}", title="Selecione uma pasta")
        if self.pasta_caminho:
            logger.debug("Pasta selecionada:", self.pasta_caminho)
            pasta_caminho = self.pasta_caminho.replace("/", "\\")
            self.configuracoes["PastaUsuarioPadrao"] = pasta_caminho + "\\"
            with open('presets.json', 'w') as arquivo:
                json.dump(self.configuracoes, arquivo, indent=4)
            self.canvas.itemconfig(self.notificar_pasta, text=f"{pasta_caminho}")

    def func_btt_audio(self, *args):
        logger.debug("A baixar: Áudio")
        self.midia = "Áudio"
        self.canvas.itemconfig(self.mostrar_midia, text=f"Mídia: {self.midia}")

    def func_btt_video(self, *args):
        logger.debug("A baixar: Vídeo")
        self.midia = "Video"
        self.canvas.itemconfig(self.mostrar_midia, text=f"Mídia: {self.midia}")

    def func_btt_colar(self, *args):
        logger.debug("botão colar funcionando")
        texto_copiado = smd.Tratar().get_copiar()
        self.link_input.delete(0, END)
        self.link_input.insert(0, texto_copiado)

    def func_btt_limpar(self, *args):
        logger.debug("botão limpar funcionando")
        self.link_input.delete(0, END)
        self.autolimpar_tela()

    def func_btt_donate(self, *args):
        self.janela_donate = Toplevel(self.root)
        self.janela_donate.title("Donate")
        self.janela_donate.geometry("250x300")

        logger.debug("botão de donate funcionando")

    def func_btt_info(self, *args):
        self.janela_info = Toplevel(self.root)
        self.janela_info.title("Sobre o Programa")
        self.janela_info.geometry("250x300")
        logger.debug("botão de informações funcinando")

    def func_btt_config(self, *args):
        if not self.janela_config or not self.janela_config.winfo_exists():  # controla abertura única
            logger.debug("abrindo janela de configurações")
            self.janela_config = Toplevel(self.root)
            self.janela_config.title("Configurações")
            self.janela_config.geometry("250x350")
            # __ botões dentro da tela
            self.origemmp4_button = Button(self.janela_config, text="Origem MP4", command=self.mudar_origem_mp4)
            self.origemmp4_button.place(x=50, y=150)
            self.destinomp3_button = Button(self.janela_config, text="Destino MP3", command=self.mudar_destino_mp3)
            self.destinomp3_button.place(x=50, y=200)
            self.autoconvertmp4 = Button(self.janela_config, text="Auto Converter para mp3", command=self.conversor_mp4)
            self.autoconvertmp4.place(x=50, y=250)
            # botão de login
            # __ botão de manter sempre janela fixada
            self.fixar_janela_button = Button(self.janela_config, text=f"{self.fixar_on_top}",
                                              command=self.fixar_janela)
            self.fixar_janela_button.place(x=50, y=100)
            self.config_aberta = True
        else:
            logger.debug("janela de configurações já está aberta")

    def fixar_janela(self):
        if self.manter_no_topo:
            self.root.attributes('-topmost', False)
            self.fixar_on_top = "Fixar janela no topo"
            logger.debug("Fixando janela principal on top")
        else:
            self.root.attributes('-topmost', True)
            self.fixar_on_top = "Desfixar janela no topo"
            logger.debug("Desfixando janela principal on top")
        self.manter_no_topo = not self.manter_no_topo  # Alterna o estado
        self.fixar_janela_button.config(text=self.fixar_on_top)  # Muda texto do botão

    def mudar_origem_mp4(self):
        smd.Tratar().mudar_origem_mp4()

    def mudar_destino_mp3(self):
        smd.Tratar().mudar_destino_mp3()

    def conversor_mp4(self):
        converter = Thread(target=lambda: smd.Tratar().conversor_mp4())
        converter.daemon = True
        converter.start()

    def link_data(self, link):
        # data = YouTube(link, on_progress_callback=self.update_progresso)
        if self.login:
            # self.youtube_login()
            data = YouTube(link, use_oauth=True, allow_oauth_cache=True, on_progress_callback=self.update_progresso)
            return data
        if not self.login:
            data = YouTube(link, on_progress_callback=self.update_progresso)
            return data

    def update_progresso(self, stream, chunk, bytes_faltando):
        self.canvas.itemconfig(self.porcentagem, text=f"0%")
        if stream:
            total_bytes = stream.filesize
            bytes_baixados = total_bytes - bytes_faltando
            self.porcent = (bytes_baixados / total_bytes) * 100
        self.canvas.itemconfig(self.porcentagem, text=f"{self.porcent:.0f}%")
        update = Thread(target=lambda: root.update_idletasks())
        update.start()
        update.join()
        if self.porcent == 100:
            self.canvas.itemconfig(self.notificacao_meio, text="Concluído")
            time.sleep(1.5)
            self.canvas.itemconfig(self.porcentagem, text="")

    def autolimpar_tela(self):
        self.canvas.itemconfig(self.porcentagem, text="")
        self.canvas.itemconfig(self.notificacao_topo, text="")
        self.canvas.itemconfig(self.notificacao_meio, text="")
        try:
            self.canvas.delete(self.stopdownload_button)
        except:
            logger.debug("botao de parar download ainda não foi criado, mas já era esperado.")


if __name__ == "__main__":
    root = Tk()
    root.title("Simple Music Downloader - SMD 0.5.3 by suportedoluiz")
    root.iconbitmap(smd.config_inicial().assegurar_arquivo("imagens\\icon.ico"))
    root.resizable(width=False, height=False)
    app = Programa(root)
    root.mainloop()
#    fila = queue.Queue()
