import json
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk


# Classe principal que define a estrutura do programa
class Programa:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x200")
        self.root.minsize(1000, 200)
        self.root.maxsize(1000, 200)
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.place(relwidth=1, relheight=1)

        # Importa o arquivo json com argumentos importantes.
        with open('presets.json') as f:
            self.confi = json.load(f)


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

    # Inicia o loop principal do tkinter
    root.mainloop()
