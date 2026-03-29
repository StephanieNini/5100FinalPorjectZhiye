from .mazes import ALL_MAZES
from .q_learning import QLearningAgent
from .search_agents import a_star_search, bfs_search


def print_result(maze, result) -> None:
    """
    Print a standard summary for one algorithm result.
    """
    print(f"\nAlgorithm: {result.algorithm}")
    print(f"Solved: {result.solved}")
    print(f"Path length: {result.path_length}")
    print(f"Explored nodes: {result.explored_nodes}")
    print(f"Runtime (ms): {result.runtime_ms:.3f}")

    if result.solved:
        print("Path visualization:")
        print(maze.render(result.path))


def run_demo() -> None:
    for maze_name, maze in ALL_MAZES.items():
        print(f"\n=== Maze: {maze_name} ===")
        print("Original maze:")
        print(maze.render())

        # Run baseline search algorithms
        for solver in (bfs_search, a_star_search):
            result = solver(maze)
            print_result(maze, result)

        # Run Q-learning
        agent = QLearningAgent(
            alpha=0.1,
            gamma=0.9,
            epsilon=0.2,
            epsilon_decay=0.995,
            min_epsilon=0.05,
            seed=42,
        )
        q_result, q_stats = agent.solve(
            world=maze,
            episodes=2000,
            max_steps_per_episode=200,
            extract_max_steps=200,
        )

        print_result(maze, q_result)
        print(f"Training episodes: {q_stats.episodes}")
        print(f"Final epsilon: {agent.epsilon:.4f}")
        print(f"Last episode reward: {q_stats.training_rewards[-1]:.2f}")
        print(f"Last episode steps: {q_stats.training_steps[-1]}")


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()