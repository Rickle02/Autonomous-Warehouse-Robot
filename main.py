import pygame
from environment.warehouse import Warehouse
from agents.robot_agent import RobotAgent
import sys
import os

# Settings
tile_size = 40
rows, cols = 15, 15
info_panel_width = 200
fps = 5

SEARCH_METHOD = 'bfs'

def load_layout(file_path):
    shelves = []
    pickup = None
    dropoff = None
    rest_places = []

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
                elif cell == 'E':
                    rest_places.append((i, j))

    return shelves, pickup, dropoff, rest_places

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

        screen.blit(title, (150, 50))
        screen.blit(option1, (140, 150))
        screen.blit(option2, (140, 200))

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

    choice = show_menu(screen, clock)
    layout_file = os.path.join("layouts", f"layout{choice}.txt")
    shelves, pickup_point, dropoff_point, rest_places = load_layout(layout_file)

    warehouse = Warehouse(screen, tile_size, pickup_point, dropoff_point, rows, cols)
    warehouse.shelves = shelves
    warehouse.rest_places = rest_places

    robots = []
    robot_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

    for i in range(len(robot_colors)):
        if i < len(rest_places):
            robots.append(RobotAgent(rest_places[i], robot_colors[i], pickup_point, dropoff_point, method=SEARCH_METHOD))

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

        robots_sorted = sorted(robots, key=lambda r: (r.x, r.y))
        planned_moves = {}
        reserved_tiles = {(r.x, r.y) for r in robots}

        for robot in robots_sorted:
            if robot.phase != 'done':
                current_pos = (robot.x, robot.y)
                next_pos = robot.get_action(current_pos, warehouse, robots)
                if next_pos not in reserved_tiles:
                    planned_moves[robot] = next_pos
                    reserved_tiles.add(next_pos)
                else:
                    planned_moves[robot] = current_pos

        for robot in robots_sorted:
            next_pos = planned_moves.get(robot, (robot.x, robot.y))
            robot.x, robot.y = next_pos

        for robot in robots:
            robot.update_phase(warehouse)

        warehouse.draw(robots)

        pygame.draw.rect(screen, (255, 255, 255), (cols * tile_size, 0, info_panel_width, rows * tile_size))
        font = pygame.font.SysFont(None, 30)
        steps_text = font.render(f"Steps: {frame_count}", True, (0, 0, 0))
        real_time_text = font.render(f"Real Time: {frame_count / fps:.2f} sec", True, (0, 0, 0))
        items_delivered_text = font.render(f"Items Delivered: {4 - warehouse.packages_to_deliver}", True, (0, 0, 0))

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
