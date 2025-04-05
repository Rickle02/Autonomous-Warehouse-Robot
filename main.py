from environment.warehouse import Warehouse
from agents.robot_agent import RobotAgent
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def main():
    grid = [
        ['S', 'S', '_', '_', '_', '_', '_', 'S', 'S', 'S'],
        ['S', 'S', '_', 'P', '_', '_', '_', 'S', 'S', 'S'],
        ['_', '_', '_', '_', 'S', 'S', '_', '_', '_', '_'],
        ['_', 'S', 'S', '_', 'S', 'S', '_', '_', 'S', '_'],
        ['_', '_', '_', '_', '_', '_', '_', 'S', 'S', '_'],
        ['_', 'S', 'S', '_', '_', 'S', 'S', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_', 'S', 'S'],
        ['S', 'S', '_', '_', 'S', 'S', '_', '_', '_', '_'],
        ['S', 'S', '_', '_', '_', '_', '_', 'S', 'S', 'S'],
        ['_', '_', '_', '_', '_', '_', '_', '_', 'D', '_']
    ]

    fig, ax = plt.subplots(figsize=(5, 5))
    warehouse = Warehouse(grid, ax)

    robots = [
        RobotAgent(name='1', start_pos=(0, 0)),
        RobotAgent(name='2', start_pos=(0, 9)),
        RobotAgent(name='3', start_pos=(9, 0)),
        RobotAgent(name='4', start_pos=(9, 9))
    ]

    for robot in robots:
        warehouse.add_robot(robot)

    pickup_goal = (1, 3)
    dropoff_goal = (9, 8)

    def update(frame):
        all_done = True
        for robot in robots:
            if robot.phase == "pickup":
                all_done = False
                if robot.position != pickup_goal:
                    if not warehouse.is_cell_occupied(*pickup_goal):
                        robot.move_one_step_towards(pickup_goal, warehouse)
                else:
                    robot.check_pickup(warehouse)

            elif robot.phase == "dropoff":
                all_done = False
                if robot.position != dropoff_goal:
                    if not warehouse.is_cell_occupied(*dropoff_goal):
                        robot.move_one_step_towards(dropoff_goal, warehouse)
                else:
                    robot.check_dropoff(warehouse)

        warehouse.render()

        if all_done:
            print("All robots finished their tasks!")
            # anim.event_source.stop()

    anim = FuncAnimation(fig, update, frames=300, interval=500, repeat=False)
    plt.show()

if __name__ == "__main__":
    main()
