import pandas as pd
import csv
import time
aluno = ["João","Maria","Pedro","Carla"]
notas = [10,9,9,10]

info = {"aluno":aluno, "notas":notas}

df = pd.DataFrame(info)

df.to_csv("demo.csv")
# time.sleep(5)
with open("demo.csv", "r") as demo:
    demo_csv = csv.reader(demo, delimiter=",")
    for i, linha in enumerate(demo_csv):
        if i == 0:
            print("cabeçalho" + str(linha))
        else:
            print("valor" + str(linha))