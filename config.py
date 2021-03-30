#! /usr/bin/env python

import pygame


width = 800
height = 600
fontname = 'Arial'
fontsize = 32
start_timer = 10

level_colors = [(255, 0, 0),  # red
                (255, 0, 255),  # magenta
                (0, 255, 0),  # green
                (0, 0, 255),  # blue
                (0, 255, 255),  # cyan
                (255, 255, 0),  # yellow
                (255, 255, 255),  # white
                (190, 140, 0),  # brown
                ]

num_levels = len(level_colors) - 2

raw_origins = [
               (width // 8, height),
               ((width * 3) // 8, height),
               ((width * 5) // 8, height),
               ((width * 7) // 8, height),
               (width // 8, (height * 13) // 16),
               ((width * 7) // 8, (height * 13) // 16),
               (width // 8, (height * 9) // 16),
               ((width * 7) // 8, (height * 9) // 16),
               ]

# 1/8 + 2/8 i
# 9/16 + 1/4 height, 1/8 and 7/8

origins = {k: v for k, v in zip(level_colors, raw_origins)}

keys = [pygame.K_d,
        pygame.K_f,
        pygame.K_j,
        pygame.K_k,
        pygame.K_s,
        pygame.K_l,
        pygame.K_a,
        pygame.K_SEMICOLON,
        ]

keys = {k: v for k, v in zip(keys, level_colors)}

keys[pygame.K_q] = 'quit'
keys[pygame.K_r] = 'restart'
