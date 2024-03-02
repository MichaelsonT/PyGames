#tutorial credits -> Tech With Tim
#https://www.youtube.com/watch?v=waY3LfJhQLY&ab_channel=TechWithTim

import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDHT = 50
PLAYER_HEIGHT = 60

PLAYER_VEL = 5

START_WIDTH = 10
STAR_HEIGHT = 20

STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, (255, 0, 0), player) #player color

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(WIDTH/2 - PLAYER_WIDHT/2, HEIGHT - PLAYER_HEIGHT, 
                         PLAYER_WIDHT, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000 # first star
    start_count = 0 #when we get the next star

    stars = []
    hit = False

    while run:
        
        start_count += clock.tick(60)
        
        #clock
        elapsed_time = time.time() - start_time

        #generating stars
        if start_count > star_add_increment:
            for _ in range(5):
                star_x = random.randint(0, WIDTH - START_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, START_WIDTH, STAR_HEIGHT) #star starting point
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50) #star aperance increment
            start_count = 0
    
        #Running the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        #controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + player.width <= WIDTH:
            player.x += PLAYER_VEL

        #moving stars
        for star in stars[:]: #copy of the list
            star.y += STAR_VEL
            if star.y > HEIGHT: #gets to the end of the screen
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player): # see if the player got hit while the star is on the bottom
                #colliderect sees if 2 rects collided
                stars.remove(star)
                hit = True
                break  

        #Losing the game
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)
    
    pygame.quit()

if __name__ == "__main__":
    main()
    