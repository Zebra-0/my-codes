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
import urllib.parse
# tarefas a finalizar
"""
- adicionar/ajustar layouts novos
- corrigir captura de dados dos layouts novos
- corrigir ordem dos botões para apertar tab
- verificar de salvar está salvando corretamente
- ajustar campo do telefone nas solicitações para "Telefone"
- melhorar função de salvar para integrar o save data
"""

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
        with open('optimizeconfig.json') as f:
            self.confi = json.load(f)
        # Variaveis que precisam ser definidas antes
        self.unidades = ['Centro', 'Tijuca (Sans Peña)', 'Tijuca (Maj Ávila)', 'Botafogo', 'Copacabana', 'Ramos',
                         'Campo Grande', 'Cascadura', 'Caxias', 'Grande Rio', ' Jacarepaguá', 'Catete',
                         'Ilha do Governador', 'Madureira', 'Norte Shopping', 'Santa Cruz', 'São Gonçalo']
        self.forget = None
        self.error = False
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
        # cria global para desativar copia por causa de erro
        self.cancelar_copia = False
        # cria uma global para desativar mensagem de copiar
        self.desativar_mensagens = False
        '''iniciando Janela do tkinter com as configurações desejadas'''
        self.root = janela
        self.root.geometry("600x500")
        self.root.minsize(self.confi["screen"]["min-x"], self.confi["screen"]["min-y"])
        self.root.maxsize(self.confi["screen"]["max-x"], self.confi["screen"]["max-y"])
        # criando frame para por as coisas e n ficar tremendo ao redimencionar
        self.frame_dados = ttk.Frame(self.root, style="equilux.TFrame")
        self.frame_dados.pack(fill=BOTH, expand=1)

        '''crie a janela de menu'''
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Menu', menu=file_menu)
        file_menu.add_command(label='Curioso né?', command=lambda: print("botao funcionando, insira uma função aqui"))

        '''cria uma fonte para as labels'''
        self.fontes = font.Font(size=14)
        self.paciente_label = ttk.Label(self.frame_dados, text="         Paciente:",
                                        font=self.fontes, width=300)
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
        self.nome_paciente_label = ttk.Label(self.frame_dados, text="", font=self.fontes)
        self.solicitacao_label = ttk.Label(self.frame_dados, text="  Solicitação: ", font=self.fontes)
        self.atraso_label = ttk.Label(self.frame_dados, text="Motivo atraso:", font=self.fontes)
        self.extensao_retorno_label = ttk.Label(self.frame_dados, text="Extensão retorno")

        '''Criando campos para as entradas dos usuários'''
        self.paciente_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.aniversario_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.tel_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.email_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.dataprocedimento_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.procedimento_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.profissional_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        self.unidade_entry = ttk.Entry(self.frame_dados, font=self.fontes)
        ''' campos que precisam de configuração'''
        self.requerimento_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                          foreground="#a6a6a6", borderwidth=3, relief="groove",
                                          highlightthickness=0)
        self.motivo_extensao_entry = tk.Text(self.frame_dados, font=self.fontes, height=10,
                                             background="#414141",
                                             foreground="#a6a6a6", borderwidth=3, relief="groove",
                                             highlightthickness=0)
        self.motivo_encaixe_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                            foreground="#a6a6a6", borderwidth=3, relief="groove",
                                            highlightthickness=0)
        self.motivo_atraso_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                           foreground="#a6a6a6", borderwidth=3, relief="groove",
                                           highlightthickness=0)
        self.motivo_extensao_label = ttk.Label(self.frame_dados, text="")

        self.motivo_extensao_conosco_entry = tk.Text(self.frame_dados, font=self.fontes, height=10,
                                                     background="#414141",
                                                     foreground="#a6a6a6", borderwidth=3, relief="groove",
                                                     highlightthickness=0)
        self.motivo_extensao_encrr_prof_entry = tk.Text(self.frame_dados, font=self.fontes, height=10,
                                                        background="#414141",
                                                        foreground="#a6a6a6", borderwidth=3, relief="groove",
                                                        highlightthickness=0)
        self.motivo_resultado_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                              foreground="#a6a6a6", borderwidth=3, relief="groove",
                                              highlightthickness=0)
        self.motivo_extensao_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                             foreground="#a6a6a6", borderwidth=3, relief="groove",
                                             highlightthickness=0)
        self.resultado_exame_entry = tk.Text(self.frame_dados, font=self.fontes, height=10, background="#414141",
                                             foreground="#a6a6a6", borderwidth=3, relief="groove",
                                             highlightthickness=0)
        ''' carrega campos personalizados.'''
        self.extensao_retorno_result = ttk.Label(self.frame_dados,
                                                 text=self.custom_text_for("Extensao Retorno", tratado=False))
        self.data_exame_entry = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))
        self.data_exame_entry2 = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))
        self.data_exame_entry3 = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))
        self.data_exame_entry4 = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))
        self.extensao_retorno_conosco_result = ttk.Label(self.frame_dados,
                                                         text=self.custom_text_for("Extensao Retorno \nConosco"))
        self.ERC_data_exame_entry1 = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))
        self.ERC_data_exame_entry2 = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))
        self.ERC_data_exame_entry3 = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))
        self.REP_retorno_encerr_profiss = ttk.Label(self.frame_dados, text="")
        self.resultado_de_exame_label = ttk.Label(self.frame_dados, text="")
        self.receber_contato = ttk.Entry(self.frame_dados, font=lambda: fontes.configure(size=12))

        '''Criando botões'''
        self.criar_botoes()

        ''' Pede para o usuário selecionar o tipo de layout'''
        # configurações necessárias para carregar o layout de solicitação padão
        self.solicitacao = tk.StringVar(self.frame_dados)
        self.solicitacao.set("Padrão")
        # mudar primeira string para trocar o valor inicial da OptionMenu
        self.listbox = ttk.OptionMenu(self.frame_dados, self.solicitacao, "Extensao Retorno", "Padrão",
                                      "Nota Fiscal", "Encaixe/Retorno", "Atraso", "Extensao Retorno",
                                      "Extensao Retorno \nConosco", "Retorno \nEncerr. Profiss.",
                                      "Resultado\n de Exame", command=self.load_layout)
        self.listbox.configure(style="equilux.TMenubutton")
        self.listbox.place(x=self.confi["botoes"]["solicitacao"]["x"], y=self.confi["botoes"]["solicitacao"]["y"])
        '''carregar modulos recentes'''
        self.dinamic_label = ttk.Label(self.frame_dados, text='')
        self.load_layout()
        # self.new_things()
        self.layout_falha()

    def custom_text_for(self, text, tratado=True):
        if text == "Extensao Retorno":
            motivo = (
                f"Paciente entrou em contato solicitando\na extensão de retorno, o mesmo informou\nque realizou"
                f" o procedimento de \n\nno dia [00/00/0000], e vai ficar pronto\nno dia [11/11/1111]."
                f"\nO retorno do paciente encerra\nno dia [22/22/2222]."
                f"\nPoderia verificar a possibilidade do \npaciente retornar no dia [33/33/3333]?"
            )

            if tratado:
                data_exame = self.data_exame_entry.get()
                data_exame2 = self.data_exame_entry2.get()
                data_exame3 = self.data_exame_entry3.get()
                data_exame4 = self.data_exame_entry4.get()
                procedimento = self.procedimento_entry.get()
                lista = [data_exame, data_exame2, data_exame3, data_exame4, procedimento]

                if data_exame and data_exame2 and data_exame3 and data_exame4 and procedimento != '':
                    print(lista)
                    if not all(c.isdigit() or c == '/' for c in data_exame):
                        self.cancelar_copia = True
                        messagebox.showerror("Erro",
                                             f"Data de exame inválida: {data_exame}. "
                                             f"Por favor insira uma data no formato DD/MM/AAAA.")
                    elif not all(c.isdigit() or c == '/' for c in data_exame2):
                        self.cancelar_copia = True
                        messagebox.showerror("Erro",
                                             f"Data de exame inválida: {data_exame2}. "
                                             f"Por favor insira uma data no formato DD/MM/AAAA.")
                    elif not all(c.isdigit() or c == '/' for c in data_exame3):
                        self.cancelar_copia = True
                        messagebox.showerror("Erro",
                                             f"Data de exame inválida: {data_exame3}. "
                                             f"Por favor insira uma data no formato DD/MM/AAAA.")
                    elif not all(c.isdigit() or c == '/' for c in data_exame4):
                        self.cancelar_copia = True
                        messagebox.showerror("Erro",
                                             f"Data de exame inválida: {data_exame4}. "
                                             f"Por favor insira uma data no formato DD/MM/AAAA.")
                    else:
                        new_motivo = motivo.replace("[00/00/0000]", data_exame)
                        new_motivo = new_motivo.replace("[11/11/1111]", data_exame2)
                        new_motivo = new_motivo.replace("[22/22/2222]", data_exame3)
                        new_motivo = new_motivo.replace("[33/33/3333]", data_exame4)
                        new_motivo = new_motivo.replace("\n\n", f"\n{procedimento}\n")
                        self.cancelar_copia = False
                        return new_motivo
                else:
                    print(lista)
                    messagebox.showerror("Erro", "Por favor preencha todos os campos: "
                                                 "Procedimento e Datas no formato Dia/mês/Ano")
                    self.cancelar_copia = True
            else:
                return motivo

    def load_layout(self, *args: object, carregar_layout=True):  # lembrar de colocar os capos novos no limpar.
        """Carrega layouts selecionado pelo usuário"""
        layout = self.solicitacao.get()
        self.limpar_layouts()
        x_requerimento = 160
        y_requerimento = 5 + (self.espacamento * 7)
        if carregar_layout == True:
            if layout == "Padrão":
                layout = str(layout.replace("Padrão", "Padrao"))
                self.layout_base()
                self.requerimento_label.place(x=30,
                                              y=y_requerimento)
                self.requerimento_entry.place(x=x_requerimento,
                                              y=y_requerimento, width=400)
                # mensagem explicativa ao usuário
            elif layout == "Nota Fiscal":
                print("Layout nota fiscal Selecionado")
                self.layout_base(layout)
                # note que somente essa parte muda
                self.nota_fiscal_label.place(x=self.confi["layout"][layout]["x"],
                                             y=self.confi["layout"][layout]["y0"])
                self.nome_paciente_label.place(x=self.confi["layout"][layout]["x"] + 300,
                                               y=self.confi["layout"][layout]["y0"])
                self.paciente_entry.bind("<KeyRelease>", self.atualizar_paciente)
            elif layout == "Encaixe/Retorno":
                self.layout_base(layout)
                # note ser somente essa parte que muda.
                self.solicitacao_label.place(x=self.confi["layout"][layout]["x"],
                                             y=self.confi["layout"][layout]["y"] + (self.espacamento * 7))
                self.motivo_encaixe_entry.place(x=self.confi["layout"][layout]["xentry"],
                                                y=y_requerimento, width=400)
                # --
                motivo = ("Paciente entrou em contato para agendamento de retorno, porém a agenda da profissional se "
                          "encontra completa. Pode liberar o encaixe para o dia ")

                if not motivo in self.motivo_encaixe_entry.get("1.0", "end"):
                    self.motivo_encaixe_entry.insert("1.0", motivo)
            elif layout == "Atraso":
                self.layout_base(layout)
                self.motivo_atraso_entry.place(x=self.confi["layout"][layout]["xentry"],
                                               y=y_requerimento, width=400)
                self.atraso_label.place(x=self.confi["layout"][layout]["x"],
                                        y=self.confi["layout"][layout]["y"] + (self.espacamento * 7))

                motivo = "Paciente informou que irá se atrasar, pois "
                if not motivo in self.motivo_atraso_entry.get("1.0", "end"):
                    self.motivo_atraso_entry.insert("1.0", motivo)
            elif layout == "Extensao Retorno":
                self.layout_base()
                self.requerimento_label.configure(text="Extensão Retorno:", font=lambda: fontes.configure(size=14))
                self.requerimento_label.place(x=15, y=y_requerimento)
                self.extensao_retorno_result.place(x=x_requerimento, y=y_requerimento, width=400)
                self.procedimento_entry.bind("<KeyRelease>", self.atualizar_procediemento)
                self.dinamic_label.place(x=160, y=281)
                self.dinamic_label.lift()
                self.data_exame_entry.place(x=217, y=303, width=110)
                self.data_exame_entry.lift()
                self.data_exame_entry2.place(x=217, y=325, width=110)
                self.data_exame_entry2.lift()
                self.data_exame_entry3.place(x=217, y=370, width=110)
                self.data_exame_entry3.lift()
                self.data_exame_entry4.place(x=365, y=415, width=110)
                self.data_exame_entry4.lift()
            elif layout == "Extensao Retorno \nConosco":
                self.layout_base()
                self.requerimento_label.configure(text=f"Extensão Retorno\n {' ' * 15}Conosco:",
                                                  font=lambda: fontes.configure(size=12))
                self.requerimento_label.place(x=15, y=y_requerimento)
                motivo = f"Paciente entrou em contato solicitando\na extensão de retorno," \
                         f" o mesmo informou\nque realizou os exames conosco. \nO prazo de retorno " \
                         f"encerrou no dia [--/--/----], \nsendo assim, podemos agendar o paciente \npara a " \
                         f"proxima agenda\ndo profissional, no dia [--/--/----]? " \
                         f"\nExames realizados no dia [--/--/----]."
                print(motivo)
                self.extensao_retorno_conosco_result.configure(text=motivo)
                self.extensao_retorno_conosco_result.place(x=x_requerimento, y=y_requerimento, width=400)
                self.ERC_data_exame_entry1.place(x=462, y=283, width=70)
                self.ERC_data_exame_entry1.lift()
                self.ERC_data_exame_entry2.place(x=352, y=325, width=70)
                self.ERC_data_exame_entry2.lift()
                self.ERC_data_exame_entry3.place(x=380, y=350, width=70)
                self.ERC_data_exame_entry3.lift()

                # Configurar label na saída.
                # self.requerimento_entry.place(x=x_requerimento, y=y_requerimento, width=400)
            elif layout == "Retorno \nEncerr. Profiss.":
                self.layout_base()
                # Configurar label na saída!
                self.requerimento_label.configure(text=f"{' ' * 7}Retorno\nEncerr. Profiss.:",
                                                  font=lambda: fontes.configure(size=14))
                self.requerimento_label.place(x=30, y=y_requerimento)
                motivo = "Paciente entrou em contato para agendamento \nde retorno, " \
                         "porém o profissional encerrou \natendimento conosco"
                print(motivo)
                # self.requerimento_entry.place(x=x_requerimento, y=y_requerimento, width=400)
                self.REP_retorno_encerr_profiss.configure(text=motivo)
                self.REP_retorno_encerr_profiss.place(x=x_requerimento, y=y_requerimento)
            elif layout == "Resultado\n de Exame":
                self.layout_base()
                # Configurar label na saída
                self.requerimento_label.configure(text=f"{' ' * 8}Resultado\n{' ' * 7} de Exame:")
                self.requerimento_label.place(x=30, y=y_requerimento - 5)
                # self.requerimento_entry.place(x=x_requerimento, y=y_requerimento, width=400)
                motivo = "Paciente gostaria de receber o resultado via: \n[campo para digitar]"

                self.resultado_de_exame_label.configure(text=motivo)
                self.resultado_de_exame_label.place(x=x_requerimento, y=y_requerimento + 17)

                self.receber_contato.place(x=x_requerimento, y=y_requerimento + 40, width=170)

    def better_copy(self, notificacao=True):
        dados_solocitacao = self.get_data()
        if self.desativar_mensagens:
            print("desativando mensagens")
            notificacao = False
        if not self.cancelar_copia:
            if notificacao:
                pyperclip.copy(str(dados_solocitacao))
                messagebox.showinfo(title="Dados Copiados",
                                    message="Os dados foram copiados!\n Aperte ctrl + V para colar onde desejar!")
            else:
                pyperclip.copy(str(dados_solocitacao))
        elif self.cancelar_copia:
            print("cancelando cópias")

    def get_data(self):
        try:
            # Define uma lista de campos comuns a todas as opções
            comuns = [('Paciente', 'paciente_entry'), ('Data de Nascimento', 'aniversario_entry'),
                      ('Tel', 'tel_entry'), ('E-mail', 'email_entry'),
                      ('Data do procedimento', 'dataprocedimento_entry'), ('Procedimento', 'procedimento_entry'),
                      ('Profissional', 'profissional_entry'), ('Unidade', 'unidade_entry')]
            # Obtém os campos comuns a todas as opções
            dados = '\n'.join([f'{campo}: {getattr(self, widget).get()}' for campo, widget in comuns])
            # Adiciona a opção selecionada, se necessário
            solicitacao = self.solicitacao.get()
            if solicitacao == "Padrão":
                dados += f'\nRequerimento: {self.requerimento_entry.get("1.0", END)}'
                print("Dados a serem copiados:\n" + dados)
            elif solicitacao == "Nota Fiscal":  # contém excessões
                dados = (f'Solicito nota fiscal para o Paciente: {self.paciente_entry.get()}\n'
                         # faz com que essa mensagem seja mostrada no topo
                         f'Data de Nascimento: {self.aniversario_entry.get()}\n'
                         f'Tel: {self.tel_entry.get()}\nE-mail: {self.email_entry.get()}\n'
                         f'Data do procedimento: {self.dataprocedimento_entry.get()}\n'
                         f'Procedimento: {self.procedimento_entry.get()}\n'
                         f'Profissional: {self.profissional_entry.get()}\n'
                         f'Unidade: {self.unidade_entry.get()}\n')
                print("Dados a serem copiados:\n" + dados)
            elif solicitacao == "Encaixe/Retorno":
                dados += f'\nSolicitação: \n{self.motivo_encaixe_entry.get("1.0", END)}'
                print("Dados a serem copiados:\n" + dados)
            elif solicitacao == "Atraso":
                dados += f'\nSolicitação: \n{self.motivo_atraso_entry.get("1.0", END)}'
                print("Dados a serem copiados:\n" + dados)
            elif solicitacao == "Extensao Retorno":
                dados += '\n'.join([f'\nMotivo do pedido de Extensão do retorno:\n' +
                                    f' {self.custom_text_for(solicitacao, True)}'])
            # elif solicitacao ==
            return dados

        except Exception as e:
            messagebox.showinfo("Erro", f"Houve um erro ao obter os dados. \n{e}")
            print(f"[-]Houve um erro ao obter os dados. \n{e}")
            # inserir dados de novos valores

    def criar_botoes(self):
        """Criando botões"""
        try:
            salvartxt_botao = ttk.Button(self.frame_dados, text="Salvar em TXT", command=self.on_salvar_txt)
            escolherpasta_botao = ttk.Button(self.frame_dados, text="Escolher Pasta...",
                                             command=self.escolher_pasta)
            limpar_botao = ttk.Button(self.frame_dados, text="Limpar", command=self.limpar_campos)
            copiar_botao = ttk.Button(self.frame_dados, text="Copiar Solicitação",
                                      command=self.better_copy)
            abrirtelegram_botao = ttk.Button(self.frame_dados, text="Telegram",
                                             command=lambda: abrir_sites("telegram"))
            abrirfeegow_botao = ttk.Button(self.frame_dados, text="Feegow", command=lambda: abrir_sites("feegow"))
            abrirfeegow2_botao = ttk.Button(self.frame_dados, text="Feegow backup",
                                            command=lambda: abrir_sites("feegow2"))
            abrirsuporte_botao = ttk.Button(self.frame_dados, text="Suporte",
                                            command=lambda: abrir_sites("suporte"))
            abriralvaro_botao = ttk.Button(self.frame_dados, text="Alvaro", command=lambda: abrir_sites("alvaro"))
            abrirdb_botao = ttk.Button(self.frame_dados, text="DB", command=lambda: abrir_sites("db"))

            salvartxt_botao.place(x=self.confi["botoes"]["salvar"]["x"], y=self.confi["botoes"]["salvar"]["y"])

            escolherpasta_botao.place(x=self.confi["botoes"]["escolher-pasta"]["x"],
                                      y=self.confi["botoes"]["escolher-pasta"]["y"])
            limpar_botao.place(x=self.confi["botoes"]["limpar"]["x"], y=self.confi["botoes"]["limpar"]["y"])
            copiar_botao.place(x=self.confi["botoes"]["copiar"]["x"], y=self.confi["botoes"]["copiar"]["y"])
            abrirtelegram_botao.place(x=30, y=self.confi["botoes"]["links"]["linha1"])
            abrirfeegow_botao.place(x=120, y=self.confi["botoes"]["links"]["linha1"])
            abrirfeegow2_botao.place(x=210, y=self.confi["botoes"]["links"]["linha1"])
            abrirsuporte_botao.place(x=320, y=self.confi["botoes"]["links"]["linha1"])
            abriralvaro_botao.place(x=410, y=self.confi["botoes"]["links"]["linha1"])
            abrirdb_botao.place(x=500, y=self.confi["botoes"]["links"]["linha1"])
            enviar_zap = ttk.Button(self.frame_dados, text="Enviar via Whatsapp", command=lambda: self.wpp_link())
            enviar_zap.place(x=30, y=375)
        except Exception as e:
            print(f"Houve um erro nos botões.\n {e}")

    def wpp_link(self):
        # Lembrar de verficar se o texto for None, não abrir o whatsapp.
        text = str(self.better_copy())
        if not text == "None":
            pre_texto = "?text="
            link = "https://wa.me/5521964758717"
            text_encoded = urllib.parse.quote(text)
            print(text_encoded)
            return webbrowser.open(link + pre_texto + text_encoded)
        else:
            print("não foi enviada mensagem pelo whatsapp porque o texto retornou None")

    def layout_base(self, layout="Padrao"):
        carregar_base = True
        if carregar_base == True:
            print(f"[...] Carregando layout base, tipo de layout: {layout}")
            x = self.confi["layout"][layout]["x"]  # valor padrão = 30
            y = self.confi["layout"][layout]["y"]  # valor padrão = 5, se Nota fiscal = 30
            distancia_min = 30
            tel_x = [285, 325]
            x_entry = 160
            long_entry_width = 400
            self.paciente_label.place(x=x, y=y, width=160)
            self.aniversario_label.place(x=x, y=y + distancia_min)
            self.tel_label.place(x=tel_x[0], y=y + distancia_min)
            self.email_label.place(x=x, y=y + (distancia_min * 2))
            self.dataprocedimento_label.place(x=x - 16, y=y + (distancia_min * 3))  # x-16 -> ajuste de formatação
            self.procedimento_label.place(x=x, y=y + (distancia_min * 4))
            self.profissional_label.place(x=x, y=y + (distancia_min * 5))
            self.unidade_label.place(x=x, y=y + (distancia_min * 6))
            # Criando campos para as variáveis (inputs)
            self.paciente_entry.place(x=x_entry, y=y, width=long_entry_width, height=28)
            self.aniversario_entry.place(x=x_entry, y=y + distancia_min, width=120, height=28)
            self.tel_entry.place(x=tel_x[1], y=y + distancia_min, width=235, height=28)
            self.email_entry.place(x=x_entry, y=y + (distancia_min * 2), width=long_entry_width, height=28)
            self.dataprocedimento_entry.place(x=x_entry, y=y + (distancia_min * 3), width=120, height=28)
            self.procedimento_entry.place(x=x_entry, y=y + (distancia_min * 4), width=long_entry_width, height=28)
            self.profissional_entry.place(x=x_entry, y=y + (distancia_min * 5), width=long_entry_width)
            self.unidade_entry.place(x=x_entry, y=y + (distancia_min * 6), width=long_entry_width, height=28)
            print(f"[+]layout base carregado com sucesso!")

    def new_things(self):
        problema_2 = ttk.Label(self.frame_dados, text="2 - Ligações com ruídos ")
        problema_3 = ttk.Label(self.frame_dados, text="3 - Ligações com mudas")
        problema_4 = ttk.Label(self.frame_dados, text="4 - Feegow")

        problema_2.place(x=200, y=35)
        problema_3.place(x=200, y=65)
        problema_4.place(x=200, y=95)

    def layout_falha(self, ativar_layout=False):
        ativar_layout = ativar_layout
        if ativar_layout == True:
            problema_1 = ttk.Label(self.frame_dados, text="Selecione o tipo de problema: ")
            problema_1.place(x=30, y=5)
            ''' Pede para o usuário selecionar o tipo de problema'''
            # configurações necessárias para carregar o layout de solicitação padão
            falha = tk.StringVar(self.frame_dados)
            falha.set("Padrão")
            tipo_falha = ttk.OptionMenu(self.frame_dados, falha, "Atraso", "Atraso",
                                        "Ruido", "Muda", "Feegow", "Nuvem")  # , command=self.load_layout)
            tipo_falha.configure(style="equilux.TMenubutton")
            tipo_falha.place(x=300, y=5)
            falha_atual = falha.get()
            if falha_atual == "Atraso":
                self.nome_label = ttk.Label(self.frame_dados, text="       Atendente:")
                self.falha_label = ttk.Label(self.frame_dados, text="Falha: Ligação com atraso.")
                self.numero_label = ttk.Label(self.frame_dados, text="Nº do Paciente:")
                self.ramal_label = ttk.Label(self.frame_dados, text="             Ramal:")
                self.atendente = ttk.Entry(self.frame_dados)
                self.num_paciente = ttk.Entry(self.frame_dados)
                self.ramal = ttk.Entry(self.frame_dados)
                self.falha_label.place(x=30, y=30)
                self.nome_label.place(x=30, y=60)
                self.atendente.place(x=160, y=60, width=400)
                self.numero_label.place(x=20, y=90)
                self.num_paciente.place(x=160, y=90, width=400)
                self.ramal_label.place(x=30, y=120)
                self.ramal.place(x=160, y=120, width=400)
                # cola
        """Atendente - Adalia
,
            Ligação com Ruídos 

            [numero] - Ramal 345"""

    def limpar_layouts(self):
        """limpa os widgets dos layouts que estão na tela. adicionar widgets novos se criados."""
        print("[...] Iniciando limpeza de widgets")
        self.forget = [self.paciente_label, self.aniversario_label, self.tel_label, self.email_label,
                       self.dataprocedimento_label, self.procedimento_label, self.profissional_label,
                       self.unidade_label, self.requerimento_label, self.paciente_entry, self.aniversario_entry,
                       self.tel_entry, self.email_entry, self.dataprocedimento_entry, self.procedimento_entry,
                       self.profissional_entry, self.unidade_entry, self.requerimento_entry, self.nota_fiscal_label,
                       self.nome_paciente_label, self.motivo_encaixe_entry, self.solicitacao_label, self.atraso_label,
                       self.motivo_atraso_entry, self.motivo_extensao_entry, self.motivo_extensao_conosco_entry,
                       self.extensao_retorno_label, self.extensao_retorno_result, self.data_exame_entry,
                       self.data_exame_entry2, self.data_exame_entry3, self.data_exame_entry4,
                       self.extensao_retorno_conosco_result, self.ERC_data_exame_entry1, self.ERC_data_exame_entry2,
                       self.ERC_data_exame_entry3, self.requerimento_label, self.requerimento_label,
                       self.resultado_de_exame_label, self.REP_retorno_encerr_profiss, self.receber_contato,
                       self.extensao_retorno_result, self.dinamic_label]
        for widget in self.forget:
            widget.place_forget()
        print("[+] Limpeza de widgets concluida")

    # limpa os campos preenchidos da tela
    def limpar_campos(self):
        print("[...] Iniciando limpeza de campos")
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
        print("[+] Limpeza de campos concluida")

    # atualiza labels para retornar um valor imediatamente
    def atualizar_paciente(self, event):
        """exemplo de uso  entry.bind("<KeyRelease>", self.atualizar_label)
        :type event: object
        """
        self.nome_paciente_label.config(
            text=self.paciente_entry.get())  # Atualiza o valor da label com o conteúdo da entry

    def atualizar_procediemento(self, event):
        """exemplo de uso  entry.bind("<KeyRelease>", self.atualizar_label)
        :type event: object
        """
        self.dinamic_label.config(text=self.procedimento_entry.get())

    def on_salvar_txt(self): # gerar eventos ao clicar no botão
        """ Obtém dados inseridos nos campos e salva num arquivo txt na pasta padrão ou selecionada """
        self.dados = self.get_data()
        print(self.dados)
        self.fullpath = self.fullpath.replace("/", "\\")
        # criando diretório
        if self.clicked_escolherpasta:
            self.caminho = self.folder_path
        else:
            # se não existir o caminho, cria-se
            if not os.path.exists(self.caminho):
                os.makedirs(self.caminho)
        # configura o nome do arquivo com o nome do paciente
        if self.dados is not None:
            nome_paciente = self.paciente_entry.get()
            nome_paciente.strip().replace(" ", "_").upper()
            self.fullpath = f"{self.caminho}\\Solicatacao_{nome_paciente}.txt"
            print(self.fullpath)
        else:
            erro = Exception
            print(self.dados, str(erro))
            messagebox.showinfo(f"Houve um erro:", f" {str(erro)}")
        try:
            # Criar um arquivo de texto e escrever os dados nele
            print("Caminho do arquivo " + self.fullpath)
            with open(self.fullpath, "w") as f:
                f.write(f"{self.dados}\n")
                # Exibir uma mensagem de sucesso
                messagebox.showinfo("Sucesso", f"Dados salvos em {self.fullpath}!")
        except Exception as e:
            logging.exception("Ocorreu um erro: ")
            print(e)

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
    fontes = font.Font(size=14)
    style.configure('TLabel', font=fontes, )
    style.configure('TEntry', selectbackground=['#0078d7'], font=fontes,
                    fieldbackground=[('!focus', 'systemWindow'), ('focus', 'systemHighlight')])
    app = JanelaPrincipal(root)
    root.mainloop()

print(' Após a finalização da interface e funcionalidades, implementar:'
      ' o envio para o e-mail do paciente confirmando a solicitação\n'
      'gerar, exibir e inserir nº de tickets da solicitação em alguma solução cloud'
      ''
      )
