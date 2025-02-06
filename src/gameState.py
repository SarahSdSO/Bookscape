class GameState:
    def __init__(self, game):
        self.game = game
        self.widgets = []

    def enter(self):
        pass

    def exit(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass