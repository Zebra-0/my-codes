from tkinter import *
from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
# notas da versão: mudança do método de implementação do código, adição de botões e aprendendo e lidar com canvas
class Programa:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x200")
        self.root.minsize(1000, 200)
        self.root.maxsize(1000, 200)
        # define imagem
        self.bg = PhotoImage(file="1.png")
        # Criando Label para o background
        #self.label = Label(self.root, image=self.bg)
        #self.label.place(x=0, y=0, relwidth=1, relheight=1)
        # criando um canvas, "desenho" dentro da janela
        self.canvas = Canvas(self.root, width=1000, height=200)
        self.canvas.pack(fill="both", expand=True)
        # selecionar imagem no canvas, ancorar nortwest para a imagem centralizar direito.
        self.canvas.create_image(0,0, image=self.bg, anchor="nw")
        #self.canvas.create_text(400, 50, text="welcome!", font=("Halvetica", 24), fill="white")
        # criando um botão
        #self.music_image = PhotoImage(file="audio.png")
        #self.music_button = Button(self.root, image=self.music_image, borderwidth=0)
        #self.music_button_window = self.canvas.create_window(10,10, anchor="nw", window=self.music_button)

        #  __botões__
        # __ Botão de down Música
        self.music_image = PhotoImage(file="audio.png")
        self.music_button = self.canvas.create_image(127, 142, image=self.music_image)
        self.canvas.tag_bind(self.music_button, "<Button-1>", self.func_btt_audio)

        # __ Botão down Vídeo
        self.video_image = PhotoImage(file="video.png")
        self.video_button = self.canvas.create_image(245, 142, image=self.video_image, anchor="w")
        self.canvas.tag_bind(self.video_button, "<Button-1>", self.func_btt_video)

        # __ botão selecionar pasta
        self.pasta_image = PhotoImage(file="select.png")
        self.pasta_button = self.canvas.create_image(644, 30, image=self.pasta_image, anchor="nw")
        self.canvas.tag_bind(self.pasta_button, "<Button-1>", self.func_btt_pasta)

        # __ botão de colar
        self.colar_image = PhotoImage(file="Paste.png")
        self.colar_button = self.canvas.create_image(600, 40, image=self.colar_image, anchor="nw")
        self.canvas.tag_bind(self.colar_button, "<Button-1>", self.func_btt_colar)
        # __END__

        # __ https image
        self.https_image = PhotoImage(file="https.png")
        self.https_place = self.canvas.create_image(15, 7, image=self.https_image, anchor="nw")

        # __ Input link
        self.link_input = Entry(self.root, font="Monserrat")
        self.link_input.place(x=100, y=50, width=500)

        # __ Mensagem de notificação inferior
        # self.notificacao_label = Label(self.root, text='teste', font=("Monserrat", 26))
        self.notificacoes = self.canvas.create_text(5, 180, text="teste", font=("Monserrat", 12), anchor="nw")


    def func_btt_audio(self, *args):
        print("A baixar: Áudio")
        self.canvas.itemconfig(self.notificacoes, text="A baixar: Áudio")
    def func_btt_video(self, *args):
        print("A baixar: Vídeo")
        self.canvas.itemconfig(self.notificacoes, text="A baixar: Vídeo")

    def func_btt_pasta(self, *args):
        print("selecionar pasta funcionando")

    def func_btt_colar(self, *args):
        print("botão colar funcionando")
        self.canvas.itemconfig(self.notificacoes, text="*** link colado")

if __name__ == "__main__":
    root = Tk()
    root.title("Simple Music Downloader - SMD 0.3")
    app = Programa(root)
    root.mainloop()
