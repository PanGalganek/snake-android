"""Pure-Python Snake rules; no graphics required."""
import random

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:
    def __init__(self, width=18, height=24, rng=None):
        if width < 4 or height < 4:
            raise ValueError("Board must be at least 4x4")
        self.width = width
        self.height = height
        self.rng = rng if rng is not None else random.Random()
        self.reset()

    def reset(self):
        x, y = self.width // 2, self.height // 2
        self.snake = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.score = 0
        self.game_over = False
        self.won = False
        self.food = self._make_food()

    def _make_food(self):
        occupied = set(self.snake)
        free = [(x, y) for x in range(self.width) for y in range(self.height)
                if (x, y) not in occupied]
        return self.rng.choice(free) if free else None

    def turn(self, direction):
        if self.game_over or direction not in (UP, DOWN, LEFT, RIGHT):
            return False
        if direction[0] == -self.direction[0] and direction[1] == -self.direction[1]:
            return False
        self.pending_direction = direction
        return True

    def step(self):
        if self.game_over:
            return
        self.direction = self.pending_direction
        hx, hy = self.snake[0]
        dx, dy = self.direction
        head = (hx + dx, hy + dy)
        if not (0 <= head[0] < self.width and 0 <= head[1] < self.height):
            self.game_over = True
            return
        eating = head == self.food
        occupied = self.snake if eating else self.snake[:-1]
        if head in occupied:
            self.game_over = True
            return
        self.snake.insert(0, head)
        if eating:
            self.score += 1
            self.food = self._make_food()
            if self.food is None:
                self.won = True
                self.game_over = True
        else:
            self.snake.pop()
