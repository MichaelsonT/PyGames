import pygame
import sys 
import main
#import music
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = main.WIN #pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Space Dodge")

BG = main.BG

FONT = main.FONT


def draw_button(button_rect, text, mouse_pos, button_color=(200, 200, 200), text_color=(0, 0, 0)): # Draws a button and changes its color when hovered over.
    
    if button_rect.collidepoint(mouse_pos): #See if mouse is on botton 
        button_color = (255, 255, 255)  # Highlight color 
    pygame.draw.rect(WIN, button_color, button_rect)
    
    text_surf = FONT.render(text, True, text_color)  # Render the text
    text_rect = text_surf.get_rect(center=button_rect.center)  # Center text in button
    WIN.blit(text_surf, text_rect)


def main_menu():
    start_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 - 50, 200, 50)
    
    level_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 10, 200, 50)

    quit_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50)


    running = True
    while running:
        WIN.blit(BG, (0, 0))  # Draw the background
        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        # Draw buttons
        draw_button(start_button, "Start", mouse_pos)  
        draw_button(level_button, "Levels", mouse_pos)
        draw_button(quit_button, "Quit", mouse_pos)  
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Exit the function and stop the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    running = False  # Exit menu loop to start the game
                if level_button.collidepoint(mouse_pos):
                    running = False # Exit menu loop to start the Levels Tab
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return  # Exit the function and stop the game

        pygame.display.update()
