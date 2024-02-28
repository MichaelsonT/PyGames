
import pygame, time, sys

pygame.mixer.init()


pygame.mixer.music.load("space.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)

input("enter to exit")

