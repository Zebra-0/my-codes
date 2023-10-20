import customtkinter
import tkinter as tk
from tkinter import ttk
import bot_sprout
def automacao():
    bot_sprout.setup(link_curto.get(), int(codigo_na.get()))

janela = customtkinter.CTk()
janela.geometry("500x500")
janela.resizable(False, False)
texto = customtkinter.CTkLabel(janela, text="Inserir link curto")
texto.pack(padx=10, pady=10)
link_curto = customtkinter.CTkEntry(janela, width=400)
link_curto.pack(padx=10, pady=10)
texto_codigo = texto = customtkinter.CTkLabel(janela, text="O código vai aparecar na página")
texto_codigo.pack(padx=10, pady=10)
codigo_na = customtkinter.CTkEntry(janela, width=50)
codigo_na.pack(padx=10, pady=10)
iniciat_btt = customtkinter.CTkButton(janela, text="iniciar", command=automacao)
iniciat_btt.pack(padx=10, pady=10)
# chrome_is_open = customtkinter.CTkCheckBox(janela, text="Chrome já está aberto")
# chrome_is_open.pack(padx=10, pady=10)
# print(chrome_is_open.get())
janela.mainloop()





