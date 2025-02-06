from tkinter import Tk

class Game:
    def __init__(self):
        self.root = Tk()
        self.current_state = None

    def change_state(self, new_state):
        if self.current_state:
            self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()

    def run(self):
        from states.menuState import MenuState  
        self.change_state(MenuState(self))
        self.root.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()