# Autonomous Warehouse Robot

This project implements an **Autonomous Warehouse Robot** system, developed as part of the *Designing Intelligent Agents* (DIA) module. Robots operate in a 2D simulated warehouse, autonomously navigating shelves, pickup points, and dropoff zones while demonstrating reactive and learning behaviors.

---

## 🛠️ Project Structure

| Folder/File      | Description |
|:-----------------|:------------|
| `environment/`   | Contains `warehouse.py`, which defines the warehouse environment. |
| `agents/`        | Contains `robot_agent.py`, defining the behavior and logic of warehouse robots. |
| `layouts/`       | Warehouse layout files in text format (e.g., Layout 1, Layout 2). |
| `main.py`        | Main entry point to run the simulation and select warehouse layouts. |
| `README.md`      | This documentation file. |

---

## 🚀 How to Run

1. Install the required dependencies:
    ```bash
    pip install pygame
    ```

2. Run the simulation:
    ```bash
    python main.py
    ```

3. Select a warehouse layout at the menu screen (e.g., Layout 1, Layout 2).

4. Observe autonomous robots performing pickup and delivery tasks!

---

## 🌟 Features

- **Dynamic Layout Loading**: Warehouse configurations loaded from `.txt` files.
- **Autonomous Agents**:
  - Navigate around shelves, obstacles, and each other.
  - Perform pickups and deliveries intelligently.
  - Return to resting zones when idle.
- **Reactive and Reactive+State Behavior**:
  - Immediate perception-response cycle.
  - Memory of previous tasks to optimize behavior.
- **Pathfinding**:
  - Basic Breadth-First Search (BFS) algorithm for movement planning.
- **Task Management**:
  - Dynamic task assignment based on environment changes.

---

## 📚 Key Concepts Demonstrated

- **Reactive Agents**: Immediate response to environment perceptions&#8203;:contentReference[oaicite:0]{index=0}.
- **Stateful Agents**: Agents that maintain internal states for decision-making&#8203;:contentReference[oaicite:1]{index=1}.
- **Multi-Agent Coordination**: Managing multiple robots in a shared environment&#8203;:contentReference[oaicite:2]{index=2}.
- **Experimental Methods**: Extendable for running experiments (e.g., varying robot counts)&#8203;:contentReference[oaicite:3]{index=3}.

---

## 🧠 Future Work

- Introduce learning mechanisms (e.g., reinforcement learning).
- Add multiple pickup/dropoff zones and dynamic obstacles.
- Implement more efficient task coordination strategies.
- Track performance metrics (e.g., task completion time, collision rates).
