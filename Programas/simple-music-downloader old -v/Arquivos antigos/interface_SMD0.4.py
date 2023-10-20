from tkinter import *
from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
# Notas da versão:
# implementar mudanças no layout ✔
# sprite para limpar texto. X
import time

class Programa:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x200")
        self.root.minsize(1000, 200)
        self.root.maxsize(1000, 200)
        self.max_x = 1000
        # define imagem
        self.bg = PhotoImage(file="imagens\\0.png")
        # criando um canvas, "desenho" dentro da janela
        self.canvas = Canvas(self.root, width=1000, height=200)
        self.canvas.pack(fill="both", expand=True)
        # selecionar imagem no canvas, ancorar nortwest para a imagem centralizar direito.
        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        #  __botões__
        # __ Botão de down Música
        self.music_image = PhotoImage(file="imagens\\audio_btt.png")
        self.music_button = self.canvas.create_image(99, 130, image=self.music_image, anchor="nw")
        self.canvas.tag_bind(self.music_button, "<Button-1>", self.func_btt_audio)

        # __ Botão down Vídeo
        self.video_image = PhotoImage(file="imagens\\video_btt.png")
        self.video_button = self.canvas.create_image(326, 128, image=self.video_image, anchor="nw")
        self.canvas.tag_bind(self.video_button, "<Button-1>", self.func_btt_video)

        # __ botão selecionar pasta
        self.pasta_image = PhotoImage(file="imagens\\SelecionarPasta_btt.png")
        self.pasta_button = self.canvas.create_image(585, 130, image=self.pasta_image, anchor="nw")
        self.canvas.tag_bind(self.pasta_button, "<Button-1>", self.func_btt_pasta)

        # __ botão de colar
        self.colar_image = PhotoImage(file="imagens\\colar_btt.png")
        self.colar_button = self.canvas.create_image(560, 43, image=self.colar_image, anchor="nw")
        self.canvas.tag_bind(self.colar_button, "<Button-1>", self.func_btt_colar)

        # __ botão de limpar
        self.limpar_image = PhotoImage(file="imagens\\limpar_btt.png")
        self.limpar_sprite = PhotoImage(file="imagens\\limpar_btt.png")
        self.sprite_item = self.canvas.create_image(550, 40, image= self.limpar_sprite, anchor="nw")
        self.limpar_button = self.canvas.create_image(600, 40, image= self.limpar_image, anchor="nw")

        self.canvas.tag_bind(self.limpar_button, "<Button-1>", self.start_animation)

        # __ botão de baixar
        self.baixar_image = PhotoImage(file="imagens\\baixar_btt.png")
        self.baixar_button = self.canvas.create_image(670, 39, image=self.baixar_image, anchor="nw")
        self.canvas.tag_bind(self.baixar_button, "<Button-1>", self.func_btt_baixar)

        # __ botão de donate
        self.donate_image = PhotoImage(file="imagens\\dontate_btt.png")
        self.donate_button = self.canvas.create_image(922, 163, image=self.donate_image, anchor="nw")
        self.canvas.tag_bind(self.donate_button, "<Button-1>", self.func_btt_donate)

        # __ botão de informação
        self.info_image = PhotoImage(file="imagens\\info_btt.png")
        self.info_button = self.canvas.create_image(963, 163, image=self.info_image, anchor="nw")
        self.canvas.tag_bind(self.info_button, "<Button-1>", self.func_btt_info)

        # __ botão de configurações
        self.config_image = PhotoImage(file="imagens\\configs_btt.png")
        self.config_button = self.canvas.create_image(862, 46, image=self.config_image, anchor="nw")
        self.canvas.tag_bind(self.config_button, "<Button-1>", self.func_btt_config)
        # __END__
        # __ https image
        # self.https_image = PhotoImage(file="imagens\\https.png")
        # self.https_place = self.canvas.create_image(15, 7, image=self.https_image, anchor="nw")

        # __ Input link
        self.link_input = Entry(self.root, font="Monserrat")
        # self.link_input.place(x=93, y=53, width=456)

        # __ Mensagem de notificação inferior
        self.notificacoes = self.canvas.create_text(90, 89, text="Baixando: nome do arquivo",
                                                    font=("Monserrat", 14), anchor="nw", fill="white")


    def func_btt_audio(self, *args):
        print("A baixar: Áudio")
        # self.canvas.itemconfig(self.notificacoes, text="A baixar: Áudio")  # Configura o texto de notificações
    def func_btt_video(self, *args):
        print("A baixar: Vídeo")
        #self.canvas.itemconfig(self.notificacoes, text="A baixar: Vídeo")

    def func_btt_pasta(self, *args):
        print("selecionar pasta funcionando")

    def func_btt_colar(self, *args):
        print("botão colar funcionando")
        #self.canvas.itemconfig(self.notificacoes, text="*** link colado")

    def func_btt_limpar(self, *args):
        print("botão limpar funcionando")

    def func_btt_baixar(self, *args):
        print("botão de baixar funcionando")

    def func_btt_donate(self, *args):
        print("botão de donate funcionando")

    def func_btt_info(self, *args):
        print("botão de informações funcinando")

    def func_btt_config(self, *args):
        print("botão de configurações funcionando")

if __name__ == "__main__":
    root = Tk()
    root.title("Simple Music Downloader - SMD 0.4")
    app = Programa(root)
    root.mainloop()
