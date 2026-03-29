from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple


Position = Tuple[int, int]
Action = str

ACTIONS: Tuple[Action, ...] = ("up", "down", "left", "right")
ACTION_DELTAS: Dict[Action, Position] = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}


"""
environment.py

This module defines the grid-based maze environment used in the project.
It stores the maze dimensions, start state, goal state, and wall locations.

The module provides helper methods for both classical search and
reinforcement learning. Search algorithms use neighbor expansion,
while Q-learning can use action selection, state transitions, rewards,
and terminal-state checks in the same environment.
"""


@dataclass(frozen=True)
class GridWorld:
    """
    A grid-based maze environment.

    The environment stores the size of the grid, the start and goal
    positions, and the set of wall cells. It supports both search-based
    path finding and reinforcement learning interaction.
    """

    rows: int
    cols: int
    start: Position
    goal: Position
    walls: Set[Position]

    def in_bounds(self, pos: Position) -> bool:
        """
        Check whether a position lies within the grid boundaries.
        """
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def passable(self, pos: Position) -> bool:
        """
        Check whether a position is not blocked by a wall.
        """
        return pos not in self.walls

    def is_valid_state(self, pos: Position) -> bool:
        """
        Check whether a state is both inside the grid and passable.
        """
        return self.in_bounds(pos) and self.passable(pos)

    def neighbors(self, pos: Position) -> List[Position]:
        """
        Return all valid neighboring positions for a given cell.

        Movement is restricted to the four cardinal directions.
        A neighbor is valid only if it is inside the grid and not blocked
        by a wall.
        """
        r, c = pos
        candidates = [
            (r - 1, c),
            (r + 1, c),
            (r, c - 1),
            (r, c + 1),
        ]
        return [p for p in candidates if self.is_valid_state(p)]

    def get_actions(self, state: Position) -> List[Action]:
        """
        Return the available action labels.

        In this project, the action space is fixed to four directions.
        Invalid moves are handled by the transition function.
        """
        return list(ACTIONS)

    def next_position(self, state: Position, action: Action) -> Position:
        """
        Compute the next state after applying an action.

        If the action would move the agent out of bounds or into a wall,
        the agent stays in the current state.
        """
        if action not in ACTION_DELTAS:
            raise ValueError(f"Unsupported action '{action}'.")

        dr, dc = ACTION_DELTAS[action]
        candidate = (state[0] + dr, state[1] + dc)

        if self.is_valid_state(candidate):
            return candidate
        return state

    def is_terminal(self, state: Position) -> bool:
        """
        Check whether the given state is the goal state.
        """
        return state == self.goal

    def get_reward(
        self, state: Position, action: Action, next_state: Position
    ) -> float:
        """
        Return the reward for a transition.

        Reward design for phase 2:
        - reaching the goal: +10
        - invalid move that keeps the agent in place: -2
        - normal step: -1
        """
        if next_state == self.goal:
            return 10.0
        if next_state == state:
            return -2.0
        return -1.0

    def step(self, state: Position, action: Action) -> Tuple[Position, float, bool]:
        """
        Execute one environment step for reinforcement learning.

        Returns:
            next_state: the resulting state after the action
            reward: reward for the transition
            done: whether the next state is terminal
        """
        next_state = self.next_position(state, action)
        reward = self.get_reward(state, action, next_state)
        done = self.is_terminal(next_state)
        return next_state, reward, done

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
        start_count = 0
        goal_count = 0
        walls: Set[Position] = set()

        for r in range(rows):
            for c in range(cols):
                cell = grid[r][c]
                if cell == "S":
                    start = (r, c)
                    start_count += 1
                elif cell == "G":
                    goal = (r, c)
                    goal_count += 1
                elif cell == "#":
                    walls.add((r, c))
                elif cell == ".":
                    pass
                else:
                    raise ValueError(
                        f"Unsupported maze symbol '{cell}'. Use S, G, #, or ."
                    )

        if start_count != 1 or goal_count != 1:
            raise ValueError("Maze must contain exactly one S and one G.")

        world = cls(rows=rows, cols=cols, start=start, goal=goal, walls=walls)
        world.validate()
        return world

    def render(self, path: List[Position] | None = None) -> str:
        """
        Return a string representation of the maze.

        If a path is provided, cells on the path are marked with '*'
        while preserving the start and goal symbols.
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