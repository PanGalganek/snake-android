import random
import unittest
from snake_logic import SnakeGame, UP, DOWN, LEFT, RIGHT

class SnakeTests(unittest.TestCase):
    def setUp(self):
        self.g = SnakeGame(8, 8, random.Random(1))

    def test_start(self):
        self.assertEqual(len(self.g.snake), 3)
        self.assertNotIn(self.g.food, self.g.snake)

    def test_move(self):
        x,y = self.g.snake[0]
        self.g.food = (0,0)
        self.g.step()
        self.assertEqual(self.g.snake[0], (x+1,y))
        self.assertEqual(len(self.g.snake), 3)

    def test_reverse_disallowed(self):
        self.assertFalse(self.g.turn(LEFT))
        self.assertEqual(self.g.direction, RIGHT)

    def test_two_turn_reverse_disallowed(self):
        self.assertTrue(self.g.turn(UP))
        self.assertFalse(self.g.turn(LEFT))
        self.g.step()
        self.assertEqual(self.g.direction, UP)

    def test_eat_growth(self):
        x,y = self.g.snake[0]
        self.g.food = (x+1,y)
        self.g.step()
        self.assertEqual(self.g.score, 1)
        self.assertEqual(len(self.g.snake), 4)
        self.assertNotIn(self.g.food, self.g.snake)

    def test_wall_collision(self):
        self.g.snake = [(7,4),(6,4),(5,4)]
        self.g.step()
        self.assertTrue(self.g.game_over)

    def test_body_collision(self):
        self.g.snake = [(3,3),(3,4),(4,4),(4,3),(4,2),(3,2)]
        self.g.direction = UP
        self.g.pending_direction = RIGHT
        self.g.step()
        self.assertTrue(self.g.game_over)

    def test_tail_square_permitted(self):
        self.g.snake = [(3,3),(3,4),(4,4),(4,3)]
        self.g.direction = DOWN
        self.g.pending_direction = RIGHT
        self.g.food = (0,0)
        self.g.step()
        self.assertFalse(self.g.game_over)
        self.assertEqual(self.g.snake[0], (4,3))

    def test_restart(self):
        self.g.game_over = True
        self.g.score = 5
        self.g.reset()
        self.assertFalse(self.g.game_over)
        self.assertEqual(self.g.score, 0)

    def test_board_full_win(self):
        g = SnakeGame(4,4,random.Random(1))
        g.snake = [(1,1)] + [(x,y) for x in range(4) for y in range(4) if (x,y) not in ((1,1),(2,1))]
        g.direction = RIGHT
        g.pending_direction = RIGHT
        g.food = (2,1)
        g.step()
        self.assertTrue(g.won)
        self.assertTrue(g.game_over)
        self.assertIsNone(g.food)

if __name__ == '__main__':
    unittest.main()
