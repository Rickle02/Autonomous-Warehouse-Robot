class RobotAgent:
    def __init__(self, x, y, color, pickup, dropoff):
        self.x = x
        self.y = y
        self.color = color
        self.pickup = pickup
        self.dropoff = dropoff
        self.carrying = False
        self.phase = 'to_pickup'  # 'to_pickup', 'to_dropoff', 'done'

    def move_one_step(self, warehouse):
        target = self.pickup if self.phase == 'to_pickup' else self.dropoff
        tx, ty = target

        possible_moves = []

        # Try preferred directions first (based on target)
        if self.x < tx:
            possible_moves.append((self.x + 1, self.y))  # move down
        elif self.x > tx:
            possible_moves.append((self.x - 1, self.y))  # move up

        if self.y < ty:
            possible_moves.append((self.x, self.y + 1))  # move right
        elif self.y > ty:
            possible_moves.append((self.x, self.y - 1))  # move left

        # Add alternative directions (not preferred but still valid)
        if (self.x + 1, self.y) not in possible_moves:
            possible_moves.append((self.x + 1, self.y))
        if (self.x - 1, self.y) not in possible_moves:
            possible_moves.append((self.x - 1, self.y))
        if (self.x, self.y + 1) not in possible_moves:
            possible_moves.append((self.x, self.y + 1))
        if (self.x, self.y - 1) not in possible_moves:
            possible_moves.append((self.x, self.y - 1))

        # Move to the first non-obstacle cell found
        for new_x, new_y in possible_moves:
            if 0 <= new_x < warehouse.rows and 0 <= new_y < warehouse.cols:
                if (new_x, new_y) not in warehouse.shelves:
                    self.x, self.y = new_x, new_y
                    break

        # After moving, check if arrived
        if (self.x, self.y) == target:
            if self.phase == 'to_pickup':
                self.carrying = True
                self.phase = 'to_dropoff'
            elif self.phase == 'to_dropoff':
                self.carrying = False
                self.phase = 'done'

