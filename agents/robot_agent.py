from collections import deque

class RobotAgent:
    def __init__(self, x, y, color, pickup, dropoff):
        self.x = x
        self.y = y
        self.color = color
        self.pickup = pickup
        self.dropoff = dropoff
        self.carrying = False
        self.phase = 'to_pickup'  # 'to_pickup', 'to_dropoff', 'done'
        self.path = []  # path found using BFS

    def bfs(self, warehouse, target):
        queue = deque()
        queue.append((self.x, self.y, []))
        visited = set()
        visited.add((self.x, self.y))

        while queue:
            x, y, path = queue.popleft()

            if (x, y) == target:
                return path

            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < warehouse.rows and 0 <= ny < warehouse.cols:
                    if (nx, ny) not in warehouse.shelves and (nx, ny) not in visited:
                        queue.append((nx, ny, path + [(nx, ny)]))
                        visited.add((nx, ny))
        return []

    def move_one_step(self, warehouse):
        if not self.path:
            if self.phase == 'to_pickup':
                self.path = self.bfs(warehouse, self.pickup)
            elif self.phase == 'to_dropoff':
                self.path = self.bfs(warehouse, self.dropoff)

        if self.path:
            next_pos = self.path.pop(0)
            self.x, self.y = next_pos

        if (self.x, self.y) == self.pickup and self.phase == 'to_pickup':
            self.carrying = True
            self.phase = 'to_dropoff'
            self.path = []
        elif (self.x, self.y) == self.dropoff and self.phase == 'to_dropoff':
            self.carrying = False
            self.phase = 'done'
            self.path = []
