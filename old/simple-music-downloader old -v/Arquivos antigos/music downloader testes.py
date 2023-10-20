import subprocess
from pytube import YouTube, Playlist
from pprint import pprint
from pytube.exceptions import PytubeError
from pytube.helpers import safe_filename
from tqdm import tqdm
import os
import re
from tkinter import filedialog


class YoutubeEngine():
    "Trata e baixa vídeos ou áudios do youtube conforme a preferência."

    def get_video_data(self, link: str):
        self.yv = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        return self.yv

    def show_video_data(self):
        if hasattr(self, 'yv'):
            self.titulo = self.yv.title
            self.tumbnail_url = self.yv.thumbnail_url
            self.descricao = self.yv.description
            self.duracao = self.yv.length
            self.url = self.yv.watch_url
            self.video_data = f'''
            informações do vídeo
            título: {self.titulo}
            tumbnail url: {self.tumbnail_url}
            descrição: {self.descricao}
            duração: {self.duracao // 60}:{self.duracao % 60:02}
            URL: {self.url}
            '''
        else:
            erro0 = "Nenhum vídeo foi obtido ainda ou há um um erro em get_video_data"
            print(erro0)

    def get_video_streams_disponiveis_teste(self):
        # Obtém todos os streams disponíveis do vídeo
        self.streams = self.yv.streams

        # Cria uma lista vazia para armazenar as opções de stream
        self.stream_options = []

        # Itera sobre os streams disponíveis
        for stream in self.streams:
            # Cria um dicionário com informações relevantes do stream
            option = {
                'itag': stream.itag,
                'mime_type': stream.mime_type,
                'resolution': stream.resolution,
                'video_codec': stream.video_codec,
                'audio_codec': stream.audio_codec,
                'is_progressive': stream.is_progressive,
                'type': stream.type
            }

            # Adiciona a opção à lista de opções
            self.stream_options.append(option)

        # Filtra as opções com resolução não nula
        self.stream_options = [option for option in self.stream_options if option['resolution'] is not None]

        # Ordena a lista de opções por resolução (do menor para o maior)
        self.stream_options = sorted(self.stream_options, key=lambda x: x['resolution'])

        # Exibe as opções de stream disponíveis para o usuário
        self.exibir_opcoes_teste()

    def exibir_opcoes_teste(self):
        print("Opções de stream disponíveis:\n")
        for index, option in enumerate(self.stream_options, start=1):
            print(f"Opção {index}:")
            print(f"  - Resolução: {option['resolution']}")
            print(f"  - Codec de vídeo: {option['video_codec']}")
            print(f"  - Codec de áudio: {option['audio_codec']}")
            print(f"  - Tipo: {option['type']}")
            print()

    def format_stream_audio_info(self, stream_info):
        # Define os padrões de regex para as informações desejadas
        patterns = {
            "itag": r'itag="(\d+)"',
            "mime_type": r'mime_type="([^"]+)"',
            "abr": r'abr="([^"]+)"',
            "acodec": r'acodec="([^"]+)"',
            "progressive": r'progressive="([^"]+)"',
            "type": r'type="([^"]+)"'
        }

        # Aplica os padrões de regex para extrair as informações
        formatted_info = []
        for key, pattern in patterns.items():
            match = re.search(pattern, stream_info)
            if match:
                value = match.group(1)
                formatted_info.append(f"{key}: {value}")

        # Retorna as informações formatadas como uma string
        return "\n".join(formatted_info)

    def get_audio_stream_info(self):
        self.audio_streams = self.yv.streams.filter(only_audio=True).order_by("abr").desc()
        full_info = []
        for stream in self.audio_streams:
            stream_info = str(stream)  # Converte o objeto Stream para string
            formatted_info = self.format_stream_audio_info(stream_info)
            # print(f"Stream:\n{formatted_info}\n")
            full_info.append(f"Stream:\n{formatted_info}\n")
        for info in full_info:
            print(info)
        return full_info

    def get_mp4_stream_info(self):
        data = self.yv
        data.streams.filter(file_extension='mp4')

    def save_on_path(self):
        main_path = "D:\\Users\\remote\\Music"
        return main_path

    def get_list_of_streams(self):

        # Defina o comando que você deseja executar
        comando = 'pytube https://www.youtube.com/watch?v=2lAe1cqCOXo --list'

        # Execute o comando no CMD
        output_bytes = subprocess.check_output(comando, shell=False)
        output_str = output_bytes.decode('utf-8')
        # Expressão regular para extrair os dados entre as tags "<Stream>" e "</Stream>"
        expressao_regular = r'<Stream:.*?>'

        # Encontra todos os matches na string de dados
        matches = re.findall(expressao_regular, output_str)
        self.list_of_streams = []
        # Imprime os matches encontrados
        for match in matches:
            self.list_of_streams.append(match)
            print(match)
        print(self.list_of_streams)
        return self.list_of_streams
    def filter_streams_by_itag(self):
        expressoes = {
            'itag': r'itag="(\d+)"',
            'mime_type': r'mime_type="([^"]+)"',
            'res': r'res="([^"]+)"',
            'fps': r'fps="([^"]+)"',
            'vcodec': r'vcodec="([^"]+)"',
            'acodec': r'acodec="([^"]+)"',
            'progressive': r'progressive="([^"]+)"',
            'type': r'type="([^"]+)"'
        }

        dados = {}
        item1 = 0
        contagem = len(self.list_of_streams)
        while contagem != 0:
            for chave, expressao in expressoes.items():
                match = re.search(expressao, self.list_of_streams[item1+1])
                if match:
                    valor = match.group(1)
                    dados[chave] = valor
            contagem -= 1
        print(dados)

if __name__ == "__main__":
    engine = YoutubeEngine()
    video_link = "https://www.youtube.com/watch?v=lZxln_egw-w"
    engine.get_video_data(video_link)
    engine.show_video_data()
    # engine.get_video_streams_disponiveis_teste()
    # engine.get_audio_stream_info()
    engine.get_list_of_streams()
    engine.filter_streams_by_itag()