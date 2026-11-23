"""Touch-friendly Android Snake built with Kivy."""
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from snake_logic import SnakeGame, UP, DOWN, LEFT, RIGHT


class Board(Widget):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self._touch_start = None
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *_args):
        self.canvas.clear()
        cell = min(self.width / self.game.width, self.height / self.game.height)
        if cell <= 0:
            return
        board_w = cell * self.game.width
        board_h = cell * self.game.height
        x0 = self.x + (self.width - board_w) / 2
        y0 = self.y + (self.height - board_h) / 2
        with self.canvas:
            Color(0.07, 0.11, 0.14, 1)
            RoundedRectangle(pos=(x0, y0), size=(board_w, board_h), radius=[dp(10)])
            for x, y in self.game.snake:
                if (x, y) == self.game.snake[0]:
                    Color(0.48, 0.97, 0.52, 1)
                else:
                    Color(0.20, 0.75, 0.36, 1)
                Rectangle(pos=(x0 + x * cell + 1, y0 + y * cell + 1),
                          size=(max(1, cell - 2), max(1, cell - 2)))
            if self.game.food is not None:
                Color(1, 0.31, 0.31, 1)
                fx, fy = self.game.food
                RoundedRectangle(pos=(x0 + fx * cell + 2, y0 + fy * cell + 2),
                                 size=(max(1, cell - 4), max(1, cell - 4)),
                                 radius=[max(1, cell / 2)])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._touch_start = touch.pos
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._touch_start is not None:
            sx, sy = self._touch_start
            self._touch_start = None
            dx, dy = touch.x - sx, touch.y - sy
            if max(abs(dx), abs(dy)) >= dp(20):
                if abs(dx) > abs(dy):
                    self.game.turn(RIGHT if dx > 0 else LEFT)
                else:
                    self.game.turn(UP if dy > 0 else DOWN)
            return True
        return super().on_touch_up(touch)


class SnakeApp(App):
    def build(self):
        self.title = "Snake"
        Window.clearcolor = (0.04, 0.07, 0.09, 1)
        self.game = SnakeGame()
        self.paused = False
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(8))
        self.status = Label(text="Punkty: 0", size_hint_y=None, height=dp(48),
                            font_size="22sp", bold=True)
        root.add_widget(self.status)
        self.board = Board(self.game)
        root.add_widget(self.board)
        controls = GridLayout(cols=3, rows=2, size_hint_y=None,
                              height=dp(118), spacing=dp(6))
        controls.add_widget(Label())
        controls.add_widget(self.direction_button("GÓRA", UP))
        controls.add_widget(Label())
        controls.add_widget(self.direction_button("LEWO", LEFT))
        controls.add_widget(self.direction_button("DÓŁ", DOWN))
        controls.add_widget(self.direction_button("PRAWO", RIGHT))
        root.add_widget(controls)
        bottom = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.pause_btn = Button(text="Pauza", font_size="18sp")
        self.pause_btn.bind(on_release=self.toggle_pause)
        restart_btn = Button(text="Nowa gra", font_size="18sp")
        restart_btn.bind(on_release=self.restart)
        bottom.add_widget(self.pause_btn)
        bottom.add_widget(restart_btn)
        root.add_widget(bottom)
        self.event = Clock.schedule_interval(self.tick, 0.15)
        return root

    def direction_button(self, label, direction):
        button = Button(text=label, font_size="17sp")
        button.bind(on_release=lambda _btn: self.game.turn(direction))
        return button

    def tick(self, _dt):
        if not self.paused and not self.game.game_over:
            self.game.step()
            self.refresh()

    def refresh(self):
        if self.game.won:
            self.status.text = f"WYGRANA! Punkty: {self.game.score}"
        elif self.game.game_over:
            self.status.text = f"KONIEC GRY! Punkty: {self.game.score}"
        elif self.paused:
            self.status.text = f"PAUZA | Punkty: {self.game.score}"
        else:
            self.status.text = f"Punkty: {self.game.score}"
        self.board.draw()

    def toggle_pause(self, _btn):
        if not self.game.game_over:
            self.paused = not self.paused
            self.pause_btn.text = "Wznów" if self.paused else "Pauza"
            self.refresh()

    def restart(self, _btn):
        self.game.reset()
        self.paused = False
        self.pause_btn.text = "Pauza"
        self.refresh()

    def on_stop(self):
        self.event.cancel()


if __name__ == "__main__":
    SnakeApp().run()
