# Final Project Progress Report - Stage 1

## What I have already achieved

So far, I have completed the foundation of the project. I built the grid puzzle environment in Python, including the representation of the start state, goal state, open cells, and walls. I also implemented two search-based agents from my proposal: Breadth-First Search (BFS) and A* Search. These agents can solve the same maze environment and return a path from the start to the goal when a solution exists.

In addition, I added a basic experiment runner so I can test both algorithms on multiple maze layouts. The code currently records the main metrics that I plan to compare later in the project: whether the maze is solved, path length, number of explored nodes, and runtime. This means I now have the search baseline required before I move on to reinforcement learning.

## What are my immediate next steps?

My next step is to implement the Q-learning agent in the same grid environment. After that, I will add a training loop so the agent can learn through repeated episodes. Once the learning agent is working, I will run experiments on the same mazes used for BFS and A* and compare the results.

## Are there any challenges or adjustments?

One challenge is making sure the comparison between search and learning is fair. BFS and A* solve a maze immediately using the map, while Q-learning needs many training episodes before it can perform well. Because of this, I may need to adjust how I present the results. Instead of comparing only one runtime value, I will likely compare final path quality, training effort, and convergence behavior. This would better reflect the trade-off between planning and learning.

## What is my overall plan for the next month?

Over the next month, I plan to finish the Q-learning implementation, run experiments on several maze configurations, collect the results, and summarize the differences between the methods. My final deliverables will include the environment code, the search and learning agents, experiment results, and a short report explaining the main findings.
