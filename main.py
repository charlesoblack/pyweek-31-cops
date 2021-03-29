#! /usr/bin/env python

import pygame
import config
import sys
import random


def reset_surface(surface):
    surface.fill(pygame.Color(0, 0, 0))
    return surface


def place_random_block(surface, key_colors):
    random_color = random.choice(list(key_colors.values()))

    block = pygame.Surface((50, 50))
    block_location = ((config.width - 50) // 2, (config.height - 50) // 2)
    block.fill(random_color)

    surface.blit(block, block_location)

    return surface, random_color


def main_game_loop(surface):

    keys_colors = {pygame.K_UP: pygame.Color(255, 0, 0),
                   pygame.K_DOWN: pygame.Color(255, 0, 255),
                   pygame.K_LEFT: pygame.Color(0, 255, 0),
                   pygame.K_RIGHT: pygame.Color(0, 0, 255),
                   pygame.K_q: 'quit',
                   }

    surface = reset_surface(surface)
    surface, right_color = place_random_block(surface, keys_colors)

    points = 0

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

                print(points, color)

                if right_color == color:
                    points += 1
                    surface = reset_surface(surface)
                    surface, right_color = place_random_block(surface,
                                                              keys_colors)

        pygame.display.flip()

    return


pygame.display.init()
pygame.font.init()

play_surface = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption('COPS: Cops Organize Paper Stacks')

main_game_loop(play_surface)
