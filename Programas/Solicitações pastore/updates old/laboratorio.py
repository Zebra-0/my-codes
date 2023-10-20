from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
class JanelaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x350")
        self.frame_dados = Frame(self.root)
        self.frame_dados.pack(fill=BOTH, expand=1)
        self.botao_teste = ttk.Button(self.frame_dados, text="botao de teste", style="equilux.TButton")
        self.botao_teste.pack(side=LEFT, padx=10, pady=40)
        self.botao_outra_funcao = ttk.Button(self.frame_dados, text="Outra Função", command=self.outra_funcao)
        self.botao_outra_funcao.pack(side=LEFT, padx=10, pady=40)

    def outra_funcao(self):
        print("Essa é outra função!")
if __name__ == "__main__":
    root = ThemedTk()
    style = ttk.Style(root)
    style.theme_use("equilux")
    app = JanelaPrincipal(root)
    botao_chamar_funcao = ttk.Button(root, text="Chamar outra função", command=app.outra_funcao)
    botao_chamar_funcao.pack(pady=10)
    root.mainloop()
