from environment.warehouse import Warehouse
from agents.robot_agent import RobotAgent
import time

def main():
    grid = [
        ['S', 'S', 'S', '_', '_', '_', 'P', '_', '_', '_'],
        ['S', 'S', 'S', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', 'S', 'S', 'S', '_', '_', '_'],
        ['_', '_', '_', '_', 'S', 'S', 'S', '_', '_', 'D'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
    ]

    warehouse = Warehouse(grid)

    robot1 = RobotAgent(name='Robot1', start_pos=(4, 0))
    robot2 = RobotAgent(name='Robot2', start_pos=(4, 9))

    warehouse.add_robot(robot1)
    warehouse.add_robot(robot2)

    pickup_goal_1 = (0, 6)
    pickup_goal_2 = (0, 6)  # SAME pickup point

    dropoff_goal_1 = (3, 9)
    dropoff_goal_2 = (3, 9)  # SAME drop-off point now too!

    warehouse.display()

    robot1_phase = "pickup"
    robot2_phase = "pickup"

    # Combined moving loop
    while robot1_phase != "done" or robot2_phase != "done":
        if robot1_phase == "pickup":
            if robot1.position != pickup_goal_1:
                if not warehouse.is_cell_occupied(*pickup_goal_1):
                    robot1.move_towards(pickup_goal_1, warehouse)
                else:
                    print(f"{robot1.name} is waiting at pickup: spot occupied.")
            else:
                robot1.check_pickup(warehouse)
                robot1_phase = "dropoff"

        elif robot1_phase == "dropoff":
            if robot1.position != dropoff_goal_1:
                if not warehouse.is_cell_occupied(*dropoff_goal_1):
                    robot1.move_towards(dropoff_goal_1, warehouse)
                else:
                    print(f"{robot1.name} is waiting at dropoff: spot occupied.")
            else:
                robot1.check_dropoff(warehouse)
                robot1_phase = "done"

        if robot2_phase == "pickup":
            if robot2.position != pickup_goal_2:
                if not warehouse.is_cell_occupied(*pickup_goal_2):
                    robot2.move_towards(pickup_goal_2, warehouse)
                else:
                    print(f"{robot2.name} is waiting at pickup: spot occupied.")
            else:
                robot2.check_pickup(warehouse)
                robot2_phase = "dropoff"

        elif robot2_phase == "dropoff":
            if robot2.position != dropoff_goal_2:
                if not warehouse.is_cell_occupied(*dropoff_goal_2):
                    robot2.move_towards(dropoff_goal_2, warehouse)
                else:
                    print(f"{robot2.name} is waiting at dropoff: spot occupied.")
            else:
                robot2.check_dropoff(warehouse)
                robot2_phase = "done"

        warehouse.display()
        time.sleep(0.5)

    print("Both tasks completed!")

if __name__ == "__main__":
    main()
