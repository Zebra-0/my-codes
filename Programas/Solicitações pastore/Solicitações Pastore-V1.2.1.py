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
import json
import webbrowser
"""Pejeto feito para o call center com disponibilidade gratuita.
Facilitando o processo de criação de solicitações durante a correria do call center."""


def abrir_sites(site):
    if site == "telegram":
        return webbrowser.open("https://web.telegram.org/")
    elif site == "feegow":
        return webbrowser.open("https://app.feegow.com")
    elif site == "feegow2":
        return webbrowser.open("https://app2.feegow.com")
    elif site == "suporte":
        return webbrowser.open("http://suporte.centromedicopastore.com.br/")
    elif site == "alvaro":
        return webbrowser.open("https://aol.alvaroapoio.com.br/login")
    elif site == "db":
        return webbrowser.open("https://www.diagnosticosdobrasil.com.br/")


class JanelaPrincipal:
    def __init__(self, janela):
        with open('config.json') as f:
            self.confi = json.load(f)
        # Variaveis que precisam ser definidas antes
        self.unidades = ['Centro', 'Tijuca (Sans Peña)', 'Tijuca (Maj Ávila)', 'Botafogo', 'Copacabana', 'Ramos',
                         'Campo Grande', 'Cascadura', 'Caxias', 'Grande Rio', ' Jacarepaguá', 'Catete',
                         'Ilha do Governador', 'Madureira', 'Norte Shopping', 'Santa Cruz', 'São Gonçalo']
        self.forget = None
        self.folder_path = None
        self.caminho = "C:\\Temp\\"
        self.clicked_escolherpasta = False
        self.fullpath = ""
        self.dados = []
        self.dados_solicitacao = None
        # cria valores para x e y
        self.espacamento = 30
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
        file_menu.add_command(label='Curioso né?', command=lambda: print("botao funcionando, insira uma função aqui"))

        # cria uma fonte para as labels
        self.fontes = font.Font(size=14)
        self.paciente_label = ttk.Label(self.frame_dados, text="         Paciente:", font=self.fontes,
                                        width=300)
        self.aniversario_label = ttk.Label(self.frame_dados, text="Data de Nasc.:", font=self.fontes)
        self.tel_label = ttk.Label(self.frame_dados, text="Tel:", font=self.fontes)
        self.email_label = ttk.Label(self.frame_dados, text="             E-mail:", font=self.fontes)
        self.dataprocedimento_label = ttk.Label(self.frame_dados, text="Data do proced.:", font=self.fontes)
        self.procedimento_label = ttk.Label(self.frame_dados, text="Procedimento:", font=self.fontes)
        self.profissional_label = ttk.Label(self.frame_dados, text="    Profissional:", font=self.fontes)
        self.unidade_label = ttk.Label(self.frame_dados, text="          Unidade:", font=self.fontes)
        self.requerimento_label = ttk.Label(self.frame_dados, text="Requerimento:", font=self.fontes)
        self.nota_fiscal_label = ttk.Label(self.frame_dados, text=f"Solicito nota referente ao paciente: ",
                                           font=self.fontes)

        # Criando campos para as variáveis (inputs)
        self.paciente_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.aniversario_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.tel_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.email_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.dataprocedimento_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.procedimento_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.profissional_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.unidade_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.requerimento_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                          foreground="#a6a6a6", borderwidth=3, relief="groove",
                                          highlightthickness=0)
        # Criando botões para as funções
        self.salvartxt_botao = ttk.Button(self.frame_dados, text="Salvar em TXT",
                                          command=self.on_salvar_txt)
        self.salvartxt_botao.place(x=self.confi["widgets"]["salvar"]["x"], y=self.confi["widgets"]["salvar"]["y"])
        self.escolherpasta_botao = ttk.Button(self.frame_dados, text="Escolher Pasta...",
                                              command=self.escolher_pasta)
        self.escolherpasta_botao.place(x=self.confi["widgets"]["pasta"]["x"], y=self.confi["widgets"]["pasta"]["y"])
        self.limpar_botao = ttk.Button(self.frame_dados, text="Limpar", command=self.limpar_campos)
        self.limpar_botao.place(x=self.confi["widgets"]["limpar"]["x"], y=self.confi["widgets"]["limpar"]["y"])
        self.copiar_botao = ttk.Button(self.frame_dados, text="Copiar Solicitação",
                                       command=self.copy_dados)
        self.copiar_botao.place(x=self.confi["widgets"]["copiar"]["x"], y=self.confi["widgets"]["copiar"]["y"])
        # mensagem explicativa ao usuário
        self.solicitacao = tk.StringVar(self.frame_dados)
        self.solicitacao.set("Padrão")
        # pede para o usuário selecionar o tipo de layout
        self.listbox = ttk.OptionMenu(self.frame_dados, self.solicitacao, "Padrão", "Padrão",
                                      "Nota Fiscal", "Encaixe/Retorno", "Atraso", command=self.load_layout)
        self.listbox.configure(style="equilux.TMenubutton")
        self.listbox.place(x=self.confi["widgets"]["solicitacao"]["x"], y=self.confi["widgets"]["solicitacao"]["y"])
        self.nome_paciente_label = ttk.Label(self.frame_dados, text="", font=self.fontes)
        # cria um campo para encaixe
        self.motivo_encaixe_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                            foreground="#a6a6a6", borderwidth=3, relief="groove",
                                            highlightthickness=0, )

        self.motivo_atraso_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                           foreground="#a6a6a6", borderwidth=3, relief="groove",
                                           highlightthickness=0, )
        self.solicitacao_label = ttk.Label(self.frame_dados, text="  Solicitação: ", font=self.fontes)
        self.atraso_label = ttk.Label(self.frame_dados, text="Motivo atraso:", font=self.fontes)
        self.load_layout()
        self.abrirtelegram_botao = ttk.Button(self.frame_dados, text="Telegram",
                                              command=lambda: abrir_sites("telegram"))
        self.abrirtelegram_botao.place(x=30, y=450)
        self.abrirfeegow_botao = ttk.Button(self.frame_dados, text="Feegow", command=lambda: abrir_sites("feegow"))
        self.abrirfeegow_botao.place(x=120, y=450)
        self.abrirfeegow2_botao = ttk.Button(self.frame_dados, text="Feegow backup",
                                             command=lambda: abrir_sites("feegow2"))
        self.abrirfeegow2_botao.place(x=210, y=450)
        self.abrirsuporte_botao = ttk.Button(self.frame_dados, text="Suporte", command=lambda: abrir_sites("suporte"))
        self.abrirsuporte_botao.place(x=320, y=450)
        self.abriralvaro_botao = ttk.Button(self.frame_dados, text="Alvaro", command=lambda: abrir_sites("alvaro"))
        self.abriralvaro_botao.place(x=410, y=450)
        self.abrirdb_botao = ttk.Button(self.frame_dados, text="DB", command=lambda: abrir_sites("db"))
        self.abrirdb_botao.place(x=500, y=450)

    def load_layout(self, *args: object):
        """Carrega layouts selecionado pelo usuário"""
        print(f"limpando campos anteriores")
        layout = self.solicitacao.get()
        print(f"posicionando layout{layout}")
        self.limpar_layouts()
        print(f"layout {layout} Selecionado")
        if self.solicitacao.get() == "Padrão":
            layout = str(layout.replace("Padrão", "Padrao"))
            # criando titulos dos campos
            self.paciente_label.place(x=self.confi["pacientes"]["layout"][layout]["x"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=160)
            self.aniversario_label.place(x=self.confi["aniversario"]["layout"][layout]["x"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento)
            self.tel_label.place(x=self.confi["tel"]["layout"][layout]["x"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento)
            self.email_label.place(x=self.confi["email"]["layout"][layout]["x"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2))
            self.dataprocedimento_label.place(x=self.confi["dataprocediemnto"]["layout"][layout]["x"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3))
            self.procedimento_label.place(x=self.confi["procedimento"]["layout"][layout]["x"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4))
            self.profissional_label.place(x=self.confi["profissional"]["layout"][layout]["x"],
                                          y=self.confi["profissional"]["layout"][layout]["y"] + (
                                                  self.espacamento * 5))
            self.unidade_label.place(x=self.confi["unidade"]["layout"][layout]["x"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 6))
            self.requerimento_label.place(x=self.confi["requerimento"]["layout"][layout]["x"],
                                          y=self.confi["requerimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 7))
            # Criando campos para as variáveis (inputs)
            self.paciente_entry.place(x=self.confi["pacientes"]["layout"][layout]["xentry"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=400, height=28)
            self.aniversario_entry.place(x=self.confi["aniversario"]["layout"][layout]["xentry"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento,
                                         width=120, height=28)
            self.tel_entry.place(x=self.confi["tel"]["layout"][layout]["xentry"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento, width=235, height=28)
            self.email_entry.place(x=self.confi["email"]["layout"][layout]["xentry"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2), width=400,
                                   height=28)
            self.dataprocedimento_entry.place(x=self.confi["dataprocediemnto"]["layout"][layout]["xentry"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3), width=120, height=28)
            self.procedimento_entry.place(x=self.confi["procedimento"]["layout"][layout]["xentry"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4), width=400, height=28)
            self.profissional_entry.place(x=self.confi["profissional"]["layout"][layout]["xentry"],
                                          y=self.confi["profissional"]["layout"][layout]["y"] + (
                                                  self.espacamento * 5), width=400)
            self.unidade_entry.place(x=self.confi["unidade"]["layout"][layout]["xentry"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 6),
                                     width=400, height=28)
            self.requerimento_entry.place(x=self.confi["requerimento"]["layout"][layout]["xentry"],
                                          y=self.confi["requerimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 7), width=400)
            # mensagem explicativa ao usuário
        elif self.solicitacao.get() == "Nota Fiscal":
            print("Layout nota fiscal Selecionado")
            # Posicionando titulos
            self.paciente_label.place(x=self.confi["pacientes"]["layout"][layout]["x"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=160)
            self.aniversario_label.place(x=self.confi["aniversario"]["layout"][layout]["x"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento)
            self.tel_label.place(x=self.confi["tel"]["layout"][layout]["x"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento)
            self.email_label.place(x=self.confi["email"]["layout"][layout]["x"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2))
            self.dataprocedimento_label.place(x=self.confi["dataprocediemnto"]["layout"][layout]["x"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3))
            self.procedimento_label.place(x=self.confi["procedimento"]["layout"][layout]["x"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4))
            self.unidade_label.place(x=self.confi["unidade"]["layout"][layout]["x"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 5))
            # Posicionando campos para os inputs
            self.paciente_entry.place(x=self.confi["pacientes"]["layout"][layout]["xentry"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=400, height=28)
            self.aniversario_entry.place(x=self.confi["aniversario"]["layout"][layout]["xentry"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento,
                                         width=120, height=28)
            self.tel_entry.place(x=self.confi["tel"]["layout"][layout]["xentry"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento, width=235, height=28)
            self.email_entry.place(x=self.confi["email"]["layout"][layout]["xentry"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2), width=400,
                                   height=28)
            self.dataprocedimento_entry.place(x=self.confi["dataprocediemnto"]["layout"][layout]["xentry"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3), width=120,
                                              height=28)
            self.procedimento_entry.place(x=self.confi["procedimento"]["layout"][layout]["xentry"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4), width=400, height=28)
            self.unidade_entry.place(x=self.confi["unidade"]["layout"][layout]["xentry"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 5),
                                     width=400, height=28)
            self.nota_fiscal_label.place(x=self.confi["label-nota"]["x"],
                                         y=self.confi["label-nota"]["y"])
            self.nome_paciente_label.place(x=self.confi["label-nota"]["x"] + 300,
                                           y=self.confi["label-nota"]["y"])
            self.paciente_entry.bind("<KeyRelease>", self.atualizar_label)
            # mensagem explicativa ao usuário
        elif self.solicitacao.get() == "Encaixe/Retorno":
            self.paciente_label.place(x=self.confi["pacientes"]["layout"][layout]["x"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=160)
            self.aniversario_label.place(x=self.confi["aniversario"]["layout"][layout]["x"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento)
            self.tel_label.place(x=self.confi["tel"]["layout"][layout]["x"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento)
            self.email_label.place(x=self.confi["email"]["layout"][layout]["x"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2))
            self.dataprocedimento_label.place(x=self.confi["dataprocediemnto"]["layout"][layout]["x"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3))
            self.procedimento_label.place(x=self.confi["procedimento"]["layout"][layout]["x"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4))
            self.unidade_label.place(x=self.confi["unidade"]["layout"][layout]["x"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 5))
            # Posicionando campos para os inputs
            self.paciente_entry.place(x=self.confi["pacientes"]["layout"][layout]["xentry"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=400, height=28)
            self.aniversario_entry.place(x=self.confi["aniversario"]["layout"][layout]["xentry"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento,
                                         width=120, height=28)
            self.tel_entry.place(x=self.confi["tel"]["layout"][layout]["xentry"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento, width=235, height=28)
            self.email_entry.place(x=self.confi["email"]["layout"][layout]["xentry"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2), width=400,
                                   height=28)
            self.dataprocedimento_entry.place(x=self.confi["dataprocediemnto"]["layout"][layout]["xentry"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3), width=120,
                                              height=28)
            self.procedimento_entry.place(x=self.confi["procedimento"]["layout"][layout]["xentry"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4), width=400, height=28)
            self.unidade_entry.place(x=self.confi["unidade"]["layout"][layout]["xentry"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 5),
                                     width=400, height=28)
            self.motivo_encaixe_entry.place(x=self.confi[layout]["xentry"],
                                            y=self.confi[layout]["y"] + (self.espacamento * 7), width=400)
            self.solicitacao_label.place(x=self.confi[layout]["x"] + 15,
                                         y=self.confi[layout]["y"] + (self.espacamento * 7))
            motivo = ("Paciente entrou em contato para agendamento de retorno, porém a agenda da profissional se "
                      "encontra completa. Pode liberar o encaixe para o dia ")

            if not motivo in self.motivo_encaixe_entry.get("1.0", "end"):
                self.motivo_encaixe_entry.insert("1.0", motivo)
        elif self.solicitacao.get() == "Atraso":
            self.paciente_label.place(x=self.confi["pacientes"]["layout"][layout]["x"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=160)
            self.aniversario_label.place(x=self.confi["aniversario"]["layout"][layout]["x"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento)
            self.tel_label.place(x=self.confi["tel"]["layout"][layout]["x"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento)
            self.email_label.place(x=self.confi["email"]["layout"][layout]["x"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2))
            self.dataprocedimento_label.place(x=self.confi["dataprocediemnto"]["layout"][layout]["x"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3))
            self.procedimento_label.place(x=self.confi["procedimento"]["layout"][layout]["x"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4))
            self.unidade_label.place(x=self.confi["unidade"]["layout"][layout]["x"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 5))
            self.atraso_label.place(x=self.confi[layout]["x"],
                                    y=self.confi[layout]["y"] + (self.espacamento * 7))
            # Posicionando campos para os inputs
            self.paciente_entry.place(x=self.confi["pacientes"]["layout"][layout]["xentry"],
                                      y=self.confi["pacientes"]["layout"][layout]["y"], width=400, height=28)
            self.aniversario_entry.place(x=self.confi["aniversario"]["layout"][layout]["xentry"],
                                         y=self.confi["aniversario"]["layout"][layout]["y"] + self.espacamento,
                                         width=120, height=28)
            self.tel_entry.place(x=self.confi["tel"]["layout"][layout]["xentry"],
                                 y=self.confi["tel"]["layout"][layout]["y"] + self.espacamento, width=235, height=28)
            self.email_entry.place(x=self.confi["email"]["layout"][layout]["xentry"],
                                   y=self.confi["email"]["layout"][layout]["y"] + (self.espacamento * 2), width=400,
                                   height=28)
            self.dataprocedimento_entry.place(x=self.confi["dataprocediemnto"]["layout"][layout]["xentry"],
                                              y=self.confi["dataprocediemnto"]["layout"][layout]["y"] + (
                                                      self.espacamento * 3), width=120,
                                              height=28)
            self.procedimento_entry.place(x=self.confi["procedimento"]["layout"][layout]["xentry"],
                                          y=self.confi["procedimento"]["layout"][layout]["y"] + (
                                                  self.espacamento * 4), width=400, height=28)
            self.unidade_entry.place(x=self.confi["unidade"]["layout"][layout]["xentry"],
                                     y=self.confi["unidade"]["layout"][layout]["y"] + (self.espacamento * 5),
                                     width=400, height=28)
            self.motivo_atraso_entry.place(x=self.confi[layout]["xentry"],
                                           y=self.confi[layout]["y"] + (self.espacamento * 7), width=400)
            motivo = "Paciente informou que irá se atrasar, pois ..."
            if not motivo in self.motivo_atraso_entry.get("1.0", "end"):
                self.motivo_atraso_entry.insert("1.0", motivo)

    # limpa os widgets dos layouts que estão na tela. adicionar widgets novos se criados.
    def limpar_layouts(self):
        self.forget = [self.paciente_label, self.aniversario_label, self.tel_label, self.email_label,
                       self.dataprocedimento_label, self.procedimento_label, self.profissional_label,
                       self.unidade_label, self.requerimento_label, self.paciente_entry, self.aniversario_entry,
                       self.tel_entry, self.email_entry, self.dataprocedimento_entry, self.procedimento_entry,
                       self.profissional_entry, self.unidade_entry, self.requerimento_entry, self.nota_fiscal_label,
                       self.nome_paciente_label, self.motivo_encaixe_entry, self.solicitacao_label, self.atraso_label,
                       self.motivo_atraso_entry]
        for widget in self.forget:
            widget.place_forget()

    # limpa os campos preenchidos da tela
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
        self.motivo_encaixe_entry.delete("1.0", "end")
        self.motivo_atraso_entry.delete("1.0", "end")
        self.nome_paciente_label.config(text='')
    # atualiza labels para retornar um valor imediatamente

    def atualizar_label(self, event):
        """exemplo de uso  entry.bind("<KeyRelease>", self.atualizar_label)
        :type event: object
        """
        self.nome_paciente_label.config(
            text=self.paciente_entry.get())  # Atualiza o valor da label com o conteúdo da entry

    @property  # facilita a importaçao
    def obter_dados(self):
        if self.solicitacao.get() == "Padrão":
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
        elif self.solicitacao.get() == "Nota Fiscal":
            self.dados_solicitacao = [
                ("Solicito nota fiscal para o Paciente: ", self.paciente_entry.get()),
                ("Data de Nascimento", self.aniversario_entry.get()),
                ("Tel", self.tel_entry.get()),
                ("E-mail", self.email_entry.get()),
                ("Data do procedimento", self.dataprocedimento_entry.get()),
                ("Procedimento", self.procedimento_entry.get()),
                ("Profissional", self.profissional_entry.get()),
                ("Unidade", self.unidade_entry.get())]
            return self.dados_solicitacao
        elif self.solicitacao.get() == "Encaixe/Retorno":
            self.dados_solicitacao = [
                ("Solicitação de Encaixe Retorno ou consulta", ""),
                ("Paciente", self.paciente_entry.get()),
                ("Data de Nascimento", self.aniversario_entry.get()),
                ("Tel", self.tel_entry.get()),
                ("E-mail", self.email_entry.get()),
                ("Data do procedimento", self.dataprocedimento_entry.get()),
                ("Procedimento", self.procedimento_entry.get()),
                ("Profissional", self.profissional_entry.get()),
                ("Unidade", self.unidade_entry.get()),
                ("solicitação:", self.motivo_encaixe_entry.get("1.0", END))]
            return self.dados_solicitacao
        elif self.solicitacao.get() == "Atraso":
            self.dados_solicitacao = [
                ("Atraso", ""),
                ("Paciente", self.paciente_entry.get()),
                ("Data de Nascimento", self.aniversario_entry.get()),
                ("Tel", self.tel_entry.get()),
                ("E-mail", self.email_entry.get()),
                ("Data do procedimento", self.dataprocedimento_entry.get()),
                ("Procedimento", self.procedimento_entry.get()),
                ("Profissional", self.profissional_entry.get()),
                ("Motivo", self.motivo_atraso_entry.get("1.0", END))]
            return self.dados_solicitacao

    # gerar eventos ao clicar no botão
    def on_salvar_txt(self):
        """obtém dados inseridos nos campos e salva em um arquivo txt na pasta padrão ou selecionada"""
        self.dados = self.obter_dados
        if self.clicked_escolherpasta:
            self.caminho = self.folder_path
            # criando diretório
        else:
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

    # Copia os dados para a área de transferência.
    def copy_dados(self):
        # Obter os dados inseridos
        if self.solicitacao.get() == "Padrão":
            self.dados = (
                f'Paciente: {self.paciente_entry.get()}\n'
                f'Data de Nascimento: {self.aniversario_entry.get()}\n'
                f'Tel: {self.tel_entry.get()}\nE-mail: {self.email_entry.get()}\n'
                f'Data do procedimento: {self.dataprocedimento_entry.get()}\n'
                f'Procedimento: {self.procedimento_entry.get()}\n'
                f'Profissional: {self.profissional_entry.get()}\n'
                f'Unidade: {self.unidade_entry.get()}\n'
                f'Requerimento: {self.requerimento_entry.get("1.0", END)}\n')

        elif self.solicitacao.get() == "Nota Fiscal":
            self.dados = (
                f'Solicito nota fiscal para o Paciente: {self.paciente_entry.get()}\n'
                f'Data de Nascimento: {self.aniversario_entry.get()}\n'
                f'Tel: {self.tel_entry.get()}\nE-mail: {self.email_entry.get()}\n'
                f'Data do procedimento: {self.dataprocedimento_entry.get()}\n'
                f'Procedimento: {self.procedimento_entry.get()}\n'
                f'Profissional: {self.profissional_entry.get()}\n'
                f'Unidade: {self.unidade_entry.get()}\n')
        elif self.solicitacao.get() == "Encaixe/Retorno":
            self.dados = (
                f'Paciente: {self.paciente_entry.get()}\n'
                f'Data de Nascimento: {self.aniversario_entry.get()}\n'
                f'Tel: {self.tel_entry.get()}\nE-mail: {self.email_entry.get()}\n'
                f'Data do procedimento: {self.dataprocedimento_entry.get()}\n'
                f'Procedimento: {self.procedimento_entry.get()}\n'
                f'Profissional: {self.profissional_entry.get()}\n'
                f'Unidade: {self.unidade_entry.get()}\n'
                f'solicitação:" {self.motivo_encaixe_entry.get("1.0", END)}\n')
        elif self.solicitacao.get() == "Atraso":
            self.dados = (
                f'Paciente: {self.paciente_entry.get()}\n'
                f'Data de Nascimento: {self.aniversario_entry.get()}\n'
                f'Tel: {self.tel_entry.get()}\nE-mail: {self.email_entry.get()}\n'
                f'Data do procedimento:, {self.dataprocedimento_entry.get()}\n'
                f'Procedimento: {self.procedimento_entry.get()}\n'
                f'Profissional: {self.profissional_entry.get()}\n'
                f'Unidade: {self.unidade_entry.get()}\n'
                f'solicitação:" {self.motivo_atraso_entry.get("1.0", END)}\n')
        pyperclip.copy(str(self.dados))

        messagebox.showinfo(title="Dados Copiados", message="Os dados foram copiados!\n Aperte ctrl + V para colar "
                                                            "onde desejar!")

    # Escolhe a pasta em que uma solicitação será salva.
    def escolher_pasta(self):
        print("escolhendo pasta")
        self.clicked_escolherpasta = True
        self.folder_path = filedialog.askdirectory(initialdir=".", title="Selecione uma pasta")
        if self.folder_path:
            print("Pasta selecionada:", self.folder_path)
            return self.folder_path


if __name__ == "__main__":
    root = ThemedTk()
    root.title("Solicitações Pastore")
    root.iconbitmap("favicon.ico")
    style = ttk.Style(root)
    style.theme_use("equilux")
    style.configure('TEntry', selectbackground=['#0078d7'], fieldbackground=[('!focus', 'systemWindow'),
                                                                             ('focus', 'systemHighlight')])
    app = JanelaPrincipal(root)
    root.mainloop()

print(' Após a finalização da interface e funcionalidades, implementar:'
      '\nenvio abrir conversa no telegram'
      ' o envio para o e-mail do paciente confirmando a solicitação\n'
      'gerar, exibir e inserir nº de tickets da solicitação em alguma solução cloud')
