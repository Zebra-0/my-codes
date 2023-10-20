import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
import openai
# tudo precisamos de duas variasveis para a escuta e transcrição
audio = sr.Recognizer()
maquina = pyttsx3.init()
def listen_command():
    try:
        with sr.Microphone() as source:
            print("Escutando...")
            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'jarvis' in comando:
                comando = comando.replace('jarvis','')
                maquina.say(comando)
                maquina.runAndWait()

    except Exception as e:
        print(f'um errno inesperado aconteceu {e}')
    return comando


def execute_command():
    comando = listen_command()
    if 'procure por' in comando or 'pesquise por' in comando:
        procurar = comando.replace('procure por', '')
        wikipedia.set_lang('pt')
        resultado = wikipedia.summary(procurar)
        print(resultado)
        maquina.say(resultado)
        maquina.runAndWait()

    elif 'toque' in comando:
        musica = comando.replace('toque','')
        resultado = pywhatkit.playonyt(musica)
        maquina.say(f'tocando {musica} no youtube')
        maquina.runAndWait()
    else:
        pass

while True:
    execute_command()