import pygame
import sys
import os
import time
import random

# Global variables
global location_text_alpha, location_text_timer, LOCATION_TEXT_DURATION, location_text_shown, character_alpha
global prompt_alpha, choices_alpha, prompt_hidden, explore_fade_alpha, explore_fade_in_alpha
global vecna_fade_alpha, vecna_fade_in_alpha
global can_click
global hawkins_fade_alpha, hawkins_fade_in_alpha
global shout_fade_alpha, shout_text_visible
global explore_character
global explore_prompt_alpha, explore_choices_alpha
global run_fade_alpha, run_text_visible
global run_clicked, fight_sequence_startedY
global lightning_flash, lightning_timer, attack_animation_frameYY
global character_attack_pos, demogorgon_hit_pos
global fight_fade_alpha, fight_fade_complete
global player_pos, demogorgon_pos
global fight_fade_in_alpha
global countdown_timer, countdown_started, chase_started
global last_countdown_update
global fireballs
global last_fireball_time

# Initialize global variables
location_text_alpha = 255
location_text_timer = 0
LOCATION_TEXT_DURATION = 3000  # Duration in milliseconds (3 seconds)
location_text_shown = False
character_alpha = 0  # Start fully transparent
prompt_alpha = 0
choices_alpha = 0
prompt_hidden = False  # Initialize prompt_hidden to False
explore_fade_alpha = 0
explore_fade_in_alpha = 0  # New variable for fade-in effect
vecna_fade_alpha = 0
vecna_fade_in_alpha = 0
can_click = True  # This will control when clicks are allowed
hawkins_fade_alpha = 0
hawkins_fade_in_alpha = 0
shout_fade_alpha = 0
shout_text_visible = False  # Flag to control when to show text
explore_character = None
explore_prompt_alpha = 0
explore_choices_alpha = 0
run_clicked = False
run_fade_alpha = 0
run_text_visible = False
lightning_flash = False
lightning_timer = 0
attack_animation_frame = 0
character_attack_pos = 0
demogorgon_hit_pos = 0
fight_sequence_started = False  # Add this with the other initializations
fight_fade_alpha = 0
fight_fade_complete = False
fight_fade_in_alpha = 0
countdown_timer = 5  # Start at 5 seconds
countdown_started = False
chase_started = False
last_countdown_update = 0
fireballs = []  # List to store active fireballs
last_fireball_time = 0  # Cooldown timer for shooting
FIREBALL_COOLDOWN = 500  # Milliseconds between shots
FIREBALL_SPEED = 7  # Speed of fireballs

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stranger Things Adventure")

# Initialize positions
player_pos = [WIDTH - 130 - 100, HEIGHT - 130 - 200]  # Starting position for player
demogorgon_pos = [50, HEIGHT - 330]  # Move further left

# Load assets
def load_assets():
    assets = {}
    # Load the wallpaper
    assets['wallpaper'] = pygame.image.load(os.path.join("location", "wallpaper.png"))
    assets['wallpaper'] = pygame.transform.scale(assets['wallpaper'], (WIDTH - 40, HEIGHT - 160))
    assets['gloomy_forest'] = pygame.image.load(os.path.join("location", "gloomy_forest_four.png"))
    assets['gloomy_forest'] = pygame.transform.scale(assets['gloomy_forest'], (WIDTH - 40, HEIGHT - 160))
    assets['outside_hawkins_lab'] = pygame.image.load(os.path.join("location", "hawkins_lab.png"))
    assets['outside_hawkins_lab'] = pygame.transform.scale(assets['outside_hawkins_lab'], (WIDTH - 40, HEIGHT - 160))
    assets['gloomy_forest_three'] = pygame.image.load(os.path.join("location", "gloomy_forest_three.png"))
    assets['gloomy_forest_three'] = pygame.transform.scale(assets['gloomy_forest_three'], (WIDTH - 40, HEIGHT - 160))
    assets['gloomy_forest_one'] = pygame.image.load(os.path.join("location", "gloomy_forest_one.png"))
    assets['gloomy_forest_one'] = pygame.transform.scale(assets['gloomy_forest_one'], (WIDTH - 40, HEIGHT - 160))
    assets['hawkins_lab'] = pygame.image.load(os.path.join("location", "hawkins_lab.png"))
    assets['hawkins_lab'] = pygame.transform.scale(assets['hawkins_lab'], (WIDTH - 40, HEIGHT - 160))
    
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
    
    # Load Demogorgon image
    assets['demogorgon'] = pygame.image.load(os.path.join("character_images", "demogorgon.png"))
    assets['demogorgon'] = pygame.transform.scale(assets['demogorgon'], (150, 150))
    
    return assets

assets = load_assets()

# Game states
TITLE_SCREEN = 0
CHARACTER_SELECT = 1
LOADING_SCREEN = 2
GAME_START = 3
FIGHT_SCENE = 4

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

# Add new scenario-specific choices
EXPLORE_CHOICES = [
    "Go deeper into the forest",
    "Return to previous location"
]

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
    global explore_fade_alpha, explore_fade_in_alpha
    global vecna_fade_alpha, vecna_fade_in_alpha
    global hawkins_fade_alpha, hawkins_fade_in_alpha
    global shout_fade_alpha, shout_text_visible
    global explore_prompt_alpha, explore_choices_alpha
    global run_fade_alpha, run_text_visible
    global run_clicked
    global lightning_flash, lightning_timer

    if current_scenario == "EXPLORE":
        # Draw the green background with original fade effects
        if explore_fade_alpha < 255:
            screen.blit(assets['gloomy_forest'], (20, 20))
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(explore_fade_alpha)
            screen.blit(fade_surface, (0, 0))
            explore_fade_alpha += FADE_SPEED
        else:
            screen.fill((0, 0, 0))
            new_background = assets['gloomy_forest_three']
            new_background.set_alpha(explore_fade_in_alpha)
            screen.blit(new_background, (20, 20))
            
            if explore_fade_in_alpha < 255:
                explore_fade_in_alpha += FADE_SPEED
                
                # Draw the demogorgon with fade
                demogorgon = assets['demogorgon'].copy()
                demogorgon = pygame.transform.scale(demogorgon, (220, 220))
                demogorgon.set_alpha(explore_fade_in_alpha)
                demogorgon_rect = demogorgon.get_rect()
                demogorgon_rect.left = 160
                demogorgon_rect.bottom = HEIGHT - 120
                screen.blit(demogorgon, demogorgon_rect)
                
                # Draw the character with fade
                if selected_character in assets['characters']:
                    character = assets['characters'][selected_character]
                    scaled_character = pygame.transform.scale(character, (160, 160))
                    flipped_character = pygame.transform.flip(scaled_character, True, False)
                    character_with_alpha = flipped_character.copy()
                    character_with_alpha.set_alpha(explore_fade_in_alpha)
                    character_rect = character_with_alpha.get_rect()
                    character_rect.right = WIDTH - 160
                    character_rect.bottom = HEIGHT - 140
                    screen.blit(character_with_alpha, character_rect)
            else:
                # Draw fully opaque demogorgon
                demogorgon = assets['demogorgon'].copy()
                demogorgon = pygame.transform.scale(demogorgon, (220, 220))
                demogorgon_rect = demogorgon.get_rect()
                demogorgon_rect.left = 160
                demogorgon_rect.bottom = HEIGHT - 120
                screen.blit(demogorgon, demogorgon_rect)
                
                # Draw fully opaque character
                if selected_character in assets['characters']:
                    character = assets['characters'][selected_character]
                    scaled_character = pygame.transform.scale(character, (160, 160))
                    flipped_character = pygame.transform.flip(scaled_character, True, False)
                    character_rect = flipped_character.get_rect()
                    character_rect.right = WIDTH - 160
                    character_rect.bottom = HEIGHT - 140
                    screen.blit(flipped_character, character_rect)

                # Add new prompt and choices with fade effect
                if explore_fade_in_alpha >= 255:  # Only show after scene has faded in
                    # Create a slightly larger font for the prompt and choices
                    prompt_font = pygame.font.Font(os.path.join("fonts", "Pixellari.ttf"), 28)  # Increased from 24
                    
                    # Draw prompt
                    prompt_text = f"A Demogorgon appears! What will {selected_character} do?"
                    prompt_surface = prompt_font.render(prompt_text, True, (255, 255, 255))
                    prompt_surface.set_alpha(explore_prompt_alpha)
                    prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
                    screen.blit(prompt_surface, prompt_rect)

                    # Draw choices with the same larger font
                    if explore_prompt_alpha >= 255:
                        choices = ["Run", "Fight"]
                        prompt_font = pygame.font.Font(os.path.join("fonts", "Pixellari.ttf"), 28)
                        
                        # Calculate exact positions and areas for click detection
                        run_x = WIDTH // 2 - 150
                        run_y = HEIGHT - 60
                        
                        # Draw choices without alpha
                        run_text = prompt_font.render(choices[0], True, (255, 255, 255))
                        screen.blit(run_text, (run_x, run_y))
                        
                        fight_x = WIDTH // 2 + 100
                        fight_y = HEIGHT - 60
                        fight_text = prompt_font.render(choices[1], True, (255, 255, 255))
                        screen.blit(fight_text, (fight_x, fight_y))

                        # Debug rectangles
                        pygame.draw.rect(screen, (255, 0, 0), (run_x, run_y, run_text.get_width(), run_text.get_height()), 1)
                        pygame.draw.rect(screen, (255, 0, 0), (fight_x, fight_y, fight_text.get_width(), fight_text.get_height()), 1)

                    if explore_prompt_alpha < 255:
                        explore_prompt_alpha += FADE_SPEED

                    # If Run was clicked, start fading to black
                    if run_clicked:  # We'll add this variable
                        fade_surface = pygame.Surface((WIDTH, HEIGHT))
                        fade_surface.fill((0, 0, 0))
                        fade_surface.set_alpha(run_fade_alpha)
                        screen.blit(fade_surface, (0, 0))
                        
                        if run_fade_alpha < 255:
                            run_fade_alpha += FADE_SPEED
                        elif not run_text_visible:
                            run_text_visible = True
                            
                        # Show text and button after screen is black
                        if run_text_visible:
                            # Draw text - now with Max-specific message
                            text = assets['title_font'].render("Max ran away into the darkness alone...", True, (255, 255, 255))
                            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            screen.blit(text, text_rect)
                            
                            # Draw END button
                            button_width, button_height = 200, 50
                            button_x = (WIDTH - button_width) // 2
                            button_y = HEIGHT - 100
                            pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
                            
                            end_text = assets['button_font'].render("END", True, (255, 255, 255))
                            end_rect = end_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
                            screen.blit(end_text, end_rect)

    elif current_scenario == "VECNA_LAIR":
        if vecna_fade_alpha < 255:
            screen.blit(assets['gloomy_forest'], (20, 20))
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(vecna_fade_alpha)
            screen.blit(fade_surface, (0, 0))
            vecna_fade_alpha += FADE_SPEED
        else:
            screen.fill((0, 0, 0))
            new_background = assets['gloomy_forest_three']
            new_background.set_alpha(vecna_fade_in_alpha)
            screen.blit(new_background, (20, 20))
            
            if vecna_fade_in_alpha < 255:
                vecna_fade_in_alpha += FADE_SPEED

    elif current_scenario == "HAWKINS_LAB":
        if hawkins_fade_alpha < 255:
            screen.blit(assets['gloomy_forest'], (20, 20))
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(hawkins_fade_alpha)
            screen.blit(fade_surface, (0, 0))
            hawkins_fade_alpha += FADE_SPEED
        else:
            screen.fill((0, 0, 0))
            new_background = assets['outside_hawkins_lab']
            new_background.set_alpha(hawkins_fade_in_alpha)
            screen.blit(new_background, (20, 20))
            
            if hawkins_fade_in_alpha < 255:
                hawkins_fade_in_alpha += FADE_SPEED

    elif current_scenario == "SHOUT":
        # Draw the background
        screen.blit(assets['gloomy_forest'], (20, 20))
        
        # Draw the character
        if selected_character and selected_character in assets['characters']:
            character_image = assets['characters'][selected_character]
            character_image = pygame.transform.scale(character_image, (150, 150))
            character_rect = character_image.get_rect()
            character_rect.midbottom = (WIDTH // 2, HEIGHT - 140)
            screen.blit(character_image, character_rect)

        # Fade to black
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(shout_fade_alpha)
        screen.blit(fade_surface, (0, 0))
        
        if shout_fade_alpha < 255:
            shout_fade_alpha += FADE_SPEED
        elif not shout_text_visible:
            shout_text_visible = True

        # Show text and button after screen is black
        if shout_text_visible:
            # Draw text
            text = assets['title_font'].render("Nobody heard you...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            
            # Draw END button
            button_width, button_height = 200, 50
            button_x = (WIDTH - button_width) // 2
            button_y = HEIGHT - 100
            pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
            
            # Draw button text
            end_text = assets['button_font'].render("END", True, (255, 255, 255))
            end_rect = end_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            screen.blit(end_text, end_rect)

    else:
        # Reset all fade values when not in special scenarios
        explore_fade_alpha = 0
        explore_fade_in_alpha = 0
        vecna_fade_alpha = 0
        vecna_fade_in_alpha = 0
        hawkins_fade_alpha = 0
        hawkins_fade_in_alpha = 0

        # Draw the initial background
        screen.blit(assets['gloomy_forest'], (20, 20))

        # Only show prompts and choices in the main scenario
        if current_scenario == "MAIN":
            # Draw the character if selected
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

            # Draw location text
            font = assets['title_font']
            text_surface = font.render("LOCATION: THE UPSIDE DOWN", True, (255, 255, 255))
            text_surface.set_alpha(location_text_alpha)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 500))
            screen.blit(text_surface, text_rect)

            # Handle location text fade
            current_time = pygame.time.get_ticks()
            if current_time - location_text_timer > LOCATION_TEXT_DURATION:
                location_text_alpha = max(0, location_text_alpha - 5)

            # Draw prompt and choices only if location text has faded
            if location_text_alpha == 0:
                prompt_font = assets['button_font']
                prompt_text = "You Find Yourself In The Upside Down. What do you do?"
                prompt_surface = prompt_font.render(prompt_text, True, (255, 255, 255))
                prompt_rect = prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))
                screen.blit(prompt_surface, prompt_rect)

                choices = [
                    "Explore",
                    "Sneak into Vecna's Forest Lair",
                    "Shout for help",
                    "Find The Hawkins Lab"
                ]
                
                # Left choices
                screen.blit(prompt_font.render(choices[0], True, (255, 255, 255)), (50, HEIGHT - 60))
                screen.blit(prompt_font.render(choices[1], True, (255, 255, 255)), (50, HEIGHT - 30))
                
                # Right choices
                right_choice_x = WIDTH - 50 - prompt_font.size(choices[2])[0]
                screen.blit(prompt_font.render(choices[2], True, (255, 255, 255)), (right_choice_x, HEIGHT - 60))
                right_choice_x = WIDTH - 50 - prompt_font.size(choices[3])[0]
                screen.blit(prompt_font.render(choices[3], True, (255, 255, 255)), (right_choice_x, HEIGHT - 30))

# Add this new function near your other draw functions
def draw_explore_scene(screen, assets, selected_character):
    # Draw the green background
    screen.fill((0, 0, 0))
    screen.blit(assets['gloomy_forest_one'], (20, 20))
    
    # Draw the selected character on the right side
    if selected_character in assets['characters']:
        character = assets['characters'][selected_character]
        scaled_character = pygame.transform.scale(character, (150, 150))
        flipped_character = pygame.transform.flip(scaled_character, True, False)
        screen.blit(flipped_character, (WIDTH - 150, HEIGHT // 2))
    
    # Draw new choices
    choices = ["Run", "Fight"]
    prompt_font = assets['button_font']
    
    # Left choice (Run)
    screen.blit(prompt_font.render(choices[0], True, (255, 255, 255)), (50, HEIGHT - 60))
    
    # Right choice (Fight)
    right_choice_x = WIDTH - 50 - prompt_font.size(choices[1])[0]
    screen.blit(prompt_font.render(choices[1], True, (255, 255, 255)), (right_choice_x, HEIGHT - 60))

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
                        explore_character = character  # Set the explore character here
                        blink_timer = pygame.time.get_ticks()  # Reset blink timer when character is selected
                        print(f"Character selected: {selected_character}")  # Debug print
                
                if selected_character:
                    button_info = draw_character_select(screen, assets, selected_character)
                    if button_info:
                        button_x, button_y, button_width, button_height = button_info
                        if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                            game_state = LOADING_SCREEN
                            loading_progress = 0  # Reset loading progress
                            fade_alpha = 0  # Reset fade alpha
            elif game_state == GAME_START:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    print(f"Click detected at: {mouse_pos}")  # Debug print
                    
                    if current_scenario == "MAIN":
                        # Check for "Explore" click in the main scenario
                        if HEIGHT - 60 <= mouse_pos[1] <= HEIGHT - 30:  # Y position check
                            if 50 <= mouse_pos[0] <= 200:  # X position for "Explore"
                                print("Explore clicked!")
                                current_scenario = "EXPLORE"
                                explore_fade_alpha = 0
                                explore_fade_in_alpha = 0
                                explore_prompt_alpha = 0
                                explore_choices_alpha = 0
                    
                    elif current_scenario == "EXPLORE":
                        if explore_fade_in_alpha >= 255:  # Only after fade in is complete
                            if not run_clicked and not fight_sequence_started:
                                # Check for Fight button click
                                fight_x = WIDTH // 2 + 100
                                fight_y = HEIGHT - 60
                                fight_width = assets['button_font'].size("Fight")[0]
                                fight_height = assets['button_font'].size("Fight")[1]
                                
                                if (fight_x <= mouse_pos[0] <= fight_x + fight_width and 
                                    fight_y <= mouse_pos[1] <= fight_y + fight_height):
                                    print("Fight clicked!")
                                    fight_sequence_started = True
                                    game_state = FIGHT_SCENE  # Change the game state
                                    fight_fade_alpha = 0
                                    fight_fade_complete = False
                            
                            elif run_text_visible:  # If we're showing the ending screen
                                # Check for END button click
                                button_width, button_height = 200, 50
                                button_x = (WIDTH - button_width) // 2
                                button_y = HEIGHT - 100
                                
                                if (button_x <= mouse_pos[0] <= button_x + button_width and 
                                    button_y <= mouse_pos[1] <= button_y + button_height):
                                    print("END button clicked!")
                                    pygame.quit()
                                    sys.exit()

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
    elif game_state == FIGHT_SCENE:
        if not fight_fade_complete:
            # Fade transition code
            screen.blit(assets['gloomy_forest_three'], (20, 20))
            fade_surface = pygame.Surface((WIDTH, HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fight_fade_alpha)
            screen.blit(fade_surface, (0, 0))
            
            fight_fade_alpha += FADE_SPEED
            if fight_fade_alpha >= 255:
                fight_fade_complete = True
        else:
            # Draw checkerboard background
            square_size = WIDTH // 8
            for row in range(8):
                for col in range(8):
                    x = col * square_size
                    y = row * square_size
                    color = (139, 0, 0) if (row + col) % 2 == 0 else (0, 0, 0)
                    pygame.draw.rect(screen, color, (x, y, square_size, square_size))
            
            # Draw the Demogorgon
            demogorgon_img = assets['demogorgon']
            demo_size = 150
            scaled_demogorgon = pygame.transform.scale(demogorgon_img, (demo_size, demo_size))
            screen.blit(scaled_demogorgon, demogorgon_pos)
            
            # Draw the player character
            if selected_character in assets['characters']:
                character_img = assets['characters'][selected_character]
                char_size = 130
                scaled_char = pygame.transform.scale(character_img, (char_size, char_size))
                screen.blit(scaled_char, player_pos)
            
            # Draw border
            border_thickness = 20
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), border_thickness)
            
            # Handle countdown and chase logic
            if fight_fade_in_alpha < 255:
                fight_fade_in_alpha += FADE_SPEED
            elif not countdown_started:
                countdown_started = True
                last_countdown_update = pygame.time.get_ticks()
            
            if countdown_started and not chase_started:
                current_time = pygame.time.get_ticks()
                if current_time - last_countdown_update >= 1000:
                    countdown_timer -= 1
                    last_countdown_update = current_time
                    if countdown_timer <= 0:
                        chase_started = True
                
                # Draw countdown number
                if countdown_timer > 0:
                    countdown_font = pygame.font.Font(os.path.join("fonts", "Pixellari.ttf"), 72)
                    countdown_text = countdown_font.render(str(countdown_timer), True, (255, 255, 255))
                    text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(countdown_text, text_rect)
            
            # Start chase after countdown
            if chase_started:
                current_time = pygame.time.get_ticks()
                
                # Handle player movement
                keys = pygame.key.get_pressed()
                move_speed = 5
                
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    player_pos[0] = max(border_thickness, player_pos[0] - move_speed)
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    player_pos[0] = min(WIDTH - char_size - border_thickness, player_pos[0] + move_speed)
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    player_pos[1] = max(border_thickness, player_pos[1] - move_speed)
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    player_pos[1] = min(HEIGHT - char_size - border_thickness, player_pos[1] + move_speed)
                
                # Move Demogorgon towards player
                demo_speed = 2  # Slower speed
                if demogorgon_pos[0] < player_pos[0] - 200:  # Keep some distance
                    demogorgon_pos[0] += demo_speed
                elif demogorgon_pos[0] > player_pos[0] - 200:
                    demogorgon_pos[0] -= demo_speed
                
                if demogorgon_pos[1] < player_pos[1]:
                    demogorgon_pos[1] += demo_speed
                elif demogorgon_pos[1] > player_pos[1]:
                    demogorgon_pos[1] -= demo_speed
                
                # Handle fireball shooting
                if keys[pygame.K_SPACE] and current_time - last_fireball_time > FIREBALL_COOLDOWN:
                    # Create new fireball at player position
                    fireball_x = player_pos[0]
                    fireball_y = player_pos[1] + char_size // 2
                    
                    # Calculate direction to Demogorgon
                    dx = demogorgon_pos[0] - fireball_x
                    dy = demogorgon_pos[1] - fireball_y
                    
                    # Normalize the direction
                    distance = (dx * dx + dy * dy) ** 0.5
                    if distance > 0:  # Avoid division by zero
                        dx = dx / distance
                        dy = dy / distance
                    
                    # Store fireball with its direction
                    fireballs.append([fireball_x, fireball_y, dx, dy])
                    last_fireball_time = current_time
                
                # Update and draw fireballs
                for fireball in fireballs[:]:
                    # Recalculate direction to Demogorgon for homing effect
                    dx = demogorgon_pos[0] - fireball[0]
                    dy = demogorgon_pos[1] - fireball[1]
                    distance = (dx * dx + dy * dy) ** 0.5
                    if distance > 0:
                        dx = dx / distance
                        dy = dy / distance
                    
                    # Move fireball towards Demogorgon
                    fireball[0] += dx * FIREBALL_SPEED
                    fireball[1] += dy * FIREBALL_SPEED
                    
                    # Draw trail effect
                    trail_length = 5
                    for i in range(1, trail_length):
                        trail_x = fireball[0] - dx * i * 2
                        trail_y = fireball[1] - dy * i * 2
                        alpha = 100 - i * 20
                        trail_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                        pygame.draw.circle(trail_surface, (0, 100, 255, alpha), (10, 10), 10 - i)
                        screen.blit(trail_surface, (int(trail_x) - 10, int(trail_y) - 10))
                    
                    # Draw fireball with glow effect
                    glow_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (0, 100, 255, 100), (15, 15), 15)  # Outer glow
                    screen.blit(glow_surface, (int(fireball[0]) - 15, int(fireball[1]) - 15))
                    pygame.draw.circle(screen, (0, 100, 255), (int(fireball[0]), int(fireball[1])), 10)  # Core
                    
                    # Check collision with Demogorgon
                    demogorgon_rect = pygame.Rect(demogorgon_pos[0], demogorgon_pos[1], demo_size, demo_size)
                    fireball_rect = pygame.Rect(fireball[0] - 5, fireball[1] - 5, 10, 10)
                    
                    if demogorgon_rect.colliderect(fireball_rect):
                        fireballs.remove(fireball)
                        continue
                    
                    # Remove fireball if it goes off screen
                    if (fireball[0] < 0 or fireball[0] > WIDTH or 
                        fireball[1] < 0 or fireball[1] > HEIGHT):
                        fireballs.remove(fireball)

    pygame.display.flip()
    pygame.time.Clock().tick(60)  # Limit frame rate to 60 FPS

# Quit the game
pygame.quit()
sys.exit()
