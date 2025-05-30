import random
import pygame

class Warehouse:
    def __init__(self, screen, tile_size, pickup_point, dropoff_point, rows, cols):
        self.screen = screen
        self.tile_size = tile_size
        self.pickup_point = pickup_point
        self.dropoff_point = dropoff_point
        self.rows = rows
        self.cols = cols
        self.shelves = []
        self.reserved_items = {}  # NEW: Track reservations
        self.rest_places = []
        self.items = {}  # Dict (shelf pos -> True/False)
        self.items_delivered = 0

        self.pickup_queue = []

    def place_initial_items(self, num_items):
        available_shelves = self.shelves.copy()
        random.shuffle(available_shelves)
        for shelf in available_shelves[:num_items]:
            self.items[shelf] = True

    def add_pickup_item(self):
        self.pickup_queue.append(1)

    def pickup_item_done(self):
        if self.pickup_queue:
            self.pickup_queue.pop()

    def count_live_items(self):
        return sum(1 for val in self.items.values() if val)

    def draw(self, robots):
        for i in range(self.rows):
            for j in range(self.cols):
                rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

        for shelf in self.shelves:
            rect = pygame.Rect(shelf[1] * self.tile_size, shelf[0] * self.tile_size, self.tile_size, self.tile_size)
            color = (150, 50, 50) if self.items.get(shelf, False) else (50, 50, 150)
            pygame.draw.rect(self.screen, color, rect)

        pygame.draw.rect(self.screen, (0, 255, 0), (self.pickup_point[1] * self.tile_size, self.pickup_point[0] * self.tile_size, self.tile_size, self.tile_size))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.dropoff_point[1] * self.tile_size, self.dropoff_point[0] * self.tile_size, self.tile_size, self.tile_size))

        for place in self.rest_places:
            pygame.draw.rect(self.screen, (150, 255, 150), (place[1] * self.tile_size, place[0] * self.tile_size, self.tile_size, self.tile_size))

        for robot in robots:
            pygame.draw.circle(self.screen, robot.color, (robot.y * self.tile_size + self.tile_size // 2, robot.x * self.tile_size + self.tile_size // 2), self.tile_size // 3)

    def get_neighbors(self, pos, robot_phase=None):
        x, y = pos
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                next_pos = (nx, ny)

                # BLOCK shelf to shelf move
                if pos in self.shelves and next_pos in self.shelves:
                    continue

                # BLOCK entering shelf unless allowed
                if next_pos in self.shelves:
                    if robot_phase not in ['store_in_shelf', 'pickup_from_shelf', 'going_to_rest', 'charging',
                                           'resting']:
                        continue  # normal robots can't go into shelf unless allowed

                neighbors.append(next_pos)
        return neighbors

    def is_occupied(self, pos, robots):
        for robot in robots:
            if (robot.x, robot.y) == pos:
                return True
        return False

    def find_empty_shelf(self):
        empty_shelves = [s for s in self.shelves if not self.items.get(s, False)]
        if empty_shelves:
            return random.choice(empty_shelves)
        return None

    def find_filled_shelf(self):
        filled_shelves = [s for s in self.shelves if self.items.get(s, False) and s not in self.reserved_items]
        if filled_shelves:
            return random.choice(filled_shelves)
        return None

    def store_item(self, pos):
        self.items[pos] = True

    def remove_item(self, pos):
        if pos in self.items:
            self.items[pos] = False
            self.unreserve_item(pos)

    def pickup_items_count(self):
        return len(self.pickup_queue)

    def live_items_in_shelves(self):
        return sum(1 for shelf in self.shelves if self.items.get(shelf, False))

    def reserve_item(self, pos, robot_id):
        self.reserved_items[pos] = robot_id

    def unreserve_item(self, pos):
        if pos in self.reserved_items:
            del self.reserved_items[pos]