from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Set, Tuple


Position = Tuple[int, int]

'''
This file defines the grid-based maze environment used in the project.
It provides the basic representation of the maze, including walls, the
start state, the goal state, and valid movements between cells.
'''

@dataclass(frozen=True)
class GridWorld:
    """
    a grid based in a maze environment.
    """

    rows: int
    cols: int
    start: Position
    goal: Position
    walls: Set[Position]

    def in_bounds(self, pos: Position) -> bool:
        """chekc if the position is within the maze"""
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, pos: Position) -> bool:
        """check whether a position is not blocked"""
        return pos not in self.walls

    def neighbors(self, pos: Position) -> List[Position]:
        """
        return all valid neighboring positions for a given cell.
        movement is restricted to the four directions. neighbor is valid only if
        it is inside the gird and not blocked
        """
        r, c = pos
        candidates = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]
        return [p for p in candidates if self.in_bounds(p) and self.passable(p)]

    def validate(self) -> None:
        """
        Validate that the maze configuration is legal.
        """
        if not self.in_bounds(self.start):
            raise ValueError("Start position is out of bounds.")
        if not self.in_bounds(self.goal):
            raise ValueError("Goal position is out of bounds.")
        if self.start in self.walls:
            raise ValueError("Start position cannot be a wall.")
        if self.goal in self.walls:
            raise ValueError("Goal position cannot be a wall.")

    @classmethod
    def from_text(cls, lines: Iterable[str]) -> "GridWorld":
        """
        Build a GridWorld instance from a text-based maze description.

        The maze uses the following symbols:
        S: start
        G: goal
        #: wall
        .: free cell

        Args:
            lines: An iterable of strings representing the maze rows.

        Returns:
            A validated GridWorld object.

        Raises:
            ValueError: If the maze is empty, malformed, contains unsupported
            symbols, or does not contain both a start and a goal.
        """
        grid = [list(line.strip()) for line in lines if line.strip()]
        if not grid:
            raise ValueError("Maze text cannot be empty.")

        rows = len(grid)
        cols = len(grid[0])
        for row in grid:
            if len(row) != cols:
                raise ValueError("All maze rows must have the same length.")

        start = None
        goal = None
        walls: Set[Position] = set()

        for r in range(rows):
            for c in range(cols):
                cell = grid[r][c]
                if cell == "S":
                    start = (r, c)
                elif cell == "G":
                    goal = (r, c)
                elif cell == "#":
                    walls.add((r, c))
                elif cell == ".":
                    pass
                else:
                    raise ValueError(
                        f"Unsupported maze symbol '{cell}'. Use S, G, #, or ."
                    )

        if start is None or goal is None:
            raise ValueError("Maze must contain both one start cell 'S' and one goal cell 'G'.")

        world = cls(rows=rows, cols=cols, start=start, goal=goal, walls=walls)
        world.validate()
        return world

    def render(self, path: List[Position] | None = None) -> str:
        """
        Return a string representation of the maze.
        """
        path = path or []
        path_set = set(path)
        output: List[str] = []
        for r in range(self.rows):
            row_chars: List[str] = []
            for c in range(self.cols):
                pos = (r, c)
                if pos == self.start:
                    row_chars.append("S")
                elif pos == self.goal:
                    row_chars.append("G")
                elif pos in self.walls:
                    row_chars.append("#")
                elif pos in path_set:
                    row_chars.append("*")
                else:
                    row_chars.append(".")
            output.append("".join(row_chars))
        return "\n".join(output)
