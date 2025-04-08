# [FINAL PATCHED main.py with Re-run menu] ✅

import pygame
import sys
import os
import random
import time
from environment.warehouse import Warehouse
from agents.robot_agent import RobotAgent

# Settings
tile_size = 40
rows, cols = 15, 15
info_panel_width = 500
fps = 10

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

def choose_search_method(screen, clock):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    running = True
    method = None

    while running:
        screen.fill((255, 255, 255))
        title = font.render("Choose Search Method", True, (0, 0, 0))
        option1 = small_font.render("Press 1 for BFS", True, (0, 0, 0))
        option2 = small_font.render("Press 2 for Greedy", True, (0, 0, 0))
        option3 = small_font.render("Press 3 for A*", True, (0, 0, 0))

        screen.blit(title, (100, 50))
        screen.blit(option1, (140, 150))
        screen.blit(option2, (140, 200))
        screen.blit(option3, (140, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    method = 'bfs'
                    running = False
                elif event.key == pygame.K_2:
                    method = 'greedy'
                    running = False
                elif event.key == pygame.K_3:
                    method = 'astar'
                    running = False

        pygame.display.flip()
        clock.tick(60)

    return method

def choose_running_mode(screen, clock):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    running = True
    mode = None

    while running:
        screen.fill((255, 255, 255))
        title = font.render("Choose Running Mode", True, (0, 0, 0))
        option1 = small_font.render("Press 1 for picking up 30 Items, and 30 Items already in Shelves", True, (0, 0, 0))
        option2 = small_font.render("Press 2 for picking up 60 Items (Having Rest)", True, (0, 0, 0))
        option3 = small_font.render("Press 3 for Unlimited Items (Having Rest)", True, (0, 0, 0))

        screen.blit(title, (100, 50))
        screen.blit(option1, (140, 150))
        screen.blit(option2, (140, 200))
        screen.blit(option3, (140, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = 1
                    running = False
                elif event.key == pygame.K_2:
                    mode = 2
                    running = False
                elif event.key == pygame.K_3:
                    mode = 3
                    running = False

        pygame.display.flip()
        clock.tick(60)

    return mode

def main():
    pygame.init()
    window_width = cols * tile_size + info_panel_width + 70
    window_height = rows * tile_size
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Warehouse Project 15x15")
    clock = pygame.time.Clock()

    while True:
        choice = show_menu(screen, clock)
        layout_file = os.path.join("layouts", f"layout{choice}.txt")
        shelves, pickup_point, dropoff_point, rest_places = load_layout(layout_file)
        search_method = choose_search_method(screen, clock)
        running_mode = choose_running_mode(screen, clock)

        warehouse = Warehouse(screen, tile_size, pickup_point, dropoff_point, rows, cols)
        warehouse.shelves = shelves
        warehouse.rest_places = rest_places

        if running_mode == 1:
            warehouse.place_initial_items(30)
        else:
            warehouse.place_initial_items(0)

        robots = []
        colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

        for i in range(4):
            start_pos = rest_places[i] if i < len(rest_places) else (0, 0)
            robot = RobotAgent(start_pos, colors[i], pickup_point, dropoff_point, method=search_method)
            robot.status_text = "Idle"
            robots.append(robot)

        frame_count = 0
        stop_pressed = False
        font = pygame.font.SysFont(None, 30)

        simulation_done = False

        while not simulation_done:
            clock.tick(fps)
            frame_count += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if running_mode == 3 and event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(window_width - 150, 20, 100, 40).collidepoint(event.pos):
                        stop_pressed = True

            screen.fill((255, 255, 255))
            robots_sorted = sorted(robots, key=lambda r: (r.x, r.y))
            planned_moves = {}
            occupied_positions = {(r.x, r.y) for r in robots}

            for robot in robots_sorted:
                if robot.phase != 'done':
                    current_pos = (robot.x, robot.y)
                    next_pos = robot.get_action(current_pos, warehouse, robots)
                    if next_pos not in occupied_positions:
                        planned_moves[robot] = next_pos
                        occupied_positions.add(next_pos)
                    else:
                        planned_moves[robot] = current_pos

            for robot in robots_sorted:
                next_pos = planned_moves.get(robot, (robot.x, robot.y))
                robot.x, robot.y = next_pos

            for robot in robots:
                robot.update_phase(warehouse, robots)

            warehouse.draw(robots)

            pygame.draw.rect(screen, (255, 255, 255), (cols * tile_size, 0, info_panel_width + 70, rows * tile_size))

            steps_text = font.render(f"Steps: {frame_count}", True, (0, 0, 0))
            real_time_text = font.render(f"Real Time: {frame_count / fps:.2f} sec", True, (0, 0, 0))
            items_delivered_text = font.render(f"Items Delivered: {warehouse.items_delivered}", True, (0, 0, 0))

            screen.blit(steps_text, (cols * tile_size + 10, 20))
            screen.blit(real_time_text, (cols * tile_size + 10, 60))
            screen.blit(items_delivered_text, (cols * tile_size + 10, 100))

            mode_name = {1: "30 Items", 2: "60 Items + Rest", 3: "Unlimited Items"}
            mode_text = font.render(f"Mode: {mode_name[running_mode]}", True, (0, 0, 0))
            screen.blit(mode_text, (cols * tile_size + 10, 140))

            if running_mode == 3:
                pygame.draw.rect(screen, (255, 0, 0), (window_width - 150, 20, 100, 40))
                stop_text = font.render("STOP", True, (255, 255, 255))
                screen.blit(stop_text, (window_width - 125, 25))

            y_offset = 190
            for idx, robot in enumerate(robots):
                status = font.render(f"Robot {idx+1}: {robot.status_text}", True, (0, 0, 0))
                screen.blit(status, (cols * tile_size + 10, y_offset))
                y_offset += 40

            pygame.display.flip()

            if (running_mode == 1 and warehouse.items_delivered >= 60) or (running_mode == 2 and warehouse.items_delivered >= 60) or (running_mode == 3 and stop_pressed):
                simulation_done = True

        show_restart_menu(screen, clock)

def show_restart_menu(screen, clock):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    waiting = True

    while waiting:
        screen.fill((255, 255, 255))
        message = font.render("Simulation Finished!", True, (0, 0, 0))
        option1 = small_font.render("Press R to Re-run", True, (0, 0, 0))
        option2 = small_font.render("Press Q to Quit", True, (0, 0, 0))

        screen.blit(message, (cols * tile_size + 10, 200))
        screen.blit(option1, (cols * tile_size + 10, 300))
        screen.blit(option2, (cols * tile_size + 10, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # re-run
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
