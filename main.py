from environment.warehouse import Warehouse
from agents.robot_agent import RobotAgent
import time

def main():
    # Define the warehouse grid
    grid = [
        ['S', 'S', 'S', '_', '_', '_', 'P', '_', '_', '_'],
        ['S', 'S', 'S', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', 'S', 'S', 'S', '_', '_', '_'],
        ['_', '_', '_', '_', 'S', 'S', 'S', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
    ]

    # Create the warehouse environment
    warehouse = Warehouse(grid)

    # Create a robot agent
    robot1 = RobotAgent(name='Robot1', start_pos=(4, 0))  # Start at bottom left

    # Add the robot to the warehouse
    warehouse.add_robot(robot1)

    # Target goal (pickup point 'P') is at (0, 6)
    goal = (0, 6)

    print("\nMoving robot...")
    # Move step by step towards goal
    while robot1.position != goal:
        robot1.move_towards(goal, warehouse)
        warehouse.display()
        time.sleep(0.5)  # Optional: slow down to see movement

if __name__ == "__main__":
    main()
