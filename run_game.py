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
        pygame.display.set_caption('C.O.P.S.: Cops Organize Paper Stacks')

        self.font = pygame.font.SysFont(config.fontname, config.fontsize)
        self.font_color = pygame.Color(30, 30, 30)

        self.clock = pygame.time.Clock()

        try:
            with open('highscore.txt', 'r') as f:
                self.highscore = int(f.read())
        except (FileNotFoundError, ValueError):
            self.highscore = 0

        self.block = pygame.image.load('gfx/paper.png').convert()
        self.block = pygame.transform.scale(self.block,
                                            (50, 50))

        self.cop_left = pygame.image.load('gfx/cop_left.png').convert_alpha()
        # self.cop_left.set_colorkey(config.colorkey)
        self.cop_left = pygame.transform.scale(self.cop_left,
                                               (config.width, config.height))

        self.cop_closeleft = pygame.image.load('gfx/cop_closeleft.png').convert_alpha()  # noqa
        # self.cop_closeleft.set_colorkey(config.colorkey)
        self.cop_closeleft = pygame.transform.scale(self.cop_closeleft,
                                                    (config.width, config.height))  # noqa

        self.cop_right = pygame.image.load('gfx/cop_right.png').convert_alpha()
        # self.cop_right.set_colorkey(config.colorkey)
        self.cop_right = pygame.transform.scale(self.cop_right,
                                                (config.width, config.height))

        self.cop_closeright = pygame.image.load('gfx/cop_closeright.png').convert_alpha()  # noqa
        # self.cop_closeright.set_colorkey(config.colorkey)
        self.cop_closeright = pygame.transform.scale(self.cop_closeright,
                                                     (config.width, config.height))  # noqa

        self.cop_front = pygame.image.load('gfx/cop_front.png').convert_alpha()
        # self.cop_front.set_colorkey(config.colorkey)
        self.cop_front = pygame.transform.scale(self.cop_front,
                                                (config.width, config.height))

        self.cop_coffee_1 = pygame.image.load('gfx/cop_coffee_1.png').convert_alpha()  # noqa
        self.cop_coffee_1 = pygame.transform.scale(self.cop_coffee_1,
                                                   (config.width, config.height))  # noqa

        self.cop_coffee_2 = pygame.image.load('gfx/cop_coffee_2.png').convert_alpha()  # noqa
        self.cop_coffee_2 = pygame.transform.scale(self.cop_coffee_2,
                                                   (config.width, config.height))  # noqa

        cop_images = [self.cop_closeleft,
                      self.cop_closeleft,
                      self.cop_closeright,
                      self.cop_closeright,
                      self.cop_left,
                      self.cop_right,
                      self.cop_left,
                      self.cop_right,
                      ]

        self.cop = {k: v for k, v in zip(config.keys, cop_images)}
        self.cop['none'] = self.cop_front
        self.last_keypress = 'none'

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

        self.blit_story(0)
        self.start_game()
        self.run()

    def blit_story(self, part):

        self.surface.fill((230, 230, 230))

        self.blit_text(config.story[part],
                       center=(self.width // 2, self.height // 2))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quit()
                    elif event.key == pygame.K_SPACE:
                        return
                    else:
                        pass

            pygame.display.flip()
            self.clock.tick(60)

    def level_menu(self):

        self.last_keypress = 'none'

        if self.level == 4:
            self.blit_story(1)

        self.level_wav.play()
        self.place_random_block()

        frame = 0

        while True:
            frame = (frame + 1) % 60
            if self.level == 4:
                self.blit_coffee_break(frame >= 30)
            else:
                self.blit_level_splash()

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

    def blit_coffee_break(self, frame_2):
        self.reset_to_base_surface()
        if frame_2:
            frame = self.cop_coffee_2
        else:
            frame = self.cop_coffee_1
        self.surface.blit(frame, (0, 0))

    def blit_menu_splash(self):
        menu_splash = pygame.image.load('gfx/main.png').convert()
        menu_splash = pygame.transform.scale(menu_splash,
                                             (config.width, config.height))

        self.surface.blit(menu_splash, (0, 0))

    def blit_level_splash(self):
        level_splash = pygame.image.load('gfx/level_splash.png').convert()
        level_splash = pygame.transform.scale(level_splash,
                                              (config.width, config.height))

        self.surface.blit(level_splash, (0, 0))

    def start_game(self):
        self.level = 1
        self.start_timer = config.start_timer
        self.points = 0
        self.base_surface = pygame.Surface((self.width, self.height))
        self.old_blocks = []
        self.blit_background()

    def blit_background(self):
        background = pygame.image.load('gfx/background.png').convert()
        background = pygame.transform.scale(background,
                                            (config.width, config.height))

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
        self.reset_surface()
        self.end_screen = pygame.image.load('gfx/final.png').convert()
        self.surface.blit(self.end_screen, (0, 0))
        self.blit_text(f'Final tally: {self.points:03.0f}',
                       center=(self.width // 2,
                               self.height // 2))
        self.blit_text(f'High score: {self.highscore}',
                       center=(self.width // 2,
                               self.height // 2 + 40))
        self.blit_text(f'Press R to restart',
                       center=(self.width // 2,
                               self.height // 2 + 80))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.quit()
                    elif event.key == pygame.K_r:
                        self.start_game()
                        self.place_random_block()
                        self.start_time = time.time()
                        return
                    else:
                        pass

            pygame.display.flip()
            self.clock.tick(60)

    def blit_block(self, color, darker=False, **location):
        block_location = self.block.get_rect(**location)

        # modify color appropriately
        modification = (pygame.Color(70, 70, 70, 0)
                        if darker
                        else pygame.Color(0, 0, 0, 0))
        color = pygame.Color(color) - modification

        self.block.set_colorkey('#00ff00')

        color_mask = pygame.mask.from_threshold(self.block,
                                                pygame.Color(config.colorkey),
                                                # threshold
                                                pygame.Color(10, 10, 10, 255),
                                                )

        colored_part = color_mask.to_surface(setcolor=color, unsetcolor=None)
        colored_block = self.block.copy()
        colored_block.blit(colored_part, (0, 0))

        self.surface.blit(colored_block, block_location)

    def blit_current_block(self):
        self.blit_block(self.right_color,
                        center=(self.width // 2, self.height // 2 + 40))

    @staticmethod
    def interpolate(origin, percent):
        center_width = ((100 - percent) * config.width // 200
                        + percent * origin[0] // 100)
        center_height = ((100 - percent) * (config.height // 2 + 40) // 100
                         + percent * origin[1] // 100)
        return (center_width, center_height)

    def blit_old_blocks(self):
        for (color, percent) in self.old_blocks:
            if percent >= 100:
                continue
            # implicit else
            origin = config.origins[color]
            self.blit_block(color,
                            True,  # make it darker
                            center=self.interpolate(origin, percent),
                            )
        self.old_blocks = [(color, percent + 2)
                           for color, percent in self.old_blocks
                           if percent < 80]

    def blit_cop(self):
        cop_image = self.cop.get(self.last_keypress, self.cop_front)
        location = cop_image.get_rect(center=(config.width // 2 + 20,
                                              config.height // 2))
        self.surface.blit(cop_image, location)

    def run(self):
        self.start_time = time.time()
        self.time_left = self.start_timer + self.start_time - time.time()

        self.reset_surface()
        self.blit_infos()
        self.place_random_block()
        self.blit_cop()

        while True:
            self.time_left = self.start_timer + self.start_time - time.time()

            if self.time_left <= 0 and not self.game_over:
                self.level_menu()
                self.start_time = time.time()

            if self.game_over:
                self.highscore = max(self.highscore, self.points)
                self.reset_surface()
                self.blit_story(2)
                self.blit_final_score()
            else:
                self.reset_to_base_surface()
                self.blit_infos()
                self.blit_old_blocks()
                self.blit_current_block()
                self.blit_cop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    color = config.keys.get(event.key, None)

                    self.last_keypress = event.key

                    if color == 'quit':
                        self.quit()

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
