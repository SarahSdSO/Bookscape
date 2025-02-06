from tkinter import Label, Button
from gameState import GameState

class StoryState(GameState):
    def enter(self):
        self.game.root.title("Bookscape Story")
        self.game.root.geometry("800x450")

        self.title_label = Label(self.game.root, text="Story", width=50, bg="green", fg="white", font=("ariel", 20, "bold"))
        self.title_label.place(x=0, y=2)
        self.widgets.append(self.title_label)

        self.next_button = Button(self.game.root, text="Next", command=self.next_state, width=10, bg="blue", fg="white", font=("ariel", 16, "bold"))
        self.next_button.place(x=350, y=200)
        self.widgets.append(self.next_button)

    def next_state(self):
        from states.quizState import QuizState
        self.game.change_state(QuizState(self.game))