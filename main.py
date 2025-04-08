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


# --- Helper Functions ---
def load_layout(file_path):
    shelves, rest_places = [], []
    pickup, dropoff = None, None
    with open(file_path, 'r') as f:
        for i, line in enumerate(f.readlines()):
            for j, cell in enumerate(line.strip().split()):
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
    return show_option_menu(screen, clock, "Warehouse Project", ["Press 1 for Layout 1", "Press 2 for Layout 2"],
                            [1, 2])


def choose_search_method(screen, clock):
    return show_option_menu(screen, clock, "Choose Search Method",
                            ["Press 1 for BFS", "Press 2 for Greedy", "Press 3 for A*"], ['bfs', 'greedy', 'astar'])


def choose_running_mode(screen, clock):
    return show_option_menu(screen, clock, "Choose Running Mode", [
        "Press 1 for 30+30 Items (No Rest)",
        "Press 2 for 60 Items (With Rest)",
        "Press 3 for Unlimited Items (With Rest)"
    ], [1, 2, 3])


def show_option_menu(screen, clock, title_text, options, values):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)
    running, result = True, None
    while running:
        screen.fill((255, 255, 255))
        title = font.render(title_text, True, (0, 0, 0))
        screen.blit(title, (100, 50))
        for idx, opt in enumerate(options):
            option = small_font.render(opt, True, (0, 0, 0))
            screen.blit(option, (140, 150 + idx * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_3:
                    result = values[event.key - pygame.K_1]
                    running = False

        pygame.display.flip()
        clock.tick(60)
    return result


def show_restart_menu(screen, clock, frame_count, fps, warehouse, robots):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 30)  # smaller to fit results

    waiting = True
    while waiting:
        screen.fill((255, 255, 255))

        # Title
        screen.blit(font.render("Simulation Completed!", True, (0, 0, 0)), (cols * tile_size + 10, 50))

        # Summary Results
        result_texts = [
            f"Total Steps: {frame_count}",
            f"Total Real Time: {frame_count / fps:.2f} sec",
            f"Total Items Delivered: {warehouse.items_delivered}"
        ]
        y_offset = 120
        for line in result_texts:
            screen.blit(small_font.render(line, True, (0, 0, 0)), (cols * tile_size + 10, y_offset))
            y_offset += 35

        # Robot-specific Results
        for idx, robot in enumerate(robots):
            robot_info = f"Robot {idx + 1} - Pickups: {robot.pickup_count}, Deliveries: {robot.shelf_delivery_count}"
            screen.blit(small_font.render(robot_info, True, (0, 0, 0)), (cols * tile_size + 10, y_offset))
            y_offset += 30

        # Restart/Quit instructions
        screen.blit(font.render("Press R to Re-run", True, (0, 0, 0)), (cols * tile_size + 10, y_offset + 40))
        screen.blit(font.render("Press Q to Quit", True, (0, 0, 0)), (cols * tile_size + 10, y_offset + 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

        pygame.display.flip()
        clock.tick(60)



# --- Main Simulation ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((cols * tile_size + info_panel_width + 70, rows * tile_size))
    pygame.display.set_caption("Warehouse Project 15x15")
    clock = pygame.time.Clock()

    while True:
        # Menu setup
        layout_choice = show_menu(screen, clock)
        search_method = choose_search_method(screen, clock)
        running_mode = choose_running_mode(screen, clock)

        shelves, pickup_point, dropoff_point, rest_places = load_layout(
            os.path.join("layouts", f"layout{layout_choice}.txt"))
        warehouse = Warehouse(screen, tile_size, pickup_point, dropoff_point, rows, cols)
        warehouse.shelves = shelves
        warehouse.rest_places = rest_places

        if running_mode == 1:
            warehouse.place_initial_items(30)
        elif running_mode == 2:
            warehouse.place_initial_items(len(warehouse.shelves))
        else:
            warehouse.place_initial_items(0)

        robots = []
        for i, color in enumerate([(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]):
            start_pos = rest_places[i] if i < len(rest_places) else (0, 0)
            robots.append(RobotAgent(start_pos, color, pickup_point, dropoff_point, method=search_method,
                                     running_mode=running_mode))

        font = pygame.font.SysFont(None, 30)
        frame_count, stop_pressed = 0, False
        simulation_done = False
        finish_timer_started = False
        finish_timer_start_time = None

        while not simulation_done:
            clock.tick(fps)
            frame_count += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if running_mode == 3 and event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(cols * tile_size + 350, 20, 100, 40).collidepoint(event.pos):
                        stop_pressed = True

            screen.fill((255, 255, 255))

            # Robot movement
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

            # Info panel
            pygame.draw.rect(screen, (255, 255, 255), (cols * tile_size, 0, info_panel_width + 70, rows * tile_size))
            info = [
                (f"Steps: {frame_count}", 20),
                (f"Real Time: {frame_count / fps:.2f} sec", 60),
                (f"Items Delivered: {warehouse.items_delivered}", 100),
                (f"Pickup Point Items Waiting: {len(warehouse.pickup_queue)}", 140),
                (f"Live Items in Shelves: {warehouse.count_live_items()}", 180)
            ]
            for txt, y in info:
                screen.blit(font.render(txt, True, (0, 0, 0)), (cols * tile_size + 10, y))

            # --- Draw loading bar at TOP of right panel if finish timer started ---
            if finish_timer_started:
                elapsed = time.time() - finish_timer_start_time
                progress = min(elapsed / 5, 1)

                # Position for top-right loading bar
                bar_x = cols * tile_size + 10
                bar_y = 10
                total_bar_width = info_panel_width - 150  # Make bar shorter to leave space for text
                bar_width = int(total_bar_width * progress)
                bar_height = 10

                # Draw background gray bar
                pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, total_bar_width, bar_height))
                # Draw green progress bar
                pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width, bar_height))

                # Draw countdown text to the right of the bar
                remaining_time = max(0, 5 - elapsed)
                countdown_text = f"Ending in {remaining_time:.1f} sec"
                countdown_surface = font.render(countdown_text, True, (255, 0, 0))

                # Draw text right after the bar
                text_x = bar_x + total_bar_width + 10  # Little gap
                text_y = bar_y - 5  # Align nicely vertically

                screen.blit(countdown_surface, (text_x, text_y))

            y_offset = 230
            for idx, robot in enumerate(robots):
                screen.blit(font.render(f"Robot {idx + 1}: {robot.status_text}", True, (0, 0, 0)),
                            (cols * tile_size + 10, y_offset))
                y_offset += 30
                screen.blit(font.render(f"- Pickup to Shelf: {robot.pickup_count}", True, (0, 0, 0)),
                            (cols * tile_size + 20, y_offset))
                y_offset += 30
                screen.blit(font.render(f"- Shelf to Dropoff: {robot.shelf_delivery_count}", True, (0, 0, 0)),
                            (cols * tile_size + 20, y_offset))
                y_offset += 40

            if running_mode == 3:
                pygame.draw.rect(screen, (255, 0, 0), (cols * tile_size + 350, 20, 100, 40))
                screen.blit(font.render("STOP", True, (255, 255, 255)), (cols * tile_size + 375, 25))

            pygame.display.flip()

            # --- Simulation Finish Check ---
            if running_mode == 1 or running_mode == 2:
                if not finish_timer_started:
                    all_standby = all(r.phase == 'standby' for r in robots)
                    no_more_work = warehouse.pickup_items_count() == 0 and warehouse.live_items_in_shelves() == 0

                    if all_standby and no_more_work:
                        finish_timer_started = True
                        finish_timer_start_time = time.time()
                        print(f"[{frame_count / fps:.1f}s] Finish Timer: STARTED")

                if finish_timer_started and (time.time() - finish_timer_start_time >= 5):
                    simulation_done = True

            elif running_mode == 3:
                if stop_pressed:
                    simulation_done = True

            if simulation_done:
                show_restart_menu(screen, clock, frame_count, fps, warehouse, robots)


if __name__ == "__main__":
    main()
