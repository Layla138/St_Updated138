import pygame
import time
import sys  # Add this import at the top of the file
from constants import *

def draw_title_screen(screen, assets):
    screen.blit(assets['wallpaper'], (20, 20))
    title_text = "Welcome to the"
    subtitle_text = "Stranger Things adventure game!"
    title_surface = assets['title_font'].render(title_text, True, WHITE)
    subtitle_surface = assets['title_font'].render(subtitle_text, True, WHITE)
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, HEIGHT - 200)))
    screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(WIDTH // 2, HEIGHT - 160)))
    pygame.draw.rect(screen, RED, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    play_text = assets['button_font'].render("PLAY", True, WHITE)
    screen.blit(play_text, play_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))

def handle_title_screen_click(mouse_pos):
    return (BUTTON_X <= mouse_pos[0] <= BUTTON_X + BUTTON_WIDTH and 
            BUTTON_Y <= mouse_pos[1] <= BUTTON_Y + BUTTON_HEIGHT)

def draw_character_select(screen, assets, selected_character):
    screen.blit(assets['wallpaper'], (20, 20))
    title_text = "Select Your Character"
    title_surface = assets['title_font'].render(title_text, True, WHITE)
    screen.blit(title_surface, title_surface.get_rect(center=(WIDTH // 2, 50)))
    
    for i, character in enumerate(CHARACTERS):
        x = 150 + (i % 3) * 200
        y = 150 + (i // 3) * 150
        if character in assets['character_images']:
            screen.blit(assets['character_images'][character], (x, y))
        name_text = assets['button_font'].render(character, True, WHITE)
        screen.blit(name_text, name_text.get_rect(center=(x + 50, y + 120)))
        
        if character == selected_character:
            pygame.draw.rect(screen, RED, (x-5, y-5, 110, 110), 3)
    
    if selected_character:
        pygame.draw.rect(screen, RED, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
        start_text = assets['button_font'].render("Start Game", True, WHITE)
        screen.blit(start_text, start_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2)))

def handle_character_select_click(mouse_pos, assets):
    for i, character in enumerate(CHARACTERS):
        x = 150 + (i % 3) * 200
        y = 150 + (i // 3) * 150
        if x <= mouse_pos[0] <= x + 100 and y <= mouse_pos[1] <= y + 100:
            return character
    return None

def draw_loading_screen(screen, assets):
    screen.fill(BLACK)
    screen.blit(assets['wallpaper'], (20, 20))
    loading_text = assets['title_font'].render("Game loading...", True, WHITE)
    screen.blit(loading_text, loading_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    
    # Loading bar
    bar_width = 300
    bar_height = 20
    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT // 2 + 50
    
    loading_progress = 0
    while loading_progress < 100:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Return False instead of quitting directly
        
        # Draw empty bar
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Draw filled portion of bar
        fill_width = int(bar_width * loading_progress / 100)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, fill_width, bar_height))
        
        pygame.display.flip()
        
        # Update loading progress
        loading_progress += 2
        time.sleep(0.05)
    
    return True

def draw_game(screen, assets, player):
    screen.blit(assets['gloomy_forest'], (20, 20))
    if player.image and player.rect:
        screen.blit(player.image, player.rect)
    
    prompt_surface = assets['title_font'].render(PROMPT, True, WHITE)
    screen.blit(prompt_surface, prompt_surface.get_rect(center=(WIDTH // 2, HEIGHT - 150)))
    
    choice_rects = []
    for i, choice in enumerate(CHOICES):
        choice_surface = assets['button_font'].render(choice, True, WHITE)
        choice_rect = choice_surface.get_rect(topleft=(50 + (i % 3) * 250, HEIGHT - 100))
        screen.blit(choice_surface, choice_rect)
        choice_rects.append(choice_rect)
    
    return choice_rects

def handle_game_start_click(mouse_pos, screen, assets, player):
    choice_rects = draw_game(screen, assets, player)
    for i, rect in enumerate(choice_rects):
        if rect.collidepoint(mouse_pos):
            if i == 0:  # Player chose "Explore"
                print("Player chose to explore!")
            elif i == 1:  # Player chose "Wait"
                print("Player chose to wait!")
            elif i == 2:  # Player chose "Call for help"
                print("Player called for help!")