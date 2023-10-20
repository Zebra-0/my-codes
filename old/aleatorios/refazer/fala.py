import speech_recognition as sr
import tkinter as tk
from threading import Thread

r = sr.Recognizer()


class TranscricaoThread(Thread):
    def __init__(self, label):
        Thread.__init__(self)
        self.label = label
        self.parar = False

    def run(self):
        with sr.Microphone() as source:
            while not self.parar:
                try:
                    audio = r.listen(source, timeout=1)
                    texto = r.recognize_google(audio, language='pt-BR')
                    self.label.config(text=texto)
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    self.label.config(text="Não foi possível entender o áudio")
                except sr.RequestError as e:
                    self.label.config(text="Erro ao tentar transcrever o áudio; {0}".format(e))


def transcrever():
    global thread
    texto.config(text="Diga algo...")
    thread = TranscricaoThread(texto)
    thread.start()


def parar():
    thread.parar = True


janela = tk.Tk()

botao = tk.Button(janela, text="Transcrever", command=transcrever)
botao.pack()

botao_parar = tk.Button(janela, text="Parar", command=parar)
botao_parar.pack()

texto = tk.Label(janela, text="Clique no botão para transcrever")
texto.pack()

janela.mainloop()
