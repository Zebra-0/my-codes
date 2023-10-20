from pytube import YouTube, Playlist
import sys
from moviepy.audio.io.AudioFileClip import AudioFileClip

# fazer um conversor para mp3


# versão 0.4.3
# conversor para mp3 adicionado
# separe o progama em passos✔
# verificar se arquivo já existe
def verificar_duplicados(link, pasta):
    nome_arquivo = link_data(link)
    nome_arquivo = nome_arquivo.title
    if len(nome_arquivo) in pasta:
        print("arquivo já existe")
        return False
    if not len(nome_arquivo) in pasta:
        print("O arquivo não está duplicado.")
        return True
# configurando progress bar para o link
def link_data(link):
    data = YouTube(link, on_progress_callback=barra_de_progresso)
    return data

# verificando se o link é válido ✔
def validador_de_link(link):
    if "youtube.com/" in link or "youtu.be/" in link:
        if "youtube.com/playlist" in link:
            msg4 = "link validado - Playlist encontrada"
            print(msg4)
            validador = "Playlist"
            return validador
        else:
            msg0 = "Link validado"
            print(msg0)
            validador = "único"
            return validador

    else:
        msg1 = "Link inválido, favor verificar"
        print(msg1)
        validador = False
        # print("Fechando programa")
        return validador

# configura o path para áudio ou vídeo
def path_config(option=0):
    # muda o path de escolher entre vídeo ou música
    if option == 0:
        print("salvando na pasta do programa.")
        return "D:\\Users\\remote\\Music"
    if option == 1:
        video_path = "D:\\Users\\remote\\Music"
        return video_path
    elif option == 2:
        audio_path = "D:\\Users\\remote\\Videos"
        return audio_path


# opção para baixar vídeo
def baixar_video(link, mostrar_notificacao=True):
    # baixa o vídeo na resolução mais alta.

    if mostrar_notificacao:
        msg2 = f"baixando {link_data(link).title} na melhor resolução disponível"
        print(msg2)
    mp4_video = link_data(link).streams.get_highest_resolution() \
        .download(output_path=path_config(2))



# opção para baixar em formato de música
def baixar_audio(link, mostrar_notificacao=True, ret=False):
    # baixa audio com melhor bitrate.
    if mostrar_notificacao:
        msg3 = "baixando áudio na melhor resolução disponível"
        print(msg3)
    # interface.Programa.link_data()
    mp4_audio = link_data(link).streams.get_audio_only().download(output_path=path_config(1))


# adicionar opção para baixar playlist
def baixar_video_playlist(link):
    video_playlist = Playlist(link)
    print("Iniciando download da playlist")
    for video in video_playlist.videos:
        print(f"Baixando vídeo: {video.title}")
        url = video.watch_url
        baixar_video(url, False)
        # video.streams.get_highest_resolution().download(output_path=path_config(2))
    print("Download concluído")


# opção para baixar playlist em áudio
def baixar_audio_playlist(link):
    audio_playlist = Playlist(link)
    print("Iniciando download de audio da playlist")
    for audio in audio_playlist.videos:
        print(f"\nBaixando {audio.title}")
        url = audio.watch_url
        baixar_audio(url, False)
        # audio.streams.get_audio_only().download(output_path=path_config(1))
    print("\nDownload concluído")

# teste da barra de progresso
def barra_de_progresso(stream, chunk, faltando):
    tamanho_total = stream.filesize
    bytes_baixados = tamanho_total - faltando

    if tamanho_total > 0:
        progresso = (bytes_baixados / tamanho_total) * 100
        sys.stdout.write(f"\rProgresso: {progresso:.2f}%\n")  # - {bytes_baixados}/{tamanho_total} bytes")
        sys.stdout.flush()

    else:
        print("Progresso: Indisponível")
def mp4_mp3(mp4, mp3):
    para_converter = AudioFileClip(mp4)
    para_converter.write_audiofile(mp3)
    para_converter.close()




# organizar entre formato de vídeo e áudio
# opção manual de download (escolher)
# opção automática para download
# verificar se há tracklist e separar arquivos.
# ________________________________________________________________________
# inicializando programa

# insira um link do youtube ✔
#print("Bem-vindo ao SMD!")

#link = input("Insira o link: ")
#if not validador_de_link(link):
#    quit()

#baixar_audio(link)
