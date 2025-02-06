from tkinter import Label, Button
from gameState import GameState

class MenuState(GameState):
    def enter(self):
        self.game.root.title("Bookscape Menu")
        self.game.root.geometry("800x450")

        self.title_label = Label(self.game.root, text="Bookscape", width=50, bg="green", fg="white", font=("ariel", 20, "bold"))
        self.title_label.place(x=0, y=2)
        self.widgets.append(self.title_label)

        self.start_button = Button(self.game.root, text="Start", command=self.start_game, width=10, bg="blue", fg="white", font=("ariel", 16, "bold"))
        self.start_button.place(x=350, y=200)
        self.widgets.append(self.start_button)

    def start_game(self):
        from states.storyState import StoryState 
        self.game.change_state(StoryState(self.game))
