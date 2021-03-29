#! /usr/bin/env python

import pygame
import config
import sys


pygame.display.init()
pygame.font.init()

play_surface = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption('COPS: Cops Organize Paper Stacks')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            break
