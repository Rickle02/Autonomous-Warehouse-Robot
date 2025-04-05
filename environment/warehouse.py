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

        # Create shelves layout (organized rows)
        self.shelves = []

        for row in [1,2,4,5,7,8,10,11,13]:
            for col in [2,3,4,6,7,8,10,11,12]:
                self.shelves.append((row, col))

    def draw(self, robots):
        self.screen.fill(self.WHITE)

        # Draw grid
        for x in range(0, self.cols * self.tile_size, self.tile_size):
            for y in range(0, self.rows * self.tile_size, self.tile_size):
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, self.GRAY, rect, 1)

        # Draw shelves (obstacles)
        for sx, sy in self.shelves:
            pygame.draw.rect(self.screen, self.DARK_GRAY, (sy * self.tile_size, sx * self.tile_size, self.tile_size, self.tile_size))

        # Draw pickup and dropoff
        px, py = self.pickup_point
        dx, dy = self.dropoff_point
        pygame.draw.rect(self.screen, self.CYAN, (py * self.tile_size, px * self.tile_size, self.tile_size, self.tile_size))
        pygame.draw.rect(self.screen, self.MAGENTA, (dy * self.tile_size, dx * self.tile_size, self.tile_size, self.tile_size))

        # Draw robots
        for robot in robots:
            pygame.draw.circle(
                self.screen,
                robot.color,
                (robot.y * self.tile_size + self.tile_size // 2, robot.x * self.tile_size + self.tile_size // 2),
                self.tile_size // 3
            )
