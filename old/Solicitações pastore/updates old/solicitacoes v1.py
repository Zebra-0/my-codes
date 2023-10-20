import logging
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import tkinter.font as font
import os
import tkinter.messagebox as messagebox
import pyperclip

class JanelaPrincipal:
    def __init__(self, janela):

        # Variaveis que precisam ser definidas antes
        self.clicked_escolherpasta = False
        self.fullpath = ""
        self.dados = []
        self.dados_solicitacao = None
        # cria valores para x e y
        self.xminvalues = 30
        self.xmaxvalues = 600
        self.yvalues = {"pacientes": 8, "aniversario": 35, "tel": 35, "email": 65,
                        "dataprocediemnto": 95, "procedimento": 125, "profissional": 155, "unidade": 185,
                        "requerimento": 225, "copiar": 255, "pasta": 285, "salvar": 315, "limpar": 345,
                        "salvartxt": 375
                        }
        self.entries = None
        self.x_screen_size = 600
        self.y_screen_size = 500
        # iniciando
        self.root = janela
        self.root.geometry("600x500")
        self.root.minsize(self.x_screen_size, self.y_screen_size)
        self.root.maxsize(self.x_screen_size, self.y_screen_size)
        # criando frame para por as coisas e n ficar tremendo ao redimencionar
        self.frame_dados = ttk.Frame(self.root, style="equilux.TFrame")
        self.frame_dados.pack(fill=BOTH, expand=1)

        # crie a janela de menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Menu', menu=file_menu)
        file_menu.add_command(label='1 opção', command=lambda: print("botao funcionando, insira uma função aqui"))

        # cria uma fonte para as labels
        self.fontes = font.Font(size=14)

        # criando titulos dos campos
        self.paciente_label = ttk.Label(self.frame_dados, text="Paciente:", font=self.fontes, style="equilux.TLabel")
        self.paciente_label.place(x=30, y=self.yvalues["pacientes"], width=80)
        self.aniversario_label = ttk.Label(self.frame_dados, text="Data de Nasc.:", font=self.fontes,
                                           style="equilux.TLabel")
        self.aniversario_label.place(x=30, y=self.yvalues["aniversario"])
        self.tel_label = ttk.Label(self.frame_dados, text="Tel:", font=self.fontes, style="equilux.TLabel")
        self.tel_label.place(x=285, y=self.yvalues["tel"])
        self.email_label = ttk.Label(self.frame_dados, text="E-mail:", font=self.fontes, style="equilux.TLabel")
        self.email_label.place(x=30, y=self.yvalues["email"])
        self.dataprocedimento_label = ttk.Label(self.frame_dados, text="Data do proced.:", font=self.fontes,
                                                style="equilux.TLabel")
        self.dataprocedimento_label.place(x=30, y=self.yvalues["dataprocediemnto"])
        self.procedimento_label = ttk.Label(self.frame_dados, text="Procedimento:", font=self.fontes,
                                            style="equilux.TLabel")
        self.procedimento_label.place(x=30, y=self.yvalues["procedimento"])
        self.profissional_label = ttk.Label(self.frame_dados, text="Profissional:", font=self.fontes)
        self.profissional_label.place(x=30, y=self.yvalues["profissional"])
        self.unidade_label = ttk.Label(self.frame_dados, text="Unidade:", font=self.fontes, style="equilux.TLabel")
        self.unidade_label.place(x=30, y=self.yvalues["unidade"])
        self.requerimento_label = ttk.Label(self.frame_dados, text="Requerimento:", font=self.fontes,
                                            style="equilux.TLabel")
        self.requerimento_label.place(x=30, y=self.yvalues["requerimento"])

        # Criando campos para as variáveis (inputs)
        self.paciente_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.paciente_entry.place(x=120, y=self.yvalues["pacientes"], width=400, height=28)
        self.aniversario_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.aniversario_entry.place(x=160, y=self.yvalues["aniversario"], width=120, height=28)
        self.tel_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.tel_entry.place(x=325, y=self.yvalues["tel"], width=195, height=28)
        self.email_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.email_entry.place(x=95, y=self.yvalues["email"], width=280, height=28)
        self.dataprocedimento_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.dataprocedimento_entry.place(x=175, y=self.yvalues["dataprocediemnto"], width=120, height=28)
        self.procedimento_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.procedimento_entry.place(x=160, y=self.yvalues["procedimento"], width=350, height=28)
        self.profissional_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.profissional_entry.place(x=140, y=self.yvalues["profissional"])
        self.unidade_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.unidade_entry.place(x=110, y=self.yvalues["unidade"], width=400, height=28)
        self.requerimento_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                          foreground="#a6a6a6", borderwidth=3, relief="groove", highlightthickness=0)
        self.requerimento_entry.place(x=160, y=self.yvalues["requerimento"], width=400)

        # Criando botões para as funções
        self.salvartxt_botao = ttk.Button(self.frame_dados, text="Salvar em TXT",
                                          command=self.on_salvar_txt)
        self.salvartxt_botao.place(x=30, y=self.yvalues["salvar"])
        self.escolherpasta_botao = ttk.Button(self.frame_dados, text="Escolher Pasta...",
                                              command=self.escolher_pasta)
        self.escolherpasta_botao.place(x=30, y=self.yvalues["pasta"])
        self.limpar_botao = ttk.Button(self.frame_dados, text="Limpar",
                                       command=self.limpar_campos)
        self.limpar_botao.place(x=30, y=self.yvalues["limpar"])
        self.copiar_botao = ttk.Button(self.frame_dados, text="Copiar Solicitação",
                                       command=self.copy_dados)
        self.copiar_botao.place(x=30, y=self.yvalues["copiar"])
        # mensagem explicativa ao usuário

    def obter_dados(self):
        self.dados_solicitacao = [
        ("Paciente", self.paciente_entry.get()),
        ("Data de Nascimento", self.aniversario_entry.get()),
        ("Tel", self.tel_entry.get()),
        ("E-mail", self.email_entry.get()),
        ("Data do procedimento", self.dataprocedimento_entry.get()),
        ("Procedimento", self.procedimento_entry.get()),
        ("Profissional", self.profissional_entry.get()),
        ("Unidade", self.unidade_entry.get()),
        ("Requerimento", self.requerimento_entry.get("1.0", END)),
    ]
        return self.dados_solicitacao
    # gerar eventos ao clicar no botão
    def on_salvar_txt(self):
        # Obter os dados inseridos
        self.dados = self.obter_dados()
        if self.clicked_escolherpasta:
            self.caminho = self.folder_path
            # criando diretório
        else:
            self.caminho = "C:\\Temp\\"
            if not os.path.exists(self.caminho):
                os.makedirs(self.caminho)
        self.fullpath = self.fullpath.replace("/", "\\")

        nome_paciente = self.dados[0][1].strip().replace(" ", "_").upper()
        self.fullpath = f"{self.caminho}\\Solicatacao_{nome_paciente}.txt"
        print(self.fullpath)
        try:
            # Criar um arquivo de texto e escrever os dados nele
            with open(self.fullpath, "w") as f:
                for campo, valor in self.dados:
                    f.write(f"{campo}: {valor}\n")
                # Exibir uma mensagem de sucesso
                messagebox.showinfo("Sucesso", f"Dados salvos em {self.fullpath}!")
        except Exception as e:
            logging.exception("Ocorreu um erro: ")
            print(e)

    def copy_dados(self):
        # Obter os dados inseridos
        self.dados = f'''
Paciente: {self.paciente_entry.get()}
Data de Nascimento: {self.aniversario_entry.get()}
Tel: {self.tel_entry.get()}
E-mail: {self.email_entry.get()}
Data do procedimento:, {self.dataprocedimento_entry.get()}
Procedimento: {self.procedimento_entry.get()}
Profissional: {self.profissional_entry.get()}
Unidade: {self.unidade_entry.get()}
Requerimento: {self.requerimento_entry.get("1.0", END)}
'''
        pyperclip.copy(str(self.dados))
        messagebox.showinfo(title="Dados Copiados", message="Os dados foram copiados!\n Aperte ctrl + V para colar onde desejar!")

    def escolher_pasta(self):
        print("escolhendo pasta")
        self.clicked_escolherpasta = True
        self.folder_path = filedialog.askdirectory(initialdir=".", title="Selecione uma pasta")
        if self.folder_path:
            print("Pasta selecionada:", self.folder_path)
            return self.folder_path

    def limpar_campos(self):
        self.paciente_entry.delete(0, "end")
        self.aniversario_entry.delete(0, "end")
        self.tel_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.dataprocedimento_entry.delete(0, "end")
        self.procedimento_entry.delete(0, "end")
        self.profissional_entry.delete(0, "end")
        self.unidade_entry.delete(0, "end")
        if self.requerimento_entry.winfo_exists():
            text = self.requerimento_entry.get("1.0", "end-1c")
            if text:
                self.requerimento_entry.delete("1.0", "end")


if __name__ == "__main__":
    root = ThemedTk()
    style = ttk.Style(root)
    style.theme_use("equilux")
    app = JanelaPrincipal(root)
    root.mainloop()

print(' Após a finalização da interface e funcionalidades, implementar'
      '\nenvio abrir conversa no telegram'
      ' o envio para o e-mail do paciente confirmando a solicitação')