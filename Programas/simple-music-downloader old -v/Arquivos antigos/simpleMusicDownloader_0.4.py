from pytube import YouTube, Playlist
from pytube.cli import display_progress_bar
from pytube.exceptions import PytubeError
from pytube.helpers import safe_filename
import os
import sys
from tqdm import tqdm
# separe o progama em passos✔
# verificar se arquivo já existe

# verificando se o link é válido ✔
def validador_de_link(link):
    if "youtube.com/" in link or "youtu.be/" in link:
        msg0 = "Link validado"
        print(msg0)
        validador = True
        return validador
    elif "youtube.com/playlist" in link:
        msg4 = "link validado - Playlist encontrada"
        print(msg4)
        validador = True
        return validador
    else:
        msg1 = "Link inválido, favor verificar"
        print(msg1)
        validador = False
        print("Fechando programa")
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


def link_config(link):
    config = YouTube(link, on_progress_callback=barra_de_progresso)
    return config


# opção para baixar vídeo
def baixar_video(link):
    # baixa o vídeo na resolução mais alta.
    msg2 = f"baixando {link_config(link).title} na melhor resolução disponível"
    print(msg2)
    mp4_video = link_config(link).streams.get_highest_resolution() \
        .download(output_path=path_config(2))
    return mp4_video


# opção para baixar em formato de música
def baixar_audio(link):
    # baixa audio com melhor bitrate.
    msg3 = "baixando áudio na melhor resolução disponível"
    print(msg3)
    mp4_audio = link_config(link).streams.get_audio_only().download(output_path=path_config(1))
    return mp4_audio


# adicionar opção para baixar playlist
def baixar_video_playlist(link):
    video_playlist = Playlist(link)
    print("Iniciando download da playlist")
    for video in video_playlist.videos:
        print(f"Baixando vídeo: {video.title}")
        video.streams.get_highest_resolution().download(output_path=path_config(2))
    print("Download concluído")


# opção para baixar playlist em áudio
def baixar_audio_playlist(link):
    audio_playlist = Playlist(link)
    print("Iniciando download de áudio da playlist")
    for audio in tqdm(audio_playlist.videos, desc="Baixando áudios", unit="audio"):
        print(f"Baixando {audio.title}")
        audio.streams.get_audio_only().download(output_path=path_config(1))
    print("Download concluído")
# opção para baixar playlist em áudio
def baixar_audio_playlist0(link):
    audio_playlist = Playlist(link)
    print("Iniciand download de audio da playlist")
    for audio in audio_playlist.videos:
        print(f"Baixando {audio.title}")
        audio.streams.get_audio_only().download(output_path=path_config(1))
    print("Download concluído")


# barra de progresso
def barra_de_progresso(stream, chunk, faltando):
    tamanho_total = stream.filesize
    bytes_baixados = tamanho_total - faltando

    if tamanho_total > 0:
        progresso = (bytes_baixados / tamanho_total) * 100
        sys.stdout.write(f"\rProgresso: {progresso:.2f}%")  # - {bytes_baixados}/{tamanho_total} bytes")
        sys.stdout.flush()
    else:
        print("Progresso: Indisponível")


# organizar entre formato de vídeo e áudio
# opção manual de download (escolher)
# opção automática para download

# ________________________________________________________________________
# inicializando programa

# insira um link do youtube ✔
print("Bem-vindo ao SMD!")
link = input("Insira o link: ")

if not validador_de_link(link):
    quit()

baixar_audio_playlist(link)
