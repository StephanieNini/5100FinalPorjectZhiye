from .environment import GridWorld

SIMPLE_MAZE = GridWorld.from_text(
    [
        "S....",
        ".###.",
        "...#.",
        ".#...",
        "...#G",
    ]
)

MEDIUM_MAZE = GridWorld.from_text(
    [
        "S...#...",
        ".##.#.#.",
        ".#....#.",
        ".####.#.",
        ".#....#.",
        ".#.####.",
        "...#...G",
    ]
)

HARD_MAZE = GridWorld.from_text(
    [
        "S..#......",
        ".#.###.##.",
        ".#.....#..",
        ".#####.#.#",
        ".....#.#.#",
        ".###.#.#.#",
        ".#...#...#",
        ".#.#####.#",
        ".#.......G",
    ]
)

ALL_MAZES = {
    "simple": SIMPLE_MAZE,
    "medium": MEDIUM_MAZE,
    "hard": HARD_MAZE,
}
