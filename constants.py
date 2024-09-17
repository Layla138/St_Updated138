import os

# Display
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Font
FONT_PATH = os.path.join("fonts", "Pixellari.ttf")

# Button properties
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_X = (WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = HEIGHT - 100

# Characters
CHARACTERS = ["Mike", "Will", "Max", "Lucas", "Eleven", "Dustin"]
CHARACTER_FOLDER = "character_images"

# Game states
TITLE_SCREEN = 0
CHARACTER_SELECT = 1
LOADING_SCREEN = 2
GAME_START = 3

# Game prompts and choices
PROMPT = "You find yourself in The UpsideDown. What do you do?"
CHOICES = ["Explore", "Wait", "Call for help"]
