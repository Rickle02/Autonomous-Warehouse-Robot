import matplotlib.pyplot as plt
import numpy as np

class Warehouse:
    def __init__(self, grid, ax):
        self.grid = grid
        self.robots = []
        self.ax = ax

    def add_robot(self, robot):
        self.robots.append(robot)

    def get_cell(self, x, y):
        return self.grid[x][y]

    def is_valid_move(self, x, y):
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            if self.grid[x][y] != 'S':
                for robot in self.robots:
                    if robot.position == (x, y):
                        return False
                return True
        return False

    def is_cell_occupied(self, x, y):
        for robot in self.robots:
            if robot.position == (x, y):
                return True
        return False

    def move_robot(self, robot, direction):
        x, y = robot.position
        if direction == 'up':
            new_x, new_y = x - 1, y
        elif direction == 'down':
            new_x, new_y = x + 1, y
        elif direction == 'left':
            new_x, new_y = x, y - 1
        elif direction == 'right':
            new_x, new_y = x, y + 1
        else:
            new_x, new_y = x, y

        if self.is_valid_move(new_x, new_y):
            robot.position = (new_x, new_y)

    def render(self):
        self.ax.clear()

        nrows, ncols = len(self.grid), len(self.grid[0])
        warehouse_map = np.ones((nrows, ncols, 3))

        for i in range(nrows):
            for j in range(ncols):
                cell = self.grid[i][j]
                if cell == 'S':
                    warehouse_map[i, j] = [0.4, 0.2, 0.8]
                elif cell == 'P':
                    warehouse_map[i, j] = [0.0, 0.8, 0.0]
                elif cell == 'D':
                    warehouse_map[i, j] = [0.8, 0.0, 0.0]

        self.ax.imshow(warehouse_map, extent=[0, ncols, nrows, 0])

        for x in range(ncols + 1):
            self.ax.axvline(x, color='black', linewidth=0.5)
        for y in range(nrows + 1):
            self.ax.axhline(y, color='black', linewidth=0.5)

        for robot in self.robots:
            rx, ry = robot.position
            self.ax.text(ry + 0.5, rx + 0.5, robot.name, color='black',
                         ha='center', va='center', fontsize=8, fontweight='bold')

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("Warehouse Robot Simulation")
