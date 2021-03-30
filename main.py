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

        try:
            with open('highscore.txt', 'r') as f:
                self.highscore = int(f.read())
        except (FileNotFoundError, ValueError):
            self.highscore = 0

        self.load_sounds()

        self.main_menu()

    def load_sounds(self):
        self.good_wav = pygame.mixer.Sound('fx/good.wav')
        self.bad_wav = pygame.mixer.Sound('fx/bad.wav')
        self.level_wav = pygame.mixer.Sound('fx/level_finished.wav')

    def main_menu(self):

        self.blit_menu_splash()

        start = False

        while not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quit()
                    elif event.key == pygame.K_SPACE:
                        start = True
                    else:
                        pass

            pygame.display.flip()
            self.clock.tick(60)

        self.start_game()
        self.run()

    def level_menu(self):

        if self.level == 4:
            self.blit_coffee_break()
        else:
            self.blit_level_splash()

        self.level_wav.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quit()
                    elif event.key == pygame.K_SPACE:
                        self.old_blocks = []
                        self.place_random_block()
                        self.level += 1
                        return
                    else:
                        pass

            pygame.display.flip()
            self.clock.tick(60)

    def blit_coffee_break(self):
        # TODO
        coffee_splash = pygame.Surface((self.width, self.height))
        coffee_splash.fill((0, 0, 200))

        self.surface.blit(coffee_splash, (0, 0))

    def blit_menu_splash(self):
        # TODO
        menu_splash = pygame.Surface((self.width, self.height))
        menu_splash.fill((60, 60, 60))

        self.surface.blit(menu_splash, (0, 0))

    def blit_level_splash(self):
        # TODO
        level_splash = pygame.Surface((self.width, self.height))
        level_splash.fill((200, 0, 0))
        # modify based on level?

        self.surface.blit(level_splash, (0, 0))

    def start_game(self):
        self.level = 1
        self.start_timer = config.start_timer
        self.points = 0
        self.base_surface = pygame.Surface((self.width, self.height))
        self.old_blocks = []
        self.blit_background()

    def blit_background(self):
        # TODO
        background = pygame.image.load('gfx/background.png').convert()
        background = pygame.transform.scale(background,
                                            (config.width, config.height))
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

        self.blit_text(f'High score: {self.highscore}',
                       center=(self.width // 2,
                               self.height // 2 + 80))

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
            color = tuple([max(x - 70, 0) for x in color])
            self.blit_block(color, center=self.interpolate(origin, percent))
        self.old_blocks = [(color, percent + 1)
                           for color, percent in self.old_blocks
                           if percent < 100]

    def run(self):
        start_time = time.time()
        self.time_left = self.start_timer + start_time - time.time()

        self.reset_surface()
        self.blit_infos()
        self.place_random_block()

        while True:
            self.time_left = self.start_timer + start_time - time.time()

            if self.time_left <= 0 and not self.game_over:
                self.level_menu()
                start_time = time.time()

            if self.game_over:
                self.highscore = max(self.highscore, self.points)
                self.reset_surface()
                self.blit_final_score()
            else:
                self.reset_to_base_surface()
                self.blit_infos()
                self.blit_old_blocks()
                self.blit_current_block()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    color = config.keys.get(event.key, None)

                    if color == 'quit':
                        self.quit()

                    if self.game_over:
                        if color == 'restart':
                            self.start_game()
                            self.place_random_block()
                            start_time = time.time()
                    else:
                        if self.right_color == color:
                            self.good_wav.play()
                            self.points += 1
                            self.old_blocks.append((color, 0))
                            self.place_random_block()
                        else:
                            self.bad_wav.play()

            pygame.display.flip()
            self.clock.tick(60)
        return

    def save_highscore(self):
        with open('highscore.txt', 'w') as f:
            f.write(str(self.highscore))

    def quit(self):
        self.save_highscore()
        pygame.quit()
        sys.exit()


pygame.display.init()
pygame.font.init()
pygame.mixer.init()

COPS()
