import wave
import pyaudio
import threading
from datetime import datetime
import os
class Audio():
    def __init__(self):
        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 48000
        self.RECORD_SECONDS = 20
        self.current_output_device = 1
        print(self.p.get_device_info_by_index(self.current_output_device))
    def file_name(self):
        global recording
        global atual_file
        while recording:
            pass  # Aguarde até que a gravação termine

        data = datetime.now()
        hoje = data.strftime('%d-%m-%Y')
        hora = data.strftime('%H:%M:%S')
        self.nome_arquivo = 'audiorecord.wav'
        self.nome_atualizado = f'{self.nome_arquivo} {hoje} {hora.replace(":","")}.wav'
        original = 'output.wav'
        try:
            os.rename(original, self.nome_atualizado)
            print(f"O arquivo foi renomeado para {self.nome_atualizado}")
            atual_file = self.nome_atualizado
        except PermissionError as e:
            print(f"Erro ao renomear o arquivo: {e}")        #return str(self.nome_atualizado)
    def index_dispositivos(self):
        print("Available input devices:")
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"Index {i}: {info['name']}")

        print("Available output devices:")
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info['maxOutputChannels'] > 0:
                print(f"Index {i}: {info['name']}")
    def gravar(self):
        # Create a WAV file for writing
        global recording
        recording = True
        with wave.open(f'output.wav', 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)

            # Open a stream for recording from the default output device
            stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                 input=True, input_device_index=self.current_output_device)

            print('Recording...')

            # Record audio and write it to the WAV file
            for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
                wf.writeframes(stream.read(self.CHUNK))

            print('Done')

            # Close the stream and terminate PyAudio
            stream.close()
            self.p.terminate()
            recording = False

record = threading.Thread(target=Audio().gravar)
renomear_thread = threading.Thread(target=Audio().file_name)

record.start()
renomear_thread.start()