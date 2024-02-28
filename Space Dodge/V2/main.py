#tutorial credits -> Tech With Tim
#https://www.youtube.com/watch?v=waY3LfJhQLY&ab_channel=TechWithTim

import pygame
import time
import random
import menu
#import music
pygame.font.init()
pygame.mixer.init()

#sounds
pygame.mixer.music.load("space.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)
boopsound = pygame.mixer.Sound("boop.mp3")

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

PLAYER_WIDHT = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

START_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
Ship_image = pygame.image.load("Ship.png")

FONT = pygame.font.SysFont("comicsans", 30)

class Player():
    def __init__(self, x, y):
        self.image = Ship_image
        self.widht = PLAYER_WIDHT
        self.height = PLAYER_HEIGHT
        self.rect = pygame.Rect(0, 0, self.widht, self.height)
        self.rect.center = (x, y)
    
    def moves(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x - PLAYER_VEL >= 0:
            self.rect.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and self.rect.x + self.widht <= WIDTH:
            self.rect.x += PLAYER_VEL
        if keys[pygame.K_UP] and self.rect.y + PLAYER_VEL > 0:
            self.rect.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and self.rect.y + self.height < HEIGHT:
            self.rect.y += PLAYER_VEL
    
    def draw(self):
        WIN.blit(self.image, (self.rect.x - 5, self.rect.y)) # center the rectangle
        #pygame.draw.rect(WIN, "red", self.rect, 2)




def draw(elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    
    WIN.blit(time_text, (10, 10))

    ship.draw()

    #pygame.draw.rect(WIN, (17, 216, 50), player) #player color

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

ship = Player(WIDTH/2 , HEIGHT - PLAYER_HEIGHT/2)


def game():
    run = True

    
    #player = Player(WIDTH/2 , HEIGHT - PLAYER_HEIGHT/2)
    player = pygame.Rect(WIDTH/2 - PLAYER_WIDHT/2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDHT, PLAYER_HEIGHT) #player
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
                break # Exit the function and stop the game

        #controls
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
        #    player.x -= PLAYER_VEL
        #if keys[pygame.K_RIGHT] and player.x + player.width <= WIDTH:
        #    player.x += PLAYER_VEL
        
        #controls
        ship.moves()

        #moving stars
        for star in stars[:]: #copy of the list
            star.y += STAR_VEL
            if star.y > HEIGHT: #gets to the end of the screen
                stars.remove(star)
            elif star.y + star.height >= PLAYER_HEIGHT and star.colliderect(ship): # see if the player got hit while the star is on the bottom
                #colliderect sees if 2 rects collided
                stars.remove(star)
                hit = True
                boopsound.set_volume(0.1)
                boopsound.play()
                break  

        #Losing the game
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(elapsed_time, stars)
    
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    menu.main_menu()
    game()
    