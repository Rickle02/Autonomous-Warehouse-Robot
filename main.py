import pygame
import sys
import os
from environment.warehouse import Warehouse
from agents.robot_agent import RobotAgent

# Settings
tile_size = 40
rows, cols = 15, 15
info_panel_width = 200
fps = 5

# Load layout function
def load_layout(file_path):
    shelves = []
    pickup = None
    dropoff = None
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            cells = line.strip().split()
            for j, cell in enumerate(cells):
                if cell == 'S':
                    shelves.append((i, j))
                elif cell == 'P':
                    pickup = (i, j)
                elif cell == 'D':
                    dropoff = (i, j)
    return shelves, pickup, dropoff

# Show menu and get layout choice
def show_menu(screen, clock):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    running = True
    choice = None

    while running:
        screen.fill((255, 255, 255))

        title = font.render("Warehouse Project", True, (0, 0, 0))
        option1 = small_font.render("Press 1 for Layout 1", True, (0, 0, 0))
        option2 = small_font.render("Press 2 for Layout 2", True, (0, 0, 0))
        option3 = small_font.render("Press 3 for Layout 3", True, (0, 0, 0))

        screen.blit(title, (150, 50))
        screen.blit(option1, (140, 150))
        screen.blit(option2, (140, 200))
        screen.blit(option3, (140, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    choice = 1
                    running = False
                elif event.key == pygame.K_2:
                    choice = 2
                    running = False
                elif event.key == pygame.K_3:
                    choice = 3
                    running = False

        pygame.display.flip()
        clock.tick(60)

    return choice

def main():
    pygame.init()
    window_width = cols * tile_size + info_panel_width
    window_height = rows * tile_size
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Warehouse Project 15x15")
    clock = pygame.time.Clock()

    # Show menu first
    choice = show_menu(screen, clock)
    layout_file = os.path.join("layouts", f"layout{choice}.txt")
    shelves, pickup_point, dropoff_point = load_layout(layout_file)

    warehouse = Warehouse(screen, tile_size, pickup_point, dropoff_point, rows, cols)
    warehouse.shelves = shelves

    robots = [
        RobotAgent(0, 0, (255, 0, 0), pickup_point, dropoff_point),
        RobotAgent(0, 14, (0, 0, 255), pickup_point, dropoff_point),
        RobotAgent(14, 0, (0, 255, 0), pickup_point, dropoff_point),
        RobotAgent(14, 14, (255, 255, 0), pickup_point, dropoff_point),
    ]

    frame_count = 0
    running = True

    while running:
        clock.tick(fps)

        all_done = all(robot.phase == 'done' for robot in robots)
        if not all_done:
            frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        for robot in robots:
            robot.move_one_step(warehouse)

        warehouse.draw(robots)

        # Draw information panel
        pygame.draw.rect(screen, (255, 255, 255), (cols * tile_size, 0, info_panel_width, rows * tile_size))
        font = pygame.font.SysFont(None, 30)
        steps_text = font.render(f"Steps: {frame_count}", True, (0, 0, 0))
        real_time_text = font.render(f"Real Time: {frame_count / fps:.2f} sec", True, (0, 0, 0))
        items_delivered_text = font.render(f"Items Delivered: {sum(r.phase == 'done' for r in robots)}", True, (0, 0, 0))

        screen.blit(steps_text, (cols * tile_size + 10, 20))
        screen.blit(real_time_text, (cols * tile_size + 10, 60))
        screen.blit(items_delivered_text, (cols * tile_size + 10, 100))

        if all_done:
            done_text = font.render("Simulation Completed!", True, (0, 150, 0))
            screen.blit(done_text, (cols * tile_size + 10, 140))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
