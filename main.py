#! /usr/bin/env python

import pygame
import config
import sys
import random


class COPS(object):

    def __init__(self):

        self.level = 0
        self.surface = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption('COPS: Cops Organize Paper Stacks')
        self.run()

    def reset_surface(self):
        self.surface.fill(pygame.Color(0, 0, 0))

    @property
    def current_colors(self):
        return config.level_colors[: self.level + 3]

    def place_random_block(self):
        self.right_color = random.choice(self.current_colors)

        block = pygame.Surface((50, 50))
        block_location = ((config.width - 50) // 2, (config.height - 50) // 2)
        block.fill(pygame.Color(*self.right_color))

        self.surface.blit(block, block_location)

    def run(self):

        keys_colors = {pygame.K_UP: (255, 0, 0),
                       pygame.K_DOWN: (255, 0, 255),
                       pygame.K_LEFT: (0, 255, 0),
                       pygame.K_RIGHT: (0, 0, 255),
                       pygame.K_q: 'quit',
                       }

        self.reset_surface()
        self.place_random_block()

        self.points = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    color = keys_colors.get(event.key, None)

                    if color == 'quit':
                        pygame.quit()
                        sys.exit()

                    print(self.points, color)

                    if self.right_color == color:
                        self.points += 1
                        self.reset_surface()
                        self.place_random_block()

            pygame.display.flip()

        return


pygame.display.init()
pygame.font.init()

COPS()
