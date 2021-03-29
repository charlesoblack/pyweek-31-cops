#! /usr/bin/env python

import pygame
import config
import sys
import random
import time


class COPS(object):

    def __init__(self):
        self.surface = pygame.display.set_mode((config.width, config.height))
        pygame.display.set_caption('COPS: Cops Organize Paper Stacks')

        self.font = pygame.font.SysFont(config.fontname, config.fontsize)
        self.font_color = pygame.Color(230, 230, 230)

        self.start_game()
        self.run()

    def start_game(self):
        self.level = 0
        self.start_timer = 3
        self.points = 0
        self.base_surface = pygame.Surface((config.width, config.height))

    def reset_surface(self):
        self.surface.fill(pygame.Color(0, 0, 0))

    def reset_to_base_surface(self):
        self.surface.blit(self.base_surface, (0, 0))

    @property
    def current_colors(self):
        return config.level_colors[: self.level + 3]

    def place_random_block(self):
        self.right_color = random.choice(self.current_colors)

        block = pygame.Surface((50, 50))
        block_location = ((config.width - 50) // 2, (config.height - 50) // 2)
        block.fill(pygame.Color(*self.right_color))

        self.base_surface.blit(block, block_location)

    def blit_text(self, text, **location):
        render = self.font.render(text, True, self.font_color)
        rect = render.get_rect(**location)
        self.surface.blit(render, rect)

    def blit_infos(self):
        self.blit_text(f'Level: {self.level}', topleft=(10, 5))
        self.blit_text(f'Time left: {self.time_left:02.0f}',
                       topright=(config.width - 10, 5))
        self.blit_text(f'Points: {self.points:03.0f}',
                       midtop=(config.width // 2, 5))

    def blit_final_score(self):
        self.blit_text(f'Final tally: {self.points:03.0f}',
                       center=(config.width // 2,
                               config.height // 2))
        self.blit_text(f'Press R to restart',
                       center=(config.width // 2,
                               config.height // 2 + 40))

    def run(self):

        keys_colors = {pygame.K_UP: (255, 0, 0),
                       pygame.K_DOWN: (255, 0, 255),
                       pygame.K_LEFT: (0, 255, 0),
                       pygame.K_RIGHT: (0, 0, 255),
                       pygame.K_q: 'quit',
                       pygame.K_r: 'restart',
                       }

        start_time = time.time()
        self.time_left = self.start_timer + start_time - time.time()

        self.reset_surface()
        self.blit_infos()
        self.place_random_block()

        while True:
            self.time_left = self.start_timer + start_time - time.time()

            if self.time_left <= 0:
                self.level += 1
                start_time = time.time()

            if self.level > 1:
                self.reset_surface()
                self.blit_final_score()
            else:
                self.reset_to_base_surface()
                self.blit_infos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    color = keys_colors.get(event.key, None)

                    if color == 'quit':
                        pygame.quit()
                        sys.exit()

                    if self.level > 1:
                        if color == 'restart':
                            self.start_game()
                            self.place_random_block()
                            start_time = time.time()
                    else:
                        print(self.points, color)

                        if self.right_color == color:
                            self.points += 1
                            self.place_random_block()

            pygame.display.flip()

        return


pygame.display.init()
pygame.font.init()

COPS()
