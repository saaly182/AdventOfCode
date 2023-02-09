"""
Helper utils/data for various direction-related tasks.
"""

unitvecs = ((-1, 0), (1, 0), (0, 1), (0, -1))

dirvecs = {
    'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1),
    'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1),
    '^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1),
}

# row, col neighbors
neighbors = (
    (-1,  0),  # n
    (-1,  1),  # ne
    ( 0,  1),  # e
    ( 1,  1),  # se
    ( 1,  0),  # s
    ( 1, -1),  # sw
    ( 0, -1),  # w
    (-1, -1),  # nw
)
