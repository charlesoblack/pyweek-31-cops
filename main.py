#! /usr/bin/env python

import pygame
import config
import sys
import random
import time


class COPS(object):

    def __init__(self):
        self.width, self.height = config.width, config.height
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('COPS: Cops Organize Paper Stacks')

        self.font = pygame.font.SysFont(config.fontname, config.fontsize)
        self.font_color = pygame.Color(230, 230, 230)

        self.clock = pygame.time.Clock()

        self.start_game()
        self.run()

    def start_game(self):
        self.level = 1
        self.start_timer = 10
        self.points = 0
        self.base_surface = pygame.Surface((self.width, self.height))
        self.old_blocks = []
        self.blit_background()

    def blit_background(self):
        # TODO
        background = pygame.Surface((self.width, self.height))
        # blit background based on level?
        self.base_surface.blit(background, (0, 0))

    def reset_surface(self):
        self.surface.fill(pygame.Color(0, 0, 0))

    def reset_to_base_surface(self):
        self.surface.blit(self.base_surface, (0, 0))

    @property
    def current_colors(self):
        return config.level_colors[: self.level + 2]

    @property
    def game_over(self):
        return self.level > config.num_levels

    def place_random_block(self):
        self.right_color = random.choice(self.current_colors)

    def blit_text(self, text, **location):
        render = self.font.render(text, True, self.font_color)
        rect = render.get_rect(**location)
        self.surface.blit(render, rect)

    def blit_infos(self):
        self.blit_text(f'Level: {self.level}', topleft=(10, 5))
        self.blit_text(f'Time left: {self.time_left:02.0f}',
                       topright=(self.width - 10, 5))
        self.blit_text(f'Points: {self.points:03.0f}',
                       midtop=(self.width // 2, 5))

    def blit_final_score(self):
        self.blit_text(f'Final tally: {self.points:03.0f}',
                       center=(self.width // 2,
                               self.height // 2))
        self.blit_text(f'Press R to restart',
                       center=(self.width // 2,
                               self.height // 2 + 40))

    def blit_block(self, color, **location):
        block = pygame.Surface((50, 50))
        block_location = block.get_rect(**location)
        block.fill(pygame.Color(*color))

        self.surface.blit(block, block_location)

    def blit_current_block(self):
        self.blit_block(self.right_color,
                        center=(self.width // 2, self.height // 2))

    @staticmethod
    def interpolate(origin, percent):
        center_width = ((100 - percent) * config.width // 200
                        + percent * origin[0] // 100)
        center_height = ((100 - percent) * config.height // 200
                         + percent * origin[1] // 100)
        return (center_width, center_height)

    def blit_old_blocks(self):
        for (color, percent) in self.old_blocks:
            if percent >= 100:
                continue
            # implicit else
            origin = config.origins[color]
            self.blit_block(color, center=self.interpolate(origin, percent))
        self.old_blocks = [(color, percent + 1)
                           for color, percent in self.old_blocks]

    def run(self):

        keys_colors = {pygame.K_UP: (255, 0, 0),
                       pygame.K_DOWN: (255, 0, 255),
                       pygame.K_LEFT: (0, 255, 0),
                       pygame.K_RIGHT: (0, 0, 255),
                       pygame.K_a: (0, 255, 255),
                       pygame.K_s: (255, 255, 0),
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

            if self.game_over:
                self.reset_surface()
                self.blit_final_score()
            else:
                self.reset_to_base_surface()
                self.blit_infos()
                self.blit_current_block()
                self.blit_old_blocks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    color = keys_colors.get(event.key, None)

                    if color == 'quit':
                        pygame.quit()
                        sys.exit()

                    if self.game_over:
                        if color == 'restart':
                            self.start_game()
                            self.place_random_block()
                            start_time = time.time()
                    else:
                        print(self.points, color)

                        if self.right_color == color:
                            self.points += 1
                            self.old_blocks.append((color, 0))
                            self.place_random_block()

            pygame.display.flip()
            self.clock.tick(60)

        return


pygame.display.init()
pygame.font.init()

COPS()
