import tkinter as tk
from tkinter import messagebox
import csv
import random
from tkinter import simpledialog

class ChineseQuizApp:
    def __init__(self, root, level):
        self.root = root
        self.root.title("Chinese Quiz")
        self.root.geometry("400x450")

        self.load_data(level)
        self.shuffle_data()

        self.total_characters = len(self.data)
        self.current_index = 0
        self.current_character = tk.StringVar()

        self.progress_label = tk.Label(root, text="", font=("Arial", 12))
        self.progress_label.pack(pady=10)  # Espaciado adicional

        self.label = tk.Label(root, text="", font=("SimSun", 24), bg="#F0F0F0")
        self.label.pack(pady=20)

        self.show_character()

        self.button = tk.Button(root, text="Mostrar Significado", command=self.show_meaning, bg="#4CAF50", fg="white")
        self.button.pack(pady=10)

        self.next_button = tk.Button(root, text="Siguiente Caracter", command=self.next_character, bg="#008CBA", fg="white")
        self.next_button.pack(pady=10)

    def load_data(self, level):
        try:
            filename = f'hsk{level}.csv'
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                self.data = list(reader)
        except FileNotFoundError:
            tk.messagebox.showerror("Error", f"El archivo {filename} no se encuentra en el mismo directorio que el script.")
            self.root.destroy()

    def shuffle_data(self):
        random.shuffle(self.data)

    def show_character(self):
        char_info = self.data[self.current_index]
        character = char_info[0]
        self.current_character.set(character)
        self.label.config(text=f"Carácter: {self.current_character.get()}")
        self.update_progress_label()

    def show_meaning(self):
        char_info = self.data[self.current_index]
        meaning = char_info[2]
        pinyin = char_info[1]
        self.label.config(text=f"Carácter: {self.current_character.get()}\nSignificado: {meaning}\nPinyin: {pinyin}")

    def next_character(self):
        if self.current_index < self.total_characters - 1:
            self.current_index += 1
            self.label.config(text="")
            self.show_character()
        else:
            self.label.config(text="¡Fin del juego!")

    def update_progress_label(self):
        progress_text = f"{self.current_index + 1}/{self.total_characters}"
        self.progress_label.config(text=progress_text)

def choose_hsk_level():
    level = simpledialog.askinteger("HSK Level", "Elija el nivel de HSK (1-6):", minvalue=1, maxvalue=6)
    return level

if __name__ == "__main__":
    root = tk.Tk()
    level = choose_hsk_level()
    
    if level:
        app = ChineseQuizApp(root, level)
        root.mainloop()
    else:
        tk.messagebox.showinfo("Adiós", "Gracias por usar la aplicación. ¡Hasta luego!")
