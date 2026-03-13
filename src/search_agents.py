from __future__ import annotations

import heapq
import time
from collections import deque
from typing import Dict, List, Optional, Tuple

from .environment import GridWorld, Position
from .metrics import SearchResult

"""
search_agents.py

This module implements the baseline search algorithms used in the project.

Currently, it includes:
    Breadth-First Search (BFS)
    A* search
    helper functions for path reconstruction and heuristic evaluation

These algorithms are used to solve the grid-based maze and to provide
baseline results for later comparison with reinforcement learning methods.
"""

def reconstruct_path(
    parents: Dict[Position, Optional[Position]], goal: Position
) -> List[Position]:
    """
    Reconstruct the path from the start state to the goal state.

    The parents dictionary stores the predecessor of each visited node.
    Starting from the goal, this function traces backward until reaching
    the start node, then reverses the result to produce the correct order.

    Args:
        parents: Mapping from each visited position to its parent position.
        goal: The goal position.

    Returns:
        A list of positions representing the path from start to goal.
        Returns an empty list if the goal was never reached.
    """
    if goal not in parents:
        return []

    path: List[Position] = []
    current: Optional[Position] = goal
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    return path


def manhattan(a: Position, b: Position) -> int:
    """
    Compute the Manhattan distance between two positions.

    This heuristic is appropriate for grid navigation with four-directional
    movement because it estimates the remaining path cost without
    overestimating the true shortest path.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bfs_search(world: GridWorld) -> SearchResult:
    """
    Breadth-First Search (BFS).

    BFS explores nodes level by level using a FIFO queue. In an
    unweighted grid world, BFS guarantees finding a shortest path
    from the start state to the goal state if one exists.

    Args:
        world: The grid-based maze environment.

    Returns:
        A SearchResult object containing the algorithm name, the path
        found, the number of explored nodes, and the runtime in milliseconds.
    """
    start_time = time.perf_counter()

    frontier = deque([world.start])
    parents: Dict[Position, Optional[Position]] = {world.start: None}
    explored_nodes = 0

    while frontier:
        current = frontier.popleft()
        explored_nodes += 1

        if current == world.goal:
            runtime_ms = (time.perf_counter() - start_time) * 1000
            return SearchResult(
                algorithm="BFS",
                path=reconstruct_path(parents, world.goal),
                explored_nodes=explored_nodes,
                runtime_ms=runtime_ms,
            )

        for neighbor in world.neighbors(current):
            if neighbor not in parents:
                parents[neighbor] = current
                frontier.append(neighbor)

    runtime_ms = (time.perf_counter() - start_time) * 1000
    return SearchResult(
        algorithm="BFS",
        path=[],
        explored_nodes=explored_nodes,
        runtime_ms=runtime_ms,
    )


def a_star_search(world: GridWorld) -> SearchResult:
    """
    A* search.

    A* combines the path cost from the start state with a heuristic
    estimate of the remaining distance to the goal. In this project,
    Manhattan distance is used as the heuristic because movement is
    restricted to four directions on a grid.

    Args:
        world: The grid-based maze environment.

    Returns:
        A SearchResult object containing the algorithm name, the path
        found, the number of explored nodes, and the runtime in milliseconds.
    """
    start_time = time.perf_counter()

    open_heap: List[Tuple[int, int, Position]] = []
    heapq.heappush(open_heap, (manhattan(world.start, world.goal), 0, world.start))

    parents: Dict[Position, Optional[Position]] = {world.start: None}
    g_score: Dict[Position, int] = {world.start: 0}
    explored_nodes = 0

    while open_heap:
        _, cost_so_far, current = heapq.heappop(open_heap)
        explored_nodes += 1

        if current == world.goal:
            runtime_ms = (time.perf_counter() - start_time) * 1000
            return SearchResult(
                algorithm="A*",
                path=reconstruct_path(parents, world.goal),
                explored_nodes=explored_nodes,
                runtime_ms=runtime_ms,
            )

        if cost_so_far > g_score.get(current, float("inf")):
            continue

        for neighbor in world.neighbors(current):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parents[neighbor] = current
                f_score = tentative_g + manhattan(neighbor, world.goal)
                heapq.heappush(open_heap, (f_score, tentative_g, neighbor))

    runtime_ms = (time.perf_counter() - start_time) * 1000
    return SearchResult(
        algorithm="A*",
        path=[],
        explored_nodes=explored_nodes,
        runtime_ms=runtime_ms,
    )
