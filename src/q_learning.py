from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .environment import Action, GridWorld, Position
from .metrics import SearchResult


@dataclass
class QLearningStats:
    episodes: int
    training_rewards: List[float] = field(default_factory=list)
    training_steps: List[int] = field(default_factory=list)


class QLearningAgent:
    """
    Q-learning agent for the GridWorld environment.

    The agent learns a Q-table that maps (state, action) pairs to values.
    During training, it uses epsilon-greedy exploration and updates the
    Q-values based on the Bellman equation.
    """

    def __init__(
        self,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 0.2,
        epsilon_decay: float = 0.995,
        min_epsilon: float = 0.05,
        seed: int = 42,
    ) -> None:
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.q_table: Dict[Tuple[Position, Action], float] = {}
        self.random = random.Random(seed)

    def get_q_value(self, state: Position, action: Action) -> float:
        """
        Return the Q-value for a given (state, action) pair.
        Unseen pairs default to 0.0.
        """
        return self.q_table.get((state, action), 0.0)

    def set_q_value(self, state: Position, action: Action, value: float) -> None:
        """
        Set the Q-value for a given (state, action) pair.
        """
        self.q_table[(state, action)] = value

    def best_action(self, world: GridWorld, state: Position) -> Action:
        """
        Return the action with the highest Q-value for the current state.

        Ties are broken randomly among the best actions.
        """
        actions = world.get_actions(state)
        q_values = [self.get_q_value(state, action) for action in actions]
        max_q = max(q_values)

        best_actions = [
            action
            for action, q in zip(actions, q_values)
            if q == max_q
        ]
        return self.random.choice(best_actions)

    def choose_action(self, world: GridWorld, state: Position) -> Action:
        """
        Choose an action using epsilon-greedy exploration.
        """
        actions = world.get_actions(state)

        if self.random.random() < self.epsilon:
            return self.random.choice(actions)

        return self.best_action(world, state)

    def update(
        self,
        world: GridWorld,
        state: Position,
        action: Action,
        reward: float,
        next_state: Position,
    ) -> None:
        """
        Apply the Q-learning update rule:

        Q(s, a) <- Q(s, a) + alpha * [reward + gamma * max Q(s', a') - Q(s, a)]
        """
        current_q = self.get_q_value(state, action)

        if world.is_terminal(next_state):
            target = reward
        else:
            next_actions = world.get_actions(next_state)
            max_next_q = max(self.get_q_value(next_state, a) for a in next_actions)
            target = reward + self.gamma * max_next_q

        updated_q = current_q + self.alpha * (target - current_q)
        self.set_q_value(state, action, updated_q)

    def train(
        self,
        world: GridWorld,
        episodes: int = 2000,
        max_steps_per_episode: int = 200,
    ) -> QLearningStats:
        """
        Train the agent in the given GridWorld.

        Returns training statistics including episode rewards and steps.
        """
        stats = QLearningStats(episodes=episodes)

        for _ in range(episodes):
            state = world.start
            total_reward = 0.0
            steps = 0

            for _step in range(max_steps_per_episode):
                action = self.choose_action(world, state)
                next_state, reward, done = world.step(state, action)

                self.update(world, state, action, reward, next_state)

                total_reward += reward
                steps += 1
                state = next_state

                if done:
                    break

            stats.training_rewards.append(total_reward)
            stats.training_steps.append(steps)

            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

        return stats

    def extract_path(
        self,
        world: GridWorld,
        max_steps: int = 200,
    ) -> List[Position]:
        """
        Extract a greedy path from the learned Q-table.

        Starting from the start state, always choose the best learned action.
        Stops if the goal is reached or if the path gets stuck in a loop.
        """
        state = world.start
        path = [state]
        visited = {state}

        for _ in range(max_steps):
            if world.is_terminal(state):
                return path

            action = self.best_action(world, state)
            next_state, _, _ = world.step(state, action)

            if next_state == state:
                break

            path.append(next_state)

            if next_state in visited:
                break

            visited.add(next_state)
            state = next_state

        if world.is_terminal(path[-1]):
            return path
        return []

    def solve(
        self,
        world: GridWorld,
        episodes: int = 2000,
        max_steps_per_episode: int = 200,
        extract_max_steps: int = 200,
    ) -> tuple[SearchResult, QLearningStats]:
        """
        Train the agent and return a SearchResult-like output for comparison
        with BFS and A*.
        """
        stats = self.train(
            world=world,
            episodes=episodes,
            max_steps_per_episode=max_steps_per_episode,
        )
        path = self.extract_path(world, max_steps=extract_max_steps)

        result = SearchResult(
            algorithm="Q-Learning",
            path=path,
            explored_nodes=sum(stats.training_steps),
            runtime_ms=0.0,
        )
        return result, stats