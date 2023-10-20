import json
import tkinter as tk
from tkinter import ttk
from PIL.ImageTk import PhotoImage
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
def load_image(imagem):
    image = Image.open(f"{imagem}")
    photo = ImageTk.PhotoImage(image)
    return photo
# Classe principal que define a estrutura do programa
class Programa:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x200")
        self.root.minsize(1000, 200)
        self.root.maxsize(1000, 200)
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.place(relwidth=1, relheight=1)

        # Crie um botão personalizado usando uma label
        self.img_musica = self.load_image("audio.png")
        self.button = tk.Label(root, image=self.img_musica, cursor="hand2", bd=0)
        self.button.place(x=60, y=125, width=140, height=40)
        # Crie o botão usando o estilo personalizado
        #transparent_button = ttk.Button(root, text="Botão Transparente", style="Transparent.TButton")
        #transparent_button.place(x=60, y=125,width=140,height=40)

    def load_image(self, imagem):
        image = Image.open(f"{imagem}").convert("RGBA")
        photo = ImageTk.PhotoImage(image)
        return photo
# Função para redimensionar a imagem proporcionalmente quando a janela é redimensionada
def resize_image(event):
    new_width = event.width
    new_height = event.height
    resized_image = background_image.resize((new_width, new_height), Image.LANCZOS)
    new_photo = ImageTk.PhotoImage(resized_image)
    background_label.config(image=new_photo)
    background_label.image = new_photo


if __name__ == "__main__":
    # Criação da janela principal usando um tema do ttkthemes
    root = ThemedTk(theme="arc")  # Escolha um tema disponível

    # Criação de uma instância da classe Programa
    app = Programa(root)

    # Caminho da imagem de fundo inicial
    initial_background_path = "0.png"

    # Abre a imagem usando a biblioteca PIL
    background_image = Image.open(initial_background_path)

    # Cria uma instância do PhotoImage a partir da imagem
    background_photo = ImageTk.PhotoImage(background_image)

    # Cria um widget Label para exibir a imagem de fundo
    background_label = tk.Label(app.frame_principal, image=background_photo)

    # Vincula a função de redimensionamento ao evento de redimensionamento da label
    background_label.bind("<Configure>", resize_image)

    # Coloca a label de fundo preenchendo todo o espaço disponível
    background_label.place(relwidth=1, relheight=1)
    # Crie um estilo personalizado para o botão
    style = ttk.Style()
    style.configure("Transparent.TButton", background=root.cget("bg"), relief="flat")

    # Inicia o loop principal do tkinter
    root.mainloop()
