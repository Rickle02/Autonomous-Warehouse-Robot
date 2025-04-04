from environment.warehouse import Warehouse
from agents.robot_agent import RobotAgent

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

    # Display initial warehouse
    warehouse.display()

    print("\nMoving robot...")
    # Example moves
    robot1.move('right', warehouse)
    robot1.move('right', warehouse)
    robot1.move('up', warehouse)
    robot1.move('up', warehouse)

    # Display warehouse after movement
    warehouse.display()

if __name__ == "__main__":
    main()
