import sys
from cx_Freeze import setup, Executable

# Defina a lista de pastas e arquivos que você deseja incluir
include_files = [
    ("imagens\\", "imagens"),  # Copia a pasta1 para o diretório do executável
    ("audio-video\\", "audio-video"),  # Copia a pasta2 para o diretório do executável
    ("presets.json", "presets.json"),  # Copia o arquivo1.txt para o diretório do executável
    ("simpleMusicDownloader.py", "simpleMusicDownloader.py"),  # Copia o arquivo1.txt para o diretório do executável
]
executables01 = ["interface_SMD045.py", "simpleMusicDownloader.py"]
base = None
executar = []
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" para criar um aplicativo sem console no Windows

executables = [Executable("interface_SMD045.py", base=base)]
setup(
    name="interface_SMD045",
    version="0.45",
    description="Descrição do Seu Programa",
    executables=executables,
    options={
        "build_exe": {
            "include_files": include_files  # Especifica os arquivos e pastas a serem incluídos
        }
    }
)
