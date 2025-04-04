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

        if curr_x > goal_x and warehouse.is_valid_move(curr_x - 1, curr_y):
            self.move('up', warehouse)
        elif curr_x < goal_x and warehouse.is_valid_move(curr_x + 1, curr_y):
            self.move('down', warehouse)
        elif curr_y > goal_y and warehouse.is_valid_move(curr_x, curr_y - 1):
            self.move('left', warehouse)
        elif curr_y < goal_y and warehouse.is_valid_move(curr_x, curr_y + 1):
            self.move('right', warehouse)
