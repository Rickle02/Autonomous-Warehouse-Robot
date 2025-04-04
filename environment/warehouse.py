class Warehouse:
    def __init__(self, grid):
        self.grid = grid
        self.robots = []  # list of robots in the warehouse

    def add_robot(self, robot):
        self.robots.append(robot)

    def is_valid_move(self, x, y):
        # Check if x, y are within bounds
        if x < 0 or x >= len(self.grid) or y < 0 or y >= len(self.grid[0]):
            return False
        # Check if the cell is not a shelf ('S')
        return self.grid[x][y] != 'S'

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
            return  # invalid direction

        if self.is_valid_move(new_x, new_y):
            robot.position = (new_x, new_y)

    def display(self):
        # Create a fresh empty grid to display (without modifying original)
        display_grid = []
        for i in range(len(self.grid)):
            row = []
            for j in range(len(self.grid[0])):
                cell = self.grid[i][j]
                row.append(cell)
            display_grid.append(row)

        # Now place the robots
        for robot in self.robots:
            x, y = robot.position
            display_grid[x][y] = 'R'

        # Print the display grid nicely
        for row in display_grid:
            print(' '.join(row))
        print()  # blank line after displaying

    def get_cell(self, x, y):
        if 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]):
            return self.grid[x][y]
        return None
