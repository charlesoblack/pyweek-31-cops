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
        self.font_color = pygame.Color(180, 180, 180)

        self.start_game()
        self.run()

    def start_game(self):
        self.level = 0
        self.start_timer = 10
        self.points = 0

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

    def blit_infos(self):
        level_text = self.font.render(f'Level: {self.level}',
                                      True,
                                      self.font_color,
                                      )

        level_rect = level_text.get_rect(topleft=(10, 5))

        self.surface.blit(level_text, level_rect)

        time_text = self.font.render(f'Time left: {self.time_left:02.0f}',
                                     True,
                                     self.font_color,
                                     )

        time_rect = time_text.get_rect(topright=(config.width - 10, 5))

        self.surface.blit(time_text, time_rect)

        points_text = self.font.render(f'Points: {self.points:03.0f}',
                                       True,
                                       self.font_color,
                                       )

        points_rect = points_text.get_rect(midtop=(config.width // 2, 5))

        self.surface.blit(points_text, points_rect)

    def blit_score(self):
        points_text = self.font.render(f'Final tally: {self.points:03.0f}',
                                       True,
                                       self.font_color,
                                       )

        points_rect = points_text.get_rect(center=(config.width // 2,
                                                   config.height // 2))

        self.surface.blit(points_text, points_rect)

        restart_text = self.font.render(f'Press R to restart',
                                        True,
                                        self.font_color,
                                        )

        restart_rect = restart_text.get_rect(center=(config.width // 2,
                                                     config.height // 2 + 40))

        self.surface.blit(restart_text, restart_rect)

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    color = keys_colors.get(event.key, None)

                    if color == 'quit':
                        pygame.quit()
                        sys.exit()

                    if self.level > 0:
                        self.reset_surface()
                        self.blit_score()
                        if color == 'restart':
                            self.start_game()
                            start_time = time.time()
                    else:
                        print(self.points, color)

                        if self.right_color == color:
                            self.points += 1
                            self.reset_surface()
                            self.blit_infos()
                            self.place_random_block()

            pygame.display.flip()

        return


pygame.display.init()
pygame.font.init()

COPS()
