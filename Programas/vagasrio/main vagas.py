import multiprocessing
import time
#import threading
import ftfy
import chardet
import customtkinter as ctk
import busca_vagas4
import webbrowser
from loguru import logger
import tkinter as tk
from tkinter import ttk
class Visualizador:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x880')
        #self.dados_tarefa()
        # Widgets
        self.descricao = ctk.CTkLabel(self.root, text='Clique em Próxima para iniciar',font=('Arial',15), justify='left', wraplength=900)
        self.descricao.place(x=10, y=50)
        self.next_btt = ctk.CTkButton(self.root, text='Proxima', command=self.better_next)
        self.next_btt.place(x=870, y=10)
        self.previous_btt = ctk.CTkButton(self.root, text='Anterior', command=self.better_previous)
        self.previous_btt.place(x=720, y=10)
        self.candidatar_btt = ctk.CTkButton(self.root, text="Candidatar-se", command=self.candidatar_se)
        self.candidatar_btt.place(x=870, y=40)
        self.vernosite_btt = ctk.CTkButton(self.root, text="Ver no site", command=self.ver_on_site)
        self.vernosite_btt.place(x=870, y=70)
        self.buscar = ctk.CTkButton(self.root, text='Garimpar', command=self.garimpar)
        self.buscar.place(x=570, y=10)
        self.vagas_python_btt = ctk.CTkButton(self.root, text='Filtrar Python', command=self.vagas_python)
        self.vagas_python_btt.place(x=870, y=100)
        self.vagas = busca_vagas4.read_json('vagasrio.json')  # tirar daqui.
        self.paginas = len(self.vagas)  # tirar daqui
        self.linklabel = ctk.CTkLabel(self.root, text=f'')  # tirar daqui
        self.linklabel.place(x=5, y=30)
        self.des_tarefa = None
        self.linkvaga_tarefa = None
        self.link_candidatura_tarefa = None
        self.tarefa_atual = [1,1]
        self.qnt_tarefas = self.contar_tarefas()
        self.qt_label = ctk.CTkLabel(self.root, text=f'Quantidade{self.qnt_tarefas}')
        self.qt_label.place(x=5, y=5)
        self.keywords = ['Python', 'pyhon', 'PYTHON']
        # Visualizar dois tipos de arquivos json em uma lista suspensa
        self.arquivos = ['vagasrio.json', 'vagasrio_python.json']
        self.var_arquivos = ctk.StringVar(value='vagasrio.json')
        self.combo = ctk.CTkComboBox(self.root,values=self.arquivos, width=200, command=self.combobox_callback)
        self.combo['values'] = ('vagasrio.json', 'vagasrio_python.json')
        self.combo.place(x=350, y=10)
        self.combo.set('vagasrio.json')
        self.real_page1 = 1
        self.real_page2 = 1
        self.contagem = 0
        self.parse_vagas_python = [1] #remmover
        self.descricao_scroll = ctk.CTkTextbox(self.root, activate_scrollbars=True, width=800, height=800)
        self.descricao_scroll.place(x=5,y=70)
        self.max_words = 16 # configura em quantas palavras vai espaçar; todo: adicionar as configurações
        self.garimpar_qnt_paginas = 2
        # todo: fazer uma pesquisa por palavras chaves, exibir resultados em lista, ao clicar exibir o resultado e habilitar para o next
        self.job_handle = None
    def atualizar_infos(self):
        json_file = self.combo.get()
        if json_file == 'vagasrio.json':
            texto = f'{self.contagem}/{self.contar_tarefas()}'
            if self.contagem == self.contar_tarefas():
                self.contagem = 1
            self.qt_label.configure(text=texto)
        elif json_file == 'vagasrio_python.json':
            vagas = busca_vagas4.read_json(json_file)
            qnt_vagas_python = len(vagas)
            texto = f'{self.real_page1}/{qnt_vagas_python}'
            self.qt_label.configure(text=texto)

    def load_order(self):
        load = self.var_arquivos.get()
        arquivo = busca_vagas4.read_json(load)
        quantidade = len(list(arquivo))
    def better_next(self):
        load = self.var_arquivos.get()
        arquivo = busca_vagas4.read_json(load)
        descricao = None
        if not self.previous_btt.winfo_exists():
            self.previous_btt.place(x=720, y=10)
        if load == 'vagasrio.json':
            try:
                # if self.contagem == self.contar_tarefas():
                #     self.contagem = 1
                #     self.real_page1 = 1
                #     self.real_page2 = 1

                descricao = arquivo[f'{self.real_page1}'][f'{self.real_page2}']['descricao']
                descricao = descricao.replace('\n\n', '\n')
                link1 = arquivo[f'{self.real_page1}'][f'{self.real_page2}']['link_vaga']
                logger.debug(f"vagasrio.json: {self.real_page1}, tarefa: {self.real_page2}")
                jobs = len(list(arquivo[f'{self.real_page1}']))
                if jobs == self.real_page2:
                    self.real_page2 = 1
                    self.real_page1 += 1
                    self.contagem += 1

                else:
                    self.real_page2 += 1
                    self.contagem += 1
            except KeyError:
                print('Não há mais vagas para prosseguir. Resetando...')
                self.real_page1 = 1
                self.real_page2 = 1
                self.contagem = 1
                # logger.debug(f"vagasrio.json: {self.real_page1}, tarefa: {self.real_page2}")
                # descricao = arquivo[f'{self.real_page1}'][f'{self.real_page2}']['descricao']
                # descricao = descricao.replace('\n\n', '\n')
                # link1 = arquivo[f'{self.real_page1}'][f'{self.real_page2}']['link_vaga']

        elif load == 'vagasrio_python.json':
            descricao = arquivo[f'{self.real_page1}']['descricao']
            descricao = descricao.replace('\n\n', '\n')
            link1 = arquivo[f'{self.real_page1}']['link_vaga']
            if len(list(arquivo)) != self.real_page1:
                self.real_page1 += 1
            else:
                self.real_page1 = 1
            #link2 = arquivo[f'{self.real_page1}']['link_candidatura']
        #self.descricao_scroll.configure(text=f'\nDescrição:\n{descricao}', justify='left', wraplength=900)
        self.atualizar_infos()
        try:
            #self.root.after(100, self.atualizar_infos())
            self.descricao_scroll.configure(state='normal')
            self.descricao_scroll.delete('0.0', "end")
            self.descricao_scroll.insert('0.0', descricao)
            self.descricao_scroll.configure(state='disable')
        except:
            print("Não foi possível inserir a descrição;")
    def better_previous(self):
        load = self.var_arquivos.get()
        arquivo = busca_vagas4.read_json(load)
        descricao = None
        #resolver keyerro 0
        print(self.real_page1, self.real_page2)
        if self.real_page2 == 0 or self.real_page1 == 0:
            self.previous_btt.place_forget()
            if self.real_page2 == 0:
                self.real_page2 = 2
            elif self.real_page1 == 0:
                self.real_page1 = 2
        # else:
        #     self.previous_btt.place(x=720, y=10)
        if load == 'vagasrio.json':

            if len(list(arquivo)) != 1:
                jobs = len(list(arquivo[f'{self.real_page1}']))
                if jobs == self.real_page2:
                    self.real_page2 -= 1
                    #self.real_page1 -= 1
                elif self.real_page2 == 1:
                    if not self.real_page1 == 1:
                        self.real_page1 -= 1
                        self.real_page2 = len(list(arquivo[f'{self.real_page1}']))
                elif self.real_page2 == 0:
                    self.real_page2 = 1

                else:
                    self.real_page2 -= 1
            else:
                self.real_page1 = 1
            logger.debug(f"vagasrio.json: {self.real_page1}, tarefa: {self.real_page2}")
            descricao = arquivo[f'{self.real_page1}'][f'{self.real_page2}']['descricao']
            descricao = descricao.replace('\n\n', '\n')
            link1 = arquivo[f'{self.real_page1}'][f'{self.real_page2}']['link_vaga']
        elif load == 'vagasrio_python.json':
            # if len(list(arquivo)) != 1:
            #     jobs = len(list(arquivo[f'{self.real_page1}']))
            #     if jobs == self.real_page2:
            #         self.real_page2 -= 1
            #     elif self.real_page2 == 1:
            #         if not self.real_page1 == 1:
            #             self.real_page1 -= 1
            #     elif self.real_page2 == 0:
            #         self.real_page2 = 1
            #     else:
            #         self.real_page2 -= 1
            # else:
            #     self.real_page1 = 1

            if len(list(arquivo)) != 1:
                self.real_page1 -= 1
            elif self.real_page2 == 1:
                self.real_page1 -= 1
                self.real_page2 = len(list(arquivo[f'{self.real_page1}']))
            else:
                self.real_page1 = 1
            descricao = arquivo[f'{self.real_page1}']['descricao']
            descricao = descricao.replace('\n\n', '\n')
            link1 = arquivo[f'{self.real_page1}']['link_vaga']
            # link2 = arquivo[f'{self.real_page1}']['link_candidatura']
        self.descricao_scroll.configure(state='normal')
        self.descricao_scroll.delete('0.0', "end")
        self.descricao_scroll.insert('0.0', descricao)
        self.descricao_scroll.configure(state='disable')

    def combobox_callback(self, choice):
        self.var_arquivos.set(choice)
        #load = busca_vagas4.read_json(choice)
        self.real_page1 = 1
        self.real_page2 = 1
        self.qt_label.configure(text=f'')
        print("combobox dropdown clicked:", choice)

    def vagas_python(self):
        vagas = list(self.vagas)
        vagas_python = {}
        contagem = 1
        for vaga in vagas:
            items = list(self.vagas[vaga])
            for item in items:
                descricao = self.vagas[vaga][item]["descricao"]
                for key in self.keywords:
                    if key in descricao:
                        vagas_python[contagem] = {'pagina': vaga,
                                                  'vaga_num': item,
                                                  'descricao': descricao,
                                                  'link_vaga':self.vagas[vaga][item]["link_vaga"],
                                                  'link_candidatura': self.vagas[vaga][item]["link_candidatura"],
                                                  "data-hora": self.vagas[vaga][item]["data-hora"],
                                                  "salario": self.vagas[vaga][item]["salario"],
                                                  }
                        contagem +=1
        busca_vagas4.save_json('vagasrio_python.json', vagas_python)
        logger.debug(f'{len(list(vagas_python))} Vagas de python encontradas. ')

    def contar_tarefas(self):
        paginas = list(self.vagas)
        qnt_paginas = len(paginas)
        qnt_vagas = 0
        for pagina in paginas:
            itens = list(self.vagas[f"{pagina}"])
            qnt_vagas = qnt_vagas + len(itens)
        #print(qnt_vagas)
        return qnt_vagas

    def verificar_estado_do_processo(self):
        if self.job_handle.is_alive():
            # Se o processo ainda estiver em execução, verifica novamente após 1000ms
            self.root.after(1000, self.verificar_estado_do_processo)
        else:
            # O processo terminou
            self.buscar.configure(state="normal")
            self.buscar.configure(text='Garimpar')

    def garimpar(self):
        self.buscar.configure(text='Garimpando')
        self.job_handle = multiprocessing.Process(target=busca_vagas4.trabalhos, args=(self.garimpar_qnt_paginas,))
        self.job_handle.start()
        self.buscar.configure(state="disabled")
        # Verifica o estado do processo em intervalos regulares
        self.root.after(100, self.verificar_estado_do_processo)
    def candidatar_se(self):
        webbrowser.open(self.link_candidatura_tarefa)
    def ver_on_site(self):
        webbrowser.open(self.linkvaga_tarefa)
    def next(self):
        pagina = self.tarefa_atual[0]
        tarefa = self.tarefa_atual[1]
        logger.debug(f"Página: {pagina}, tarefa: {tarefa}")
        self.des_tarefa = self.vagas[f'{pagina}'][f'{tarefa}']['descricao']
        self.des_tarefa = self.des_tarefa.replace('\n\n','\n')
        self.linkvaga_tarefa = self.vagas[f'{pagina}'][f'{tarefa}']['link_vaga']
        self.link_candidatura_tarefa = self.vagas[f'{pagina}'][f'{tarefa}']['link_candidatura']
        self.descricao.configure(text=f'\nDescrição:\n{self.des_tarefa}', justify='left', wraplength=900)
        self.linklabel.configure(text=f'{self.linkvaga_tarefa}')
        vagas_na_pagina = len(self.vagas[f'{pagina}'])
        if vagas_na_pagina == tarefa:
            self.tarefa_atual[0] = pagina+1
            self.tarefa_atual[1] = 1
        else:
            self.tarefa_atual[1] = tarefa + 1
    def previous(self):
        pagina = self.tarefa_atual[0]
        tarefa = self.tarefa_atual[1]
        logger.debug(f"Página: {pagina}, tarefa: {tarefa}")
        self.des_tarefa = self.vagas[f'{pagina}'][f'{tarefa}']['descricao']
        self.des_tarefa = self.des_tarefa.replace('\n\n','\n')
        self.linkvaga_tarefa = self.vagas[f'{pagina}'][f'{tarefa}']['link_vaga']
        self.link_candidatura_tarefa = self.vagas[f'{pagina}'][f'{tarefa}']['link_candidatura']
        self.descricao.configure(text=f'\nDescrição:\n{self.des_tarefa}', justify='left', wraplength=900)
        vagas_na_pagina = len(self.vagas[f'{pagina}'])
        if vagas_na_pagina == tarefa:
            self.tarefa_atual[0] = pagina-1
            self.tarefa_atual[1] = 1
        else:
            self.tarefa_atual[1] = tarefa - 1


        #self.tarefa_atual[0]

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("VagasRio")
    #root.iconbitmap(assegurar_arquivo("imagens\\icon.ico"))
    root.resizable(width=False, height=True)
    app = Visualizador(root)
    root.mainloop()
