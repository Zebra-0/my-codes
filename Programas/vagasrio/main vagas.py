import customtkinter as ctk
import busca_vagas4
import webbrowser
from loguru import logger

# iniciar busca dos dados
# exibir 1 por um ao clicar em próximo
#
class Visualizador:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x800')
        #self.dados_tarefa()
        self.descricao = ctk.CTkLabel(self.root, text='Clique em Próxima para iniciar',font=('Arial',15), justify='left', wraplength=900)
        self.descricao.place(x=10, y=50)
        self.next_btt = ctk.CTkButton(self.root, text='Proxima', command=self.next)
        self.previous_btt = ctk.CTkButton(self.root, text='Anterior', command=self.previous)
        self.next_btt.place(x=870, y=10)
        self.previous_btt.place(x=720, y=10)
        self.candidatar_btt = ctk.CTkButton(self.root, text="Candidatar-se", command=self.candidatar_se)
        self.candidatar_btt.place(x=870, y=40)
        self.vernosite_btt = ctk.CTkButton(self.root, text="Ver no site", command=self.ver_on_site)
        self.vernosite_btt.place(x=870, y=70)


        self.vagas = busca_vagas4.read_json('vagasrio.json')
        self.paginas = len(self.vagas)
        self.des_tarefa = None
        self.linkvaga_tarefa = None
        self.link_candidatura_tarefa = None
        self.tarefa_atual = [1,1]
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
    root.title("Vagas")
    #root.iconbitmap(assegurar_arquivo("imagens\\icon.ico"))
    root.resizable(width=False, height=False)
    app = Visualizador(root)
    root.mainloop()
