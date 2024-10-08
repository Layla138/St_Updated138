import pygame
import sys
import os
import time

# Global variables
global location_text_alpha, location_text_timer, LOCATION_TEXT_DURATION, location_text_shown, character_alpha
global prompt_alpha, choices_alpha, prompt_hidden  # Add prompt_hidden to the global variables

# Initialize global variables
location_text_alpha = 255
location_text_timer = 0
LOCATION_TEXT_DURATION = 3000  # Duration in milliseconds (3 seconds)
location_text_shown = False
character_alpha = 0  # Start fully transparent
prompt_alpha = 0
choices_alpha = 0
prompt_hidden = False  # Initialize prompt_hidden to False

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stranger Things Adventure")

# Load assets
def load_assets():
    assets = {}
    # Load the wallpaper
    assets['wallpaper'] = pygame.image.load(os.path.join("location", "wallpaper.png"))
    assets['wallpaper'] = pygame.transform.scale(assets['wallpaper'], (WIDTH - 40, HEIGHT - 160))
    assets['gloomy_forest'] = pygame.image.load(os.path.join("location", "gloomy_forest_four.png"))
    assets['gloomy_forest'] = pygame.transform.scale(assets['gloomy_forest'], (WIDTH - 40, HEIGHT - 160))
    assets['outside_hawkins_lab'] = pygame.image.load('location/outside_hawkins_lab.png').convert()
    assets['gloomy_forest_three'] = pygame.image.load(os.path.join("location", "gloomy_forest_three.png"))
    assets['gloomy_forest_three'] = pygame.transform.scale(assets['gloomy_forest_three'], (WIDTH - 40, HEIGHT - 160))
    
    # Load character images
    assets['characters'] = {}
    character_folder = "character_images"
    for character in ["Mike", "Will", "Max", "Lucas", "Eleven", "Dustin"]:
        img_path = os.path.join(character_folder, f"{character}.png")
        if os.path.exists(img_path):
            img = pygame.image.load(img_path)
            assets['characters'][character] = pygame.transform.scale(img, (100, 100))
    
    # Load fonts
    font_path = os.path.join("fonts", "Pixellari.ttf")
    assets['title_font'] = pygame.font.Font(font_path, 36)
    assets['button_font'] = pygame.font.Font(font_path, 24)
    
    return assets

assets = load_assets()

# Game states
TITLE_SCREEN = 0
CHARACTER_SELECT = 1
LOADING_SCREEN = 2
GAME_START = 3

# Game variables
game_state = TITLE_SCREEN
selected_character = None

# Blinking effect variables
blink_timer = 0
blink_interval = 250  # milliseconds
show_border = True

# Loading progress variables
loading_progress = 0
loading_speed = 0.5  # Adjust this to change loading speed
fade_alpha = 0
FADE_SPEED = 5

# Draw functions
def draw_title_screen(screen, assets):
    screen.blit(assets['wallpaper'], (20, 20))
    title_text = "Welcome to the"
    subtitle_text = "Stranger Things adventure game!"
    title_surface = assets['title_font'].render(title_text, True, (255, 255, 255))
    subtitle_surface = assets['title_font'].render(subtitle_text, True, (255, 255, 255))
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT - 200)))
    screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT - 160)))
    
    # Draw play button
    button_width, button_height = 200, 50
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - 100
    pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
    play_text = assets['button_font'].render("PLAY", True, (255, 255, 255))
    screen.blit(play_text, play_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2)))

    return button_x, button_y, button_width, button_height  # Return button dimensions for click detection

def draw_character_select(screen, assets, selected_character):
    global blink_timer, show_border
    screen.blit(assets['wallpaper'], (20, 20))
    title_text = "Select Your Character"
    title_surface = assets['title_font'].render(title_text, True, (255, 255, 255))
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 50)))
    
    current_time = pygame.time.get_ticks()
    if current_time - blink_timer > blink_interval:
        blink_timer = current_time
        show_border = not show_border
    
    for i, character in enumerate(assets['characters']):
        x = 150 + (i % 3) * 200
        y = 150 + (i // 3) * 150
        screen.blit(assets['characters'][character], (x, y))
        name_text = assets['button_font'].render(character, True, (255, 255, 255))
        screen.blit(name_text, name_text.get_rect(center=(x + 50, y + 120)))
        
        if character == selected_character and show_border:
            pygame.draw.rect(screen, (255, 0, 0), (x-5, y-5, 110, 110), 3)
    
    # Draw start game button if character is selected
    if selected_character:
        button_width, button_height = 200, 50
        button_x = (WIDTH - button_width) // 2
        button_y = HEIGHT - 100
        pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
        start_text = assets['button_font'].render("Start Game", True, (255, 255, 255))
        screen.blit(start_text, start_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2)))
        return button_x, button_y, button_width, button_height
    return None

def draw_loading_screen(screen, assets):
    global loading_progress, fade_alpha
    screen.fill((0, 0, 0))  # Fill the screen with black for the border
    screen.blit(assets['wallpaper'], (20, 20))
    
    if loading_progress < 1:
        # Draw "Loading..." text
        loading_text = assets['title_font'].render("Loading...", True, (255, 255, 255))
        screen.blit(loading_text, loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
        
        # Draw loading bar
        bar_width = 400
        bar_height = 40
        bar_x = (WIDTH - bar_width) // 2
        bar_y = HEIGHT // 2 + 50
        
        # Draw empty bar
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Draw filled portion of bar
        fill_width = int(bar_width * loading_progress)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, fill_width, bar_height))
        
        # Draw message in the black border area with larger font
        font_path = os.path.join("fonts", "Pixellari.ttf")
        message_font = pygame.font.Font(font_path, 32)
        message_text = message_font.render("Be prepared for an amazing adventure!", True, (255, 255, 255))
        screen.blit(message_text, message_text.get_rect(center=(WIDTH // 2, HEIGHT - 60)))
        
        # Update loading progress
        loading_progress += loading_speed * 0.01
    else:
        # Start fading out the loading screen and fading in the gloomy forest image
        screen.blit(assets['gloomy_forest'], (20, 20))
        
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(255 - fade_alpha)
        screen.blit(fade_surface, (0, 0))
        
        fade_alpha += FADE_SPEED
        if fade_alpha >= 255:
            return True  # Loading complete
    
    return False

def draw_game(screen, assets, selected_character, current_scenario):
    global location_text_alpha, location_text_timer, location_text_shown, character_alpha

    # Change background based on the current scenario
    if current_scenario == "EXPLORE":  # Update this condition
        screen.blit(assets['gloomy_forest_three'], (20, 20))  # Use gloomy_forest_three for the background
    elif current_scenario == "SHOUT_FOR_HELP":
        screen.blit(assets['gloomy_forest'], (20, 20))  # Use gloomy_forest for the background
    else:
        screen.blit(assets['gloomy_forest'], (20, 20))  # Keep the same background for other scenarios

    # Only draw location text if the current scenario is not "SHOUT_FOR_HELP"
    if current_scenario != "SHOUT_FOR_HELP":
        font = assets['title_font']
        text_surface = font.render("LOCATION: THE UPSIDE DOWN", True, (255, 255, 255))
        text_surface.set_alpha(location_text_alpha)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 500))
        screen.blit(text_surface, text_rect)

    # The rest of the function remains exactly the same as before
    if selected_character and selected_character in assets['characters']:
        character_image = assets['characters'][selected_character]
        character_image = pygame.transform.scale(character_image, (150, 150))
        character_rect = character_image.get_rect()
        character_rect.midbottom = (WIDTH // 2, HEIGHT - 140)
        
        character_image_alpha = character_image.copy()
        character_image_alpha.set_alpha(character_alpha)
        screen.blit(character_image_alpha, character_rect)
        
        if character_alpha < 255:
            character_alpha = min(255, character_alpha + 5)

    # Draw and fade the location text
    font = assets['title_font']
    text_surface = font.render("LOCATION: THE UPSIDE DOWN", True, (255, 255, 255))
    text_surface.set_alpha(location_text_alpha)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 500))
    screen.blit(text_surface, text_rect)

    current_time = pygame.time.get_ticks()
    if current_time - location_text_timer > LOCATION_TEXT_DURATION:
        location_text_alpha = max(0, location_text_alpha - 5)  # Fade out

    # Only draw prompt and choices if location text has faded out and current scenario is not "EXPLORE"
    if location_text_alpha == 0 and current_scenario != "EXPLORE":
        prompt_font = assets['button_font']
        prompt_text = "You Find Yourself In The Upside Down. What do you do?"
        prompt_surface = prompt_font.render(prompt_text, True, (255, 255, 255))
        prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(prompt_surface, prompt_rect)

        choices = [
            "Explore",
            "Sneak into Vecna's Lair",
            "Shout for help",
            "Find The Hawkins Lab"
        ]
        
        # Left choices
        screen.blit(prompt_font.render(choices[0], True, (255, 255, 255)), (50, HEIGHT - 60))
        screen.blit(prompt_font.render(choices[1], True, (255, 255, 255)), (50, HEIGHT - 30))
        
        # Right choices
        right_choice_x = WIDTH - 50 - prompt_font.size(choices[2])[0]  # Align right
        screen.blit(prompt_font.render(choices[2], True, (255, 255, 255)), (right_choice_x, HEIGHT - 60))
        right_choice_x = WIDTH - 50 - prompt_font.size(choices[3])[0]  # Align right
        screen.blit(prompt_font.render(choices[3], True, (255, 255, 255)), (right_choice_x, HEIGHT - 30))

    # Mark the text as shown once it has completely faded out
    if location_text_alpha == 0:
        location_text_shown = True

# Main game loop
current_scenario = "MAIN"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == TITLE_SCREEN:
                button_x, button_y, button_width, button_height = draw_title_screen(screen, assets)
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                    game_state = CHARACTER_SELECT
            elif game_state == CHARACTER_SELECT:
                for i, character in enumerate(assets['characters']):
                    x = 150 + (i % 3) * 200
                    y = 150 + (i // 3) * 150
                    if x <= mouse_pos[0] <= x + 100 and y <= mouse_pos[1] <= y + 100:
                        selected_character = character
                        blink_timer = pygame.time.get_ticks()  # Reset blink timer when character is selected
                
                if selected_character:
                    button_info = draw_character_select(screen, assets, selected_character)
                    if button_info:
                        button_x, button_y, button_width, button_height = button_info
                        if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                            game_state = LOADING_SCREEN
                            loading_progress = 0  # Reset loading progress
                            fade_alpha = 0  # Reset fade alpha
            elif game_state == GAME_START:
                if HEIGHT - 60 <= mouse_pos[1] <= HEIGHT:
                    if WIDTH - 200 <= mouse_pos[0] <= WIDTH:
                        current_scenario = "SHOUT_FOR_HELP"  # Set the scenario to SHOUT_FOR_HELP
                        location_text_alpha = 0  # Set alpha to 0 to hide the location text
                        location_text_timer = pygame.time.get_ticks()
                        location_text_shown = False
                    elif mouse_pos[0] <= 200:  # Check if "Explore" is clicked
                        current_scenario = "EXPLORE"  # Set the scenario to EXPLORE
                        location_text_alpha = 0  # Set alpha to 0 to hide the location text
                        location_text_timer = pygame.time.get_ticks()
                        location_text_shown = False
                        # No need to set any additional flags; just skip drawing the prompt and choices

    if game_state == TITLE_SCREEN:
        draw_title_screen(screen, assets)
    elif game_state == CHARACTER_SELECT:
        draw_character_select(screen, assets, selected_character)
    elif game_state == LOADING_SCREEN:
        if draw_loading_screen(screen, assets):
            game_state = GAME_START
            location_text_timer = pygame.time.get_ticks()  # Reset the timer when entering game state
            location_text_alpha = 255  # Reset the alpha value
            location_text_shown = False  # Reset the shown flag
            character_alpha = 0  # Start with a fully transparent character
    elif game_state == GAME_START:
        draw_game(screen, assets, selected_character, current_scenario)

        # Only draw prompt and choices if the current scenario is not "EXPLORE"
        if current_scenario != "EXPLORE":
            prompt_font = assets['button_font']
            prompt_text = "You Find Yourself In The Upside Down. What do you do?"
            prompt_surface = prompt_font.render(prompt_text, True, (255, 255, 255))
            prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            screen.blit(prompt_surface, prompt_rect)

            choices = [
                "Explore",
                "Sneak into Vecna's Lair",
                "Shout for help",
                "Find The Hawkins Lab"
            ]
            
            # Left choices
            screen.blit(prompt_font.render(choices[0], True, (255, 255, 255)), (50, HEIGHT - 60))
            screen.blit(prompt_font.render(choices[1], True, (255, 255, 255)), (50, HEIGHT - 30))
            
            # Right choices
            right_choice_x = WIDTH - 50 - prompt_font.size(choices[2])[0]  # Align right
            screen.blit(prompt_font.render(choices[2], True, (255, 255, 255)), (right_choice_x, HEIGHT - 60))
            right_choice_x = WIDTH - 50 - prompt_font.size(choices[3])[0]  # Align right
            screen.blit(prompt_font.render(choices[3], True, (255, 255, 255)), (right_choice_x, HEIGHT - 30))

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limit frame rate to 60 FPS

# Quit the game
pygame.quit()
sys.exit()