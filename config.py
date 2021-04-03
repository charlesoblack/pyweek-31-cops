#! /usr/bin/env python

import pygame


width = 800
height = 600
fontname = 'Arial'
fontsize = 32
start_timer = 10

level_colors = ['#1ed6b7',
                '#6ec02e',
                '#d5aa1a',
                '#d96c15',
                '#1e49d6',
                '#ca2d1c',
                '#8a41cd',
                '#cd41ab',
                ]

num_levels = len(level_colors) - 2

raw_origins = [(width // 8, height),
               ((width * 3) // 8, height),
               ((width * 5) // 8, height),
               ((width * 7) // 8, height),
               (0, (height * 13) // 16 - 30),
               (width, (height * 13) // 16 - 30),
               (width // 8 - 60, (height * 9) // 16 + 30),
               ((width * 7) // 8 + 30, (height * 9) // 16 + 30),
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

story = ['Another day at the job... time to file some paperwork.',
         'Hump day... time for a coffee break.',
         'Finally done with all this crap...'
         ]

colorkey = '#f807cc'
