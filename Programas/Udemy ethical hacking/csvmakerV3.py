import pandas as pd
import csv
import time
aluno = ["João","Maria","Pedro","Carla"]
notas = [10,9,9,10]
info = {"aluno":aluno, "notas":notas}
df = pd.DataFrame(info)
df.to_csv("demo.csv")
# time.sleep(5)
print(pd.read_csv("demo.csv"))

