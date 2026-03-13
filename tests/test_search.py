import unittest

from src.environment import GridWorld
from src.search_agents import a_star_search, bfs_search


class SearchAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.maze = GridWorld.from_text(
            [
                "S...",
                ".##.",
                "...G",
            ]
        )

    def test_bfs_solves_maze(self) -> None:
        result = bfs_search(self.maze)
        self.assertTrue(result.solved)
        self.assertEqual(result.path[0], self.maze.start)
        self.assertEqual(result.path[-1], self.maze.goal)

    def test_a_star_solves_maze(self) -> None:
        result = a_star_search(self.maze)
        self.assertTrue(result.solved)
        self.assertEqual(result.path[0], self.maze.start)
        self.assertEqual(result.path[-1], self.maze.goal)

    def test_bfs_and_a_star_same_path_length(self) -> None:
        bfs_result = bfs_search(self.maze)
        a_star_result = a_star_search(self.maze)
        self.assertEqual(bfs_result.path_length, a_star_result.path_length)


if __name__ == "__main__":
    unittest.main()
