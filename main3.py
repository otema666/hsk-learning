import tkinter as tk
from tkinter import messagebox
import csv
import random
from tkinter import simpledialog

class ChineseQuizApp:
    def __init__(self, root, level):
        self.root = root
        self.root.title("中文学习")
        self.root.geometry("400x450")

        self.load_data(level)
        self.shuffle_data()

        self.total_characters = len(self.data)
        self.current_index = 0
        self.current_character = tk.StringVar()

        self.progress_label = tk.Label(root, text="", font=("Arial", 12))
        self.progress_label.pack(pady=10)

        self.label = tk.Label(root, text="", font=("SimSun", 14), bg="#F0F0F0")
        self.label.pack(pady=20)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.check_answer_event)  # Bind the Enter key

        self.show_character()

        self.button = tk.Button(root, text="意思 (m)", command=self.show_meaning, bg="#4CAF50", fg="white")
        self.button.pack(pady=10)

        self.next_button = tk.Button(root, text="下一个 (n)", command=self.next_character, bg="#008CBA", fg="white")
        self.next_button.pack(pady=10)

        # Bind the keys to their respective functions
        self.root.bind('<n>', self.next_character_event)
        self.root.bind('<m>', self.show_meaning_event)

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
        self.label.config(text=self.current_character.get())
        self.entry.delete(0, tk.END)  # Clear entry field for the next character
        self.update_progress_label()

    def show_meaning(self):
        char_info = self.data[self.current_index]
        meaning = char_info[2]
        pinyin = char_info[1]
        self.label.config(text=f"{self.current_character.get()}\n{meaning}\n{pinyin}")
        #self.root.after(2000, self.next_character)

    def check_answer(self):
        user_input = self.entry.get().strip()  # Get the input and remove extra spaces
        if user_input == self.current_character.get():
            tk.messagebox.showinfo("对", "对！")
            self.next_character()
        else:
            tk.messagebox.showerror("错", f"错. El carácter era: {self.current_character.get()}")

    # Event wrapper for checking answer when Enter is pressed
    def check_answer_event(self, event=None):
        self.check_answer()

    # Event wrapper for keyboard shortcut to show meaning
    def show_meaning_event(self, event=None):
        self.show_meaning()

    def next_character(self):
        if self.current_index < self.total_characters - 1:
            self.current_index += 1
            self.label.config(text="")
            self.show_character()
        else:
            self.label.config(text="¡Fin del juego!")

    # Event wrapper for keyboard shortcut to show next character
    def next_character_event(self, event=None):
        self.next_character()

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
