import pygame
import sys
from agents.robot_agent import RobotAgent
from environment.warehouse import Warehouse

def main():
    pygame.init()

    # Settings
    tile_size = 40  # smaller so it fits bigger grid
    cols, rows = 15, 15
    width, height = cols * tile_size, rows * tile_size
    FPS = 5

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Warehouse Project 15x15")
    clock = pygame.time.Clock()

    pickup_point = (2, 1)   # adjust if you want
    dropoff_point = (14, 13)  # adjust if you want

    warehouse = Warehouse(screen, tile_size, pickup_point, dropoff_point, rows, cols)

    # Create robots at different starting points
    robots = [
        RobotAgent(0, 0, (255, 0, 0), pickup_point, dropoff_point),
        RobotAgent(0, 14, (0, 0, 255), pickup_point, dropoff_point),
        RobotAgent(14, 0, (0, 255, 0), pickup_point, dropoff_point),
        RobotAgent(14, 14, (255, 255, 0), pickup_point, dropoff_point)
    ]

    # Game loop
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move robots
        for robot in robots:
            if robot.phase != 'done':
                robot.move_one_step(warehouse)

        # Draw everything
        warehouse.draw(robots)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
