import pygame
import sys
import os
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stranger Things Adventure")

# Load the wallpaper image
wallpaper = pygame.image.load("location/wallpaper.png")
wallpaper = pygame.transform.scale(wallpaper, (WIDTH - 40, HEIGHT - 160))

# Load the gloomy forest image
gloomy_forest = pygame.image.load(os.path.join("location", "gloomy_forest_four.png"))
gloomy_forest = pygame.transform.scale(gloomy_forest, (WIDTH - 40, HEIGHT - 160))  # Adjust for border and extended bottom

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Font setup
font_path = os.path.join("fonts", "Pixellari.ttf")
title_font = pygame.font.Font(font_path, 36)
button_font = pygame.font.Font(font_path, 24)

# Button properties
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_X = (WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = HEIGHT - 100

# Character selection
characters = ["Mike", "Will", "Max", "Lucas", "Eleven", "Dustin"]
character_images = {}
selected_character = None

# Load character images
character_folder = "character_images"
for character in characters:
    img_path = os.path.join(character_folder, f"{character}.png")
    if os.path.exists(img_path):
        img = pygame.image.load(img_path)
        character_images[character] = pygame.transform.scale(img, (100, 100))
    else:
        print(f"Warning: Image for {character} not found.")

# Game states
TITLE_SCREEN = 0
CHARACTER_SELECT = 1
LOADING_SCREEN = 2
GAME_START = 3
game_state = TITLE_SCREEN

# Loading bar variables
loading_progress = 0
loading_speed = 0.5  # Adjust this to change loading speed

# Blinking effect variables
blink_timer = 0
blink_interval = 250  # milliseconds
show_border = True

# Fade in variables
fade_alpha = 0
FADE_SPEED = 5

# Player variables
player_image = None
player_rect = None

def draw_title_screen():
    screen.blit(wallpaper, (20, 20))
    title_text = "Welcome to the"
    subtitle_text = "Stranger Things adventure game!"
    title_surface = title_font.render(title_text, True, WHITE)
    subtitle_surface = title_font.render(subtitle_text, True, WHITE)
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT - 200)))
    screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT - 160)))
    pygame.draw.rect(screen, RED, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    play_text = button_font.render("PLAY", True, WHITE)
    screen.blit(play_text, play_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))

def draw_character_select():
    global blink_timer, show_border
    screen.blit(wallpaper, (20, 20))
    
    # Move "Select Your Character" text back to the top
    title_text = "Select Your Character"
    title_surface = title_font.render(title_text, True, WHITE)
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 50)))
    
    for i, character in enumerate(characters):
        x = 150 + (i % 3) * 200
        y = 150 + (i // 3) * 150
        if character in character_images:
            screen.blit(character_images[character], (x, y))
        name_text = button_font.render(character, True, WHITE)
        screen.blit(name_text, name_text.get_rect(center=(x + 50, y + 120)))
        
        if character == selected_character and show_border:
            pygame.draw.rect(screen, RED, (x-5, y-5, 110, 110), 3)  # Blinking highlight for selected character
    
    if selected_character:
        pygame.draw.rect(screen, RED, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        start_text = button_font.render("Start Game", True, WHITE)
        screen.blit(start_text, start_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))
    
    current_time = pygame.time.get_ticks()
    if current_time - blink_timer > blink_interval:
        blink_timer = current_time
        show_border = not show_border

def draw_loading_screen():
    global loading_progress, fade_alpha
    screen.fill(BLACK)  # Fill the screen with black for the border
    screen.blit(wallpaper, (20, 20))
    
    # Draw "Game loading..." text
    loading_text = title_font.render("Game loading...", True, WHITE)
    screen.blit(loading_text, loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    
    # Draw loading bar
    bar_width = 400
    bar_height = 40
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2 + 50
    
    # Draw empty bar
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    # Draw filled portion of bar
    fill_width = int(bar_width * loading_progress)
    pygame.draw.rect(screen, RED, (bar_x, bar_y, fill_width, bar_height))
    
    # Update loading progress
    if loading_progress < 1:
        loading_progress += loading_speed * 0.01
    else:
        # Start fading in the gloomy forest image
        fade_surface = pygame.Surface((WIDTH - 40, HEIGHT - 160))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(255 - fade_alpha)
        screen.blit(gloomy_forest, (20, 20))
        screen.blit(fade_surface, (20, 20))
        
        fade_alpha += FADE_SPEED
        if fade_alpha >= 255:
            return True  # Loading complete
    
    return False

def start_game():
    global player_image, player_rect, selected_character
    # Load player image
    player_image = pygame.image.load(os.path.join("character_images", f"{selected_character}.png"))
    player_image = pygame.transform.scale(player_image, (150, 150))  # Increased size to 150x150
    player_rect = player_image.get_rect()
    # Position the character at the bottom center, on the black border
    player_rect.midbottom = (WIDTH // 2, HEIGHT - 5)  # 5 pixels from the bottom

def draw_game():
    screen.fill(BLACK)
    screen.blit(gloomy_forest, (20, 20))
    if player_image and player_rect:
        screen.blit(player_image, player_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == TITLE_SCREEN:
                if BUTTON_X <= mouse_pos[0] <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_pos[1] <= BUTTON_Y + BUTTON_HEIGHT:
                    game_state = CHARACTER_SELECT
            elif game_state == CHARACTER_SELECT:
                for i, character in enumerate(characters):
                    x = 150 + (i % 3) * 200
                    y = 150 + (i // 3) * 150
                    if x <= mouse_pos[0] <= x + 100 and y <= mouse_pos[1] <= y + 100:
                        selected_character = character
                        print(f"Selected character: {character}")
                        blink_timer = pygame.time.get_ticks()
                
                if selected_character and BUTTON_X <= mouse_pos[0] <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_pos[1] <= BUTTON_Y + BUTTON_HEIGHT:
                    game_state = LOADING_SCREEN
                    loading_progress = 0  # Reset loading progress

    screen.fill(BLACK)  # Fill the screen with black for the border
    
    if game_state == TITLE_SCREEN:
        draw_title_screen()
    elif game_state == CHARACTER_SELECT:
        draw_character_select()
    elif game_state == LOADING_SCREEN:
        if draw_loading_screen():
            game_state = GAME_START
            start_game()
    elif game_state == GAME_START:
        draw_game()

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limit frame rate to 60 FPS

# Quit the game
pygame.quit()
sys.exit()
