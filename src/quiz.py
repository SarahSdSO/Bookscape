from tkinter import *
from tkinter import messagebox as mb
import json
import time

class Quiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookscape Quiz")
        self.root.geometry("800x450")

        # Carregar perguntas do arquivo JSON
        with open('data.json') as f:
            data = json.load(f)

        self.questions = data['question']
        self.options = data['options']
        self.answers = data['answer']
        self.q_no = 0
        self.correct = 0
        self.lives = 3
        self.time_left = 60
        self.timer_running = False

        self.opt_selected = IntVar()
        self.create_widgets()
        self.display_question()
        self.update_lives()
        self.start_timer()

    def create_widgets(self):
        self.title_label = Label(self.root, text="Bookscape Quiz", width=50, bg="green", fg="white", font=("ariel", 20, "bold"))
        self.title_label.place(x=0, y=2)

        self.question_label = Label(self.root, text="", width=60, font=("ariel", 16, "bold"), anchor="w")
        self.question_label.place(x=70, y=100)

        self.opts = self.create_radio_buttons()
        self.next_button = Button(self.root, text="Next", command=self.next_btn, width=10, bg="blue", fg="white", font=("ariel", 16, "bold"), state=DISABLED)
        self.next_button.place(x=350, y=380)

        self.quit_button = Button(self.root, text="Quit", command=self.root.destroy, width=5, bg="black", fg="white", font=("ariel", 16, "bold"))
        self.quit_button.place(x=700, y=50)

        self.timer_label = Label(self.root, text=f"Tempo: {self.time_left}s", font=("ariel", 14, "bold"))
        self.timer_label.place(x=350, y=50)

        self.lives_label = Label(self.root, text="❤️❤️❤️", font=("ariel", 16, "bold"), fg="red")
        self.lives_label.place(x=50, y=50)

    def create_radio_buttons(self):
        q_list = []
        y_pos = 150
        for i in range(4):
            radio_btn = Radiobutton(self.root, text="", variable=self.opt_selected, value=i+1, font=("ariel", 14), command=self.enable_next_button)
            radio_btn.place(x=100, y=y_pos)
            q_list.append(radio_btn)
            y_pos += 40
        return q_list

    def display_question(self):
        """Exibe a pergunta atual e suas opções."""
        self.question_label.config(text=self.questions[self.q_no])
        self.opt_selected.set(0)
        for i, option in enumerate(self.options[self.q_no]):
            self.opts[i].config(text=option)
        self.next_button.config(state=DISABLED)
        self.time_left = 60
        self.start_timer()

    def enable_next_button(self):
        self.next_button.config(state=NORMAL)

    def check_answer(self):
        return self.opt_selected.get() == self.answers[self.q_no]

    def next_btn(self):
        if self.check_answer():
            self.correct += 1
        else:
            self.lose_life()

        self.q_no += 1
        if self.q_no == len(self.questions) or self.lives == 0:
            self.display_result()
        else:
            self.display_question()

    def lose_life(self):
        self.lives -= 1
        self.update_lives()
        if self.lives == 0:
            self.display_result()

    def update_lives(self):
        self.lives_label.config(text="❤️" * self.lives + "♡" * (3 - self.lives))

    def start_timer(self):
        if self.timer_running:
            return
        self.timer_running = True
        self.countdown()

    def countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Tempo: {self.time_left}s")
            self.root.after(1000, self.countdown)
        else:
            self.timer_running = False
            self.lose_life()
            self.next_btn()

    def display_result(self):
        score = int(self.correct / len(self.questions) * 100)
        mb.showinfo("Resultado", f"Score: {score}%\nCorretas: {self.correct}\nErradas: {len(self.questions) - self.correct}")
        self.root.destroy()

# Criar janela principal
root = Tk()
quiz = Quiz(root)
root.mainloop()