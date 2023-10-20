import pytesseract
import pyaudio
import numpy as np
import cv2
import pyscreenshot as ImageGrab
from PIL import Image
from googletrans import Translator
import time
import pyttsx3
def capture_screen():
    screen = np.array(ImageGrab.grab(bbox=(0,0,800,600)))
    text = pytesseract.image_to_string(Image.fromarray(screen))
    return text

def speak(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='pt').text # traduzindo para portugues
    engine = pyttsx3.init()
    engine.say(translated_text)
    engine.runAndWait()

while True:
    text = capture_screen()
    speak(text)
    time.sleep(1)

