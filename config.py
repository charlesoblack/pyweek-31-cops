#! /usr/bin/env python

width = 800
height = 600
fontname = 'Arial'
fontsize = 32
start_timer = 3

level_colors = [(255, 0, 0),  # red
                (255, 0, 255),  # magenta
                (0, 255, 0),  # green
                (0, 0, 255),  # blue
                (0, 255, 255),  # cyan
                (255, 255, 0),  # yellow
                (255, 255, 255),  # white
                (190, 140, 0),  # brown?
                ]

num_levels = len(level_colors) - 2

raw_origins = [(width // 2, 0),
               (width // 2, height),
               (0, height // 2),
               (width, height // 2),
               (0, height),
               (width, height),
               (0, 0),
               (width, 0),
               ]

origins = {k: v for k, v in zip(level_colors, raw_origins)}
