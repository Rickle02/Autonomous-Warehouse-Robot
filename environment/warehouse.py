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
        self.rest_places = []
        self.packages_to_deliver = 4  # 4 items to deliver initially

    def draw(self, robots):
        for i in range(self.rows):
            for j in range(self.cols):
                rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
                if (i, j) in self.shelves:
                    pygame.draw.rect(self.screen, (100, 100, 100), rect)  # Shelf - gray
                elif (i, j) == self.pickup_point:
                    pygame.draw.rect(self.screen, (0, 255, 255), rect)  # Pickup - cyan
                elif (i, j) == self.dropoff_point:
                    pygame.draw.rect(self.screen, (255, 0, 255), rect)  # Dropoff - magenta
                elif (i, j) in self.rest_places:
                    pygame.draw.rect(self.screen, (180, 255, 180), rect)  # Resting areas - light green
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)  # Empty floor - white

                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Draw grid

        for robot in robots:
            pygame.draw.circle(
                self.screen,
                robot.color,
                (robot.y * self.tile_size + self.tile_size // 2, robot.x * self.tile_size + self.tile_size // 2),
                self.tile_size // 3
            )

    def get_neighbors(self, pos):
        neighbors = []
        x, y = pos
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if (nx, ny) not in self.shelves:
                    neighbors.append((nx, ny))
        return neighbors

    def is_occupied(self, pos, robots):
        for robot in robots:
            if (robot.x, robot.y) == pos:
                return True
        return False
