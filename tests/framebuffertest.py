#!/usr/bin/python2


import random
import time
import pygame
import math
import array
import fcntl
import os

os.environ['SDL_VIDEODRIVER']="fbcon"
os.environ["FRAMEBUFFER"]="/dev/fb1"
os.environ["SDL_FBDEV"] = "/dev/fb1"

pygame.init()
pygame.font.init()
ThisSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.mouse.set_visible(False)
SmallFont = pygame.font.Font(None, 25)
LargeFont = pygame.font.Font(None,180)

Background = ThisSurface.copy()

while True:
	TextReady = LargeFont.render(time.strftime("%S"), True, (0x00, 0xFF, 0x00))
	textrect = TextReady.get_rect()
	textrect.centerx = ThisSurface.get_rect().centerx
	textrect.centery = ThisSurface.get_rect().centery

	# Set background color
	ThisSurface.fill((0x00, 0x00, 0x00))
	
	# Write some text
	ThisSurface.blit(TextReady, textrect)
	
	# Render
	pygame.display.flip()
	time.sleep(1)

pygame.mouse.set_visible(True)



