from tkinter import Label, Button
from gameState import GameState

class GameOverState(GameState):
    def enter(self):
        self.game.root.title("Game Over")
        self.game.root.geometry("800x450")

        self.title_label = Label(self.game.root, text="Game Over", width=50, bg="red", fg="white", font=("ariel", 20, "bold"))
        self.title_label.place(x=0, y=2)
        self.widgets.append(self.title_label)

        self.restart_button = Button(self.game.root, text="Restart", command=self.restart_game, width=10, bg="blue", fg="white", font=("ariel", 16, "bold"))
        self.restart_button.place(x=350, y=200)
        self.widgets.append(self.restart_button)

    def restart_game(self):
        from states.menuState import MenuState
        self.game.change_state(MenuState(self.game))