from pytube import YouTube, Playlist
from pytube.exceptions import PytubeError
from pytube.helpers import safe_filename
from tqdm import tqdm
import os

def get_audio_stream(video):
    """
    Obtém a melhor stream de áudio disponível para download.
    """
    # Filtra apenas as streams de áudio
    audio_streams = video.streams.filter(only_audio=True)
    # Ordena as streams pelo valor de "abr" (bitrate de áudio)
    audio_streams = audio_streams.order_by("abr").desc()
    if audio_streams:
        # Retorna a melhor stream de áudio
        return audio_streams.first()
    return None

def download_song(video_url, output_path=""):
    try:
        # Obtém o objeto de vídeo a partir da URL
        video = YouTube(video_url)
        # Obtém a melhor stream de áudio disponível
        audio_stream = get_audio_stream(video)
        if audio_stream:
            # Define o nome do arquivo de saída com base no título do vídeo
            filename = safe_filename(video.title) + ".mp3"
            # Verifica o tipo de mime da stream de áudio
            if audio_stream.mime_type == 'audio/webm':
                # Atualiza o nome do arquivo se for um formato webm
                filename = safe_filename(video.title) + ".webm"
            # Define o caminho completo do arquivo de saída
            output_file = os.path.join(output_path, filename) if output_path else filename
            # Verifica se o arquivo já existe e possui tamanho maior que 0
            if os.path.isfile(output_file) and os.path.getsize(output_file) > 0:
                print(f"Arquivo já existe: {output_file}")
            else:
                # Realiza o download da stream de áudio
                audio_stream.download(output_path=output_path, filename=filename, skip_existing=True)
                print(f"Download concluído: {output_file}")
        else:
            print(f"Erro: Não foi possível encontrar a versão de áudio do vídeo {video_url}")
    except PytubeError as e:
        print(f"Erro ao fazer o download de {video_url}: {str(e)}")

def download_playlist(playlist_url, output_path=""):
    try:
        playlist = Playlist(playlist_url)
        playlist.populate_video_urls()
        playlist_title = playlist.title
        print(f"Baixando playlist: {playlist_title}")
        for video_url in playlist.video_urls:
            download_song(video_url, output_path=output_path)
    except PytubeError as e:
        print(f"Erro ao fazer o download da playlist {playlist_url}: {str(e)}")
'''------------------------------↑↑↑↑↑↑ Heart of the program ↑↑↑↑↑↑↑ --------------------------------------'''
# Exemplo de uso
# song_url = "https://www.youtube.com/watch?v=Uo_1cK8X_wM"  # Substitua pela URL da música desejada
# download_song(song_url, output_path="D:\\Users\\remote\\Music")

#playlist_url = "https://youtube.com/playlist?list=PLYH4VConX3TQPJkIW3q9IkCFFbYzxrkOh"  # Substitua pela URL da playlist desejada
# download_playlist(playlist_url, output_path="D:\\Users\\remote\\Music")

# uso prático:
normal_path = "D:\\Users\\remote\\Music"  # json
'''options = input("[1] Baixar músicas\n"
                "[2] Baixar playlist\n"
                "[3] Baixar playlist privada"
                "\n\ndigite a opção desejada: ")'''
# mus_atual = input("insira o link do youtube da música que deseja baixar:")
download_song('https://www.youtube.com/watch?v=4gsjCOEoJGg', normal_path)
'''print(options)
if options == 1:
    mus_atual = input("insira o link do youtube da música que deseja baixar:")
    download_song(mus_atual, normal_path)
elif options == 2:
    playlist_atual = input("insira o link da playlist do youtube que deseja baixar")
    download_playlist(playlist_atual, normal_path)
elif options == 3:
    playlist_privada = input("insira o link da playlist privada")
    print("em desenvolvimento")'''