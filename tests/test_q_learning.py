from src.mazes import SIMPLE_MAZE
from src.q_learning import QLearningAgent


def test_q_learning_updates_q_table() -> None:
    """
    After training, the Q-table should contain learned state-action values.
    """
    agent = QLearningAgent(
        alpha=0.1,
        gamma=0.9,
        epsilon=0.2,
        epsilon_decay=0.995,
        min_epsilon=0.05,
        seed=42,
    )

    agent.train(
        world=SIMPLE_MAZE,
        episodes=500,
        max_steps_per_episode=100,
    )

    assert len(agent.q_table) > 0


def test_q_learning_finds_path_in_simple_maze() -> None:
    """
    After training on the simple maze, the agent should be able to
    extract a valid path to the goal.
    """
    agent = QLearningAgent(
        alpha=0.1,
        gamma=0.9,
        epsilon=0.2,
        epsilon_decay=0.995,
        min_epsilon=0.05,
        seed=42,
    )

    agent.train(
        world=SIMPLE_MAZE,
        episodes=3000,
        max_steps_per_episode=100,
    )
    path = agent.extract_path(SIMPLE_MAZE, max_steps=100)

    assert len(path) > 0
    assert path[-1] == SIMPLE_MAZE.goal


def test_q_learning_path_starts_and_ends_correctly() -> None:
    """
    The extracted path should begin at the maze start and end at the goal.
    """
    agent = QLearningAgent(
        alpha=0.1,
        gamma=0.9,
        epsilon=0.2,
        epsilon_decay=0.995,
        min_epsilon=0.05,
        seed=42,
    )

    agent.train(
        world=SIMPLE_MAZE,
        episodes=3000,
        max_steps_per_episode=100,
    )
    path = agent.extract_path(SIMPLE_MAZE, max_steps=100)

    assert len(path) > 0
    assert path[0] == SIMPLE_MAZE.start
    assert path[-1] == SIMPLE_MAZE.goal