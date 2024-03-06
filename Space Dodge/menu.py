import pygame
import sys 
import main
import boss_room

pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load("menu_song.mp3")
pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely
pygame.mixer.music.set_volume(0.1)


WIDTH, HEIGHT = 1000, 800
WIN = main.screen #pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Space Dodge")

BG = main.BG

FONT = main.FONT30


def draw_button(button_rect, text, mouse_pos, button_color=(200, 200, 200), text_color=(0, 0, 0)): # Draws a button and changes its color when hovered over.
    
    if button_rect.collidepoint(mouse_pos): #See if mouse is on botton 
        button_color = (255, 255, 255)  # Highlight color 
    pygame.draw.rect(WIN, button_color, button_rect)
    
    text_surf = FONT.render(text, True, text_color)  # Render the text
    text_rect = text_surf.get_rect(center=button_rect.center)  # Center text in button
    WIN.blit(text_surf, text_rect)


def main_menu():
    start_button = pygame.Rect(WIDTH / 2 - 125, HEIGHT / 2 - 50, 250, 50)
    boss_button = pygame.Rect(WIDTH / 2 - 125, HEIGHT / 2 + 10, 250, 50)
    quit_button = pygame.Rect(WIDTH / 2 - 125, HEIGHT / 2 + 70, 250, 50)

    running = True
    while running:

        WIN.blit(BG, (0, 0))  # Draw the background

        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position

        # Draw buttons
        draw_button(start_button, "Survivel Mode", mouse_pos)  
        draw_button(boss_button, "Boss Battle", mouse_pos)
        draw_button(quit_button, "Quit", mouse_pos)  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Exit the function and stop the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    pygame.mixer.music.load("space.mp3")
                    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely
                    pygame.mixer.music.set_volume(0.1)
                    main.game()  # Exit menu loop to start the game

                elif boss_button.collidepoint(mouse_pos):
                    pygame.mixer.music.load("boss_music.mp3")
                    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely
                    pygame.mixer.music.set_volume(0.1)
                    boss_room.game_boss() # Exit menu loop to start the Levels Tab

                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return  # Exit the function and stop the game

        pygame.display.update()
