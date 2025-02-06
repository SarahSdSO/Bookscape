import json
from tkinter import Label, Button, Radiobutton, IntVar, DISABLED, NORMAL
from gameState import GameState

class QuizState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.lives = 3
        self.correct = 0
        self.q_no = 0
        self.time_left = 60
        self.timer_running = False

        with open('data.json', encoding="utf-8") as f:
            data = json.load(f)

        self.questions = data['question']
        self.options = data['options']
        self.answers = data['answer']

        self.opt_selected = IntVar()

    def enter(self):
        self.game.root.title("Bookscape Quiz")
        self.game.root.geometry("800x450")

        # Limpa widgets anteriores, se houver
        self.exit()

        # Cria novos widgets
        self.title_label = Label(self.game.root, text="Bookscape Quiz", width=50, bg="green", fg="white", font=("ariel", 20, "bold"))
        self.title_label.place(x=0, y=2)
        self.widgets.append(self.title_label)

        self.question_label = Label(self.game.root, text="", width=60, font=("ariel", 16, "bold"), anchor="w")
        self.question_label.place(x=70, y=100)
        self.widgets.append(self.question_label)

        self.opts = self.create_radio_buttons()
        self.next_button = Button(self.game.root, text="Next", command=self.next_btn, width=10, bg="blue", fg="white", font=("ariel", 16, "bold"), state=DISABLED)
        self.next_button.place(x=350, y=380)
        self.widgets.append(self.next_button)

        self.quit_button = Button(self.game.root, text="Quit", command=self.game.root.destroy, width=5, bg="black", fg="white", font=("ariel", 16, "bold"))
        self.quit_button.place(x=700, y=50)
        self.widgets.append(self.quit_button)

        self.timer_label = Label(self.game.root, text=f"Tempo: {self.time_left}s", font=("ariel", 14, "bold"))
        self.timer_label.place(x=350, y=50)
        self.widgets.append(self.timer_label)

        self.lives_label = Label(self.game.root, text="❤️❤️❤️", font=("ariel", 16, "bold"), fg="red")
        self.lives_label.place(x=50, y=50)
        self.widgets.append(self.lives_label)

        self.display_question()
        self.start_timer()

    def create_radio_buttons(self):
        q_list = []
        y_pos = 150
        for i in range(4):
            radio_btn = Radiobutton(self.game.root, text="", variable=self.opt_selected, value=i+1, font=("ariel", 14), command=self.enable_next_button)
            radio_btn.place(x=100, y=y_pos)
            q_list.append(radio_btn)
            self.widgets.append(radio_btn)
            y_pos += 40
        return q_list

    def display_question(self):
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
            self.game.root.after(1000, self.countdown)
        else:
            self.timer_running = False
            self.lose_life()
            self.next_btn()

    def display_result(self):
        if self.lives > 0:
            from crosswordsState import CrosswordsState 
            self.game.change_state(CrosswordsState(self.game))
        else:
            from gameOverState import GameOverState 
            self.game.change_state(GameOverState(self.game))