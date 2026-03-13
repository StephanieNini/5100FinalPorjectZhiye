from .mazes import ALL_MAZES
from .search_agents import a_star_search, bfs_search


def run_demo() -> None:
    for maze_name, maze in ALL_MAZES.items():
        print(f"\n=== Maze: {maze_name} ===")
        print("Original maze:")
        print(maze.render())

        for solver in (bfs_search, a_star_search):
            result = solver(maze)
            print(f"\nAlgorithm: {result.algorithm}")
            print(f"Solved: {result.solved}")
            print(f"Path length: {result.path_length}")
            print(f"Explored nodes: {result.explored_nodes}")
            print(f"Runtime (ms): {result.runtime_ms:.3f}")
            if result.solved:
                print("Path visualization:")
                print(maze.render(result.path))


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
