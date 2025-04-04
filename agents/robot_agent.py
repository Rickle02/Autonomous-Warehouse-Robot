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
