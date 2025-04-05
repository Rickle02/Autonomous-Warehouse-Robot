import random

class RobotAgent:
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos
        self.carrying_item = False
        self.phase = "pickup"

    def sense(self, environment):
        x, y = self.position
        return environment.get_cell(x, y)

    def move(self, direction, warehouse):
        warehouse.move_robot(self, direction)

    def pick_item(self):
        self.carrying_item = True

    def drop_item(self):
        self.carrying_item = False

    def move_one_step_towards(self, goal, warehouse):
        goal_x, goal_y = goal
        curr_x, curr_y = self.position

        if curr_x > goal_x and self.can_move('up', warehouse):
            self.move('up', warehouse)
        elif curr_x < goal_x and self.can_move('down', warehouse):
            self.move('down', warehouse)
        elif curr_y > goal_y and self.can_move('left', warehouse):
            self.move('left', warehouse)
        elif curr_y < goal_y and self.can_move('right', warehouse):
            self.move('right', warehouse)

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
            self.pick_item()
            self.phase = "dropoff"

    def check_dropoff(self, warehouse):
        x, y = self.position
        cell = warehouse.get_cell(x, y)
        if cell == 'D' and self.carrying_item:
            self.drop_item()
            self.phase = "done"
