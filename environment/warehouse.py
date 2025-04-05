import pygame

class Warehouse:
    def __init__(self, screen, tile_size, pickup_point, dropoff_point, rows=15, cols=15):
        self.screen = screen
        self.tile_size = tile_size
        self.pickup_point = pickup_point
        self.dropoff_point = dropoff_point
        self.rows = rows
        self.cols = cols

        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)
        self.DARK_GRAY = (100, 100, 100)

        self.shelves = []  # shelves will be assigned later dynamically

    def draw(self, robots):
        for i in range(self.rows):
            for j in range(self.cols):
                rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, self.WHITE, rect)
                pygame.draw.rect(self.screen, self.GRAY, rect, 1)

        # Draw shelves
        for (i, j) in self.shelves:
            rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
            pygame.draw.rect(self.screen, self.DARK_GRAY, rect)

        # Draw pickup
        pi, pj = self.pickup_point
        pickup_rect = pygame.Rect(pj * self.tile_size, pi * self.tile_size, self.tile_size, self.tile_size)
        pygame.draw.rect(self.screen, self.CYAN, pickup_rect)

        # Draw dropoff
        di, dj = self.dropoff_point
        dropoff_rect = pygame.Rect(dj * self.tile_size, di * self.tile_size, self.tile_size, self.tile_size)
        pygame.draw.rect(self.screen, self.MAGENTA, dropoff_rect)

        # Draw robots
        for robot in robots:
            pygame.draw.circle(self.screen, robot.color, (robot.y * self.tile_size + self.tile_size // 2,
                                                           robot.x * self.tile_size + self.tile_size // 2), self.tile_size // 3)
