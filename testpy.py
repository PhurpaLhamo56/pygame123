import unittest
import pygame
from pygame.locals import *
import copy

# Import your game code here

class TestBubbleShooterGame(unittest.TestCase):

    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_bubble_collision(self):
        game = self.initialize_game()
        bubble1 = game.bubbleArray[0][0]
        bubble2 = Bubble(color=RED, row=1, column=0)
        game.bubbleArray[1][0] = bubble2

        game.launchBubble = True
        game.newBubble = Bubble(color=RED)
        game.newBubble.angle = 90

        # Simulate the game loop until the collision
        while game.launchBubble:
            game.runGame()

        # Check if the collision has occurred
        self.assertNotIn((1, 0), game.deleteList)
        self.assertIn((0, 0), game.deleteList)

    def test_score_increment(self):
        game = self.initialize_game()
        bubble1 = game.bubbleArray[0][0]
        bubble2 = Bubble(color=RED, row=1, column=0)
        game.bubbleArray[1][0] = bubble2

        game.launchBubble = True
        game.newBubble = Bubble(color=RED)
        game.newBubble.angle = 90

        # Simulate the game loop until the collision
        while game.launchBubble:
            game.runGame()

        # Check if the score increments correctly
        self.assertEqual(game.score.total, 10)

    def test_game_win(self):
        game = initialize_game()
        game.bubbleArray = make_win_board()
        game.launchBubble = True
        game.newBubble = Bubble(color=RED)
        game.newBubble.angle = 90

        # Simulate the game loop until the game ends
        while game.launchBubble:
            game.runGame()

        # Check if the game correctly recognizes the win condition
        self.assertEqual(game.winorlose, 'win')

    def test_game_lose(self):
        game = self.initialize_game()
        game.bubbleArray = make_lose_board()
        game.launchBubble = True
        game.newBubble = Bubble(color=RED)
        game.newBubble.angle = 90

        # Simulate the game loop until the game ends
        while game.launchBubble:
            game.runGame()

        # Check if the game correctly recognizes the lose condition
        self.assertEqual(game.winorlose, 'lose')

    def test_arrow_rotation(self):
        game = self.initialize_game()
        arrow = game.arrow
        initial_angle = arrow.angle

        game.direction = LEFT
        game.arrow.update_direction()
        self.assertEqual(arrow.angle, initial_angle + 2)

        game.direction = RIGHT
        game.arrow.update_direction()
        self.assertEqual(arrow.angle, initial_angle)

    def test_music_change(self):
        game = initialize_game()
        initial_track = game.track

        # Simulate the game loop until the music changes
        while game.launchBubble:
            game.runGame()

        # Check if the game correctly changes the background music
        self.assertNotEqual(game.track, initial_track)

    def test_restart_game(self):
        game = self.initialize_game()
        game.bubbleArray = make_lose_board()
        game.launchBubble = True
        game.newBubble = Bubble(color=RED)
        game.newBubble.angle = 90

        # Simulate the game loop until the game ends
        while game.launchBubble:
            game.runGame()

        initial_score = copy.deepcopy(game.score)
        initial_track = game.track

        game.endScreen()

        # Check if the game state is reset correctly after restarting
        self.assertEqual(game.score.total, 0)
        self.assertNotEqual(game.track, initial_track)
        self.assertNotEqual(game.score, initial_score)

    def initialize_game(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        game = BubbleShooterGame()
        game.FPSCLOCK = pygame.time.Clock()
        game.DISPLAYSURF, game.DISPLAYRECT = makeDisplay()
        return game

    

if __name__ == '__main__':
    unittest.main()