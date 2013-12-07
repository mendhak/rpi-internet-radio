#!/usr/bin/python2


import random
import time
import pygame
import math
import array
import fcntl



pygame.init()
pygame.mixer.init()
pygame.font.init()
ThisSurface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
ThisVideoInfo = pygame.display.Info()
pygame.mouse.set_visible(False)
SmallFont = pygame.font.Font(None, 25)
LargeFont = pygame.font.Font(None, 100)

Background = ThisSurface.copy()

TextReady = SmallFont.render("HELLO WORLD", True, (0x00, 0x00, 0x00))
TextFin = SmallFont.render("DONE!", True, (0x00, 0xFF, 0xFF))


# Set background color
ThisSurface.fill((0xFF, 0xFF, 0x00))
#ThisSurface.fill((0x00, 0x00, 0x00))

# Write some text
ThisSurface.blit(TextReady, (130, 212))

#Draw a line
pygame.draw.line(ThisSurface, (0xFF, 0x00, 0x00), [125,125], [125,55], 4)
#pygame.draw.line(ThisSurface, (0xFF, 0x00, 0x00), [155, 125], [155, 55], 4)
pygame.draw.arc(ThisSurface, (0xFF, 0x00, 0x00), (125, 25, 40, 40), 0, math.pi, 5)
pygame.draw.circle(ThisSurface, (0xFF, 0x00, 0x00), [105,125], 22, 5)
#pygame.draw.circle(ThisSurface, (0xFF, 0x00, 0x00), [145, 125], 22, 5)



# "Renders an empty graticule"
# The graticule is divided into 10 columns x 8 rows
# Each cell is 50x40 pixels large, with 5 subdivisions per
# cell, meaning 10x8 pixels each.  Subdivision lines are
# displayed on the central X and Y axis
# Active area = 10,30 to 510,350 (500x320 pixels)
borderColor = (255, 255, 255)
lineColor = (64, 64, 64)
subDividerColor = (128, 128, 128)
# Outer border: 2 pixels wide
pygame.draw.rect(ThisSurface, borderColor, (8,28,504,324), 2)
# Horizontal lines (40 pixels apart)
for i in range(0, 7):
	y = 70+i*40
	pygame.draw.line(ThisSurface, lineColor, (10, y), (510, y))
# Vertical lines (50 pixels apart)
for i in range(0, 9):
	x = 60+i*50
	pygame.draw.line(ThisSurface, lineColor, (x, 30), (x, 350))
# Vertical sub-divisions (8 pixels apart)
for i in range(1, 40):
	y = 30+i*8
	pygame.draw.line(ThisSurface, subDividerColor, (258, y), (262, y))
# Horizontal sub-divisions (10 pixels apart)
for i in range(1, 50):
	x = 10+i*10
	pygame.draw.line(ThisSurface, subDividerColor, (x, 188), (x, 192))



# Render
pygame.display.flip()
pygame.time.wait(50)
time.sleep(5)

pygame.mouse.set_visible(True)



# Erase by redrawing the background
#ThisSurface.blit(Background, (0,0))
#Again set the background color
#ThisSurface.fill((0x00, 0xFF, 0x00))
#Send new text
#ThisSurface.blit(TextFin, (130, 212))
#pygame.display.flip()
#pygame.time.wait(50)
#time.sleep(3)





#f = open('/dev/fb1')
#
#HiScore = 0
#pygame.time.wait(25)
#ThisSurface.blit(Background, (0, 0))
#ThisSurface.fill((0xFF, 0xFF, 0x00))
#ThisSurface.blit(TextReady, (130, 212))
#pygame.display.flip()

#pygame.mouse.set_visible(True)

#f.close()

