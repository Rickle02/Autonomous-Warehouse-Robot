import random

class RobotAgent:
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos  # (x, y) coordinates
        self.carrying_item = False

    def sense(self, environment):
        x, y = self.position
        return environment.get_cell(x, y)

    def move(self, direction, warehouse):
        warehouse.move_robot(self, direction)

    def pick_item(self):
        self.carrying_item = True

    def drop_item(self):
        self.carrying_item = False

    def move_towards(self, goal, warehouse):
        goal_x, goal_y = goal
        curr_x, curr_y = self.position

        moves = []

        if curr_x > goal_x:
            moves.append('up')
        elif curr_x < goal_x:
            moves.append('down')

        if curr_y > goal_y:
            moves.append('left')
        elif curr_y < goal_y:
            moves.append('right')

        random.shuffle(moves)  # Randomize preferred moves

        for move in moves:
            if self.can_move(move, warehouse):
                self.move(move, warehouse)
                return

        # Try random moves if preferred blocked
        directions = ['up', 'down', 'left', 'right']
        random.shuffle(directions)
        for move in directions:
            if self.can_move(move, warehouse):
                self.move(move, warehouse)
                return

    def can_move(self, direction, warehouse):
        x, y = self.position
        if direction == 'up':
            new_x, new_y = x - 1, y
        elif direction == 'down':
            new_x, new_y = x + 1, y
        elif direction == 'left':
            new_x, new_y = x, y - 1
        elif direction == 'right':
            new_x, new_y = x, y + 1
        else:
            return False

        return warehouse.is_valid_move(new_x, new_y)

    def check_pickup(self, warehouse):
        x, y = self.position
        cell = warehouse.get_cell(x, y)
        if cell == 'P' and not self.carrying_item:
            print(f"{self.name} picked up an item at {self.position}!")
            self.pick_item()

    def check_dropoff(self, warehouse):
        x, y = self.position
        cell = warehouse.get_cell(x, y)
        if cell == 'D' and self.carrying_item:
            print(f"{self.name} dropped off the item at {self.position}!")
            self.drop_item()

            # After dropping, move one step away to clear space
            directions = ['up', 'down', 'left', 'right']
            for move in directions:
                if self.can_move(move, warehouse):
                    self.move(move, warehouse)
                    break
