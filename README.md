# Grid Navigation AI Project - Phase 1

This repository contains the **Phase 1 implementation** for the final project based on the proposal and literature review.

## Phase 1 scope

The goal of this stage is to complete the search-problem foundation before adding reinforcement learning.

Completed in this repo:
- Grid maze environment in Python
- Start / goal / wall support
- Breadth-First Search (BFS)
- A* Search with Manhattan-distance heuristic
- Basic experiment runner
- Metrics collection: path length, explored nodes, runtime
- Sample mazes for testing
- Stage 1 progress report draft

Not included yet:
- Q-learning agent
- Training loop and policy evaluation
- Final comparison charts/report

## Project structure

```text
src/
  environment.py      # Grid and maze model
  search_agents.py    # BFS and A*
  metrics.py          # Dataclass for experiment results
  mazes.py            # Sample maze layouts
  main.py             # Demo / experiment runner

tests/
  test_search.py      # Basic correctness tests

progress_report_stage1.md
requirements.txt
```

## How to run

### 1. Create virtual environment (optional)

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Run the demo

```bash
python -m src.main
```

### 3. Run tests

```bash
python -m unittest discover -s tests -v
```
