import tkinter as tk
from tkinter import filedialog, scrolledtext

class Mission:
    def __init__(self, name, difficulty, points):
        self.name = name
        self.difficulty = difficulty
        self.points = points
        self.completed = False

    def toggle_completed(self):
        self.completed = not self.completed

class PersonProfile:
    def __init__(self, root):
        self.root = root
        self.root.title("Perfil da Pessoa")

        # Criar campos de entrada para o nome, idade e gênero
        tk.Label(self.root, text="Nome:").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)
        tk.Label(self.root, text="Idade:").grid(row=1, column=0)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1)
        tk.Label(self.root, text="Gênero:").grid(row=2, column=0)
        self.gender_entry = tk.Entry(self.root)
        self.gender_entry.grid(row=2, column=1)

        # Criar botão para fazer o download da foto
        self.photo_button = tk.Button(self.root, text="Foto", command=self.download_photo)
        self.photo_button.grid(row=0, column=2)

        # Criar widget de rolagem para exibir a lista de missões
        self.mission_scroll = scrolledtext.ScrolledText(self.root, width=30, height=10)
        self.mission_scroll.grid(row=3, column=0, columnspan=3)


        # Criar botão para exibir o perfil
        self.display_button = tk.Button(self.root, text="Exibir Perfil", command=self.display_profile)
        self.display_button.grid(row=4, column=1)

        # Inicialmente, a foto é uma etiqueta vazia
        self.photo_label = tk.Label(self.root, text="")
        self.photo_label.grid(row=5, column=1)

        # Criar lista de instâncias da classe Mission
        self.missions = [
            Mission("Instalar e configurar software em computadores pessoais", "Fácil", 10),
            Mission("Realizar backups de dados", "Fácil", 10),
            Mission("Instalar e configurar impressoras e outros dispositivos de hardware", "Fácil", 10),
            Mission("Criar e gerenciar contas de usuário em sistemas operacionais", "Fácil", 10)]

    def download_photo(self):
        # Exibir janela de diálogo para fazer o download da foto
        file_path = filedialog.askopenfilename()
        if file_path:
            # Exibir a foto na etiqueta
            self.photo = tk.PhotoImage(file=file_path)
            self.photo = self.photo.subsample(5, 5)  # Reduzir a imagem para 20% do tamanho original
            self.photo_label.configure(image=self.photo)
            self.photo_label.image = self.photo

    def display_profile(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        profile_text = f"Nome: {name}\nIdade: {age}\nGênero: {gender}"
        tk.Label(self.root, text=profile_text).grid(row=5, column=1)

        def display_missions(self):
            self.mission_scroll.delete(1.0, tk.END)  # Limpar o widget de rolagem

        for i, mission in enumerate(self.missions):
            completed_text = "Completado" if mission.completed else "Não completado"
            mission_text = f"{mission.name} ({mission.difficulty}): {mission.points} pontos - {completed_text}\n"
            self.mission_scroll.insert(tk.END, mission_text)
            # Criar botão para marcar a missão como completada/não completada
            completion_button = tk.Button(self.mission_scroll, text="Completar/Descompletar",
                                      command=mission.toggle_completed)
            self.mission_scroll.window_create(tk.END, window=completion_button)
            self.mission_scroll.insert(tk.END, "\n")
# Exibir missões na lista de rótulos
        """for i, mission in enumerate(self.missions):
            # Criar rótulo para a missão
            label = tk.Label(self.mission_scroll, text=mission.name)
            label.grid(row=i, column=0)

            # Criar botão para marcar a missão como completada
            def toggle_completed():
                mission.toggle_completed()
                if mission.completed:
                    button.configure(text="Desmarcar")
                else:
                    button.configure(text="Marcar como completada")

            button = tk.Button(self.mission_scroll, text="Marcar como completada", command=toggle_completed)
            button.grid(row=i, column=1)"""
root = tk.Tk()
app = PersonProfile(root)
root.mainloop()