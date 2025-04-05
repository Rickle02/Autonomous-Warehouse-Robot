import pygame
import sys
from agents.robot_agent import RobotAgent
from environment.warehouse import Warehouse

def main():
    pygame.init()
    pygame.font.init()

    # Settings
    tile_size = 40
    cols, rows = 15, 15
    info_panel_width = 200
    width, height = cols * tile_size, rows * tile_size
    FPS = 5

    screen = pygame.display.set_mode((width + info_panel_width, height))
    pygame.display.set_caption("Warehouse Project 15x15")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)

    pickup_point = (2, 1)
    dropoff_point = (14, 13)

    warehouse = Warehouse(screen, tile_size, pickup_point, dropoff_point, rows, cols)

    # Create robots
    robots = [
        RobotAgent(0, 0, (255, 0, 0), pickup_point, dropoff_point),
        RobotAgent(0, 14, (0, 0, 255), pickup_point, dropoff_point),
        RobotAgent(14, 0, (0, 255, 0), pickup_point, dropoff_point),
        RobotAgent(14, 14, (255, 255, 0), pickup_point, dropoff_point)
    ]

    # New tracking variables
    frame_count = 0
    items_delivered = 0

    # Game loop
    running = True
    while running:
        clock.tick(FPS)
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_done = True
        for robot in robots:
            if robot.phase != 'done':
                robot.move_one_step(warehouse)
                all_done = False
            elif robot.phase == 'done' and robot.carrying:
                items_delivered += 1
                robot.carrying = False

        warehouse.draw(robots)

        # Draw live counters
        info_text = [
            f"Steps: {frame_count}",
            f"Real Time: {frame_count / 5:.2f} sec",
            f"Items Delivered: {len([r for r in robots if r.phase == 'done'])}"
        ]

        y_offset = 5
        for text in info_text:
            img = font.render(text, True, (0, 0, 0))
            screen.blit(img, (width + 10, y_offset))  # >>> Shift text into margin area
            y_offset += 25

        pygame.display.flip()

        # End condition
        if all_done:
            running = False

    # Final report
    print(f"Simulation completed!")
    print(f"Total time steps (frames): {frame_count}")
    print(f"Approximate real time (seconds): {frame_count / 5:.2f} seconds")
    print(f"Total items transported: {len([r for r in robots if r.phase == 'done'])}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()