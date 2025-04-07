from collections import deque
import heapq

class RobotAgent:
    def __init__(self, start_pos, color, pickup_point, dropoff_point, method='default'):
        self.x, self.y = start_pos
        self.color = color
        self.pickup_point = pickup_point
        self.dropoff_point = dropoff_point
        self.method = method

        self.phase = 'start'
        self.task = None
        self.carrying_package = False
        self.rest_place = start_pos
        self.waiting = False

    def get_action(self, current_pos, warehouse, robots):
        if self.phase == 'start':
            return current_pos

        if self.phase == 'pickup':
            if warehouse.is_occupied(self.pickup_point, robots):
                goal = self.find_waiting_spot(warehouse, robots)
            else:
                goal = self.pickup_point
        elif self.phase == 'deliver':
            goal = self.dropoff_point
        elif self.phase == 'rest':
            goal = self.rest_place
        else:
            goal = None

        if goal:
            path = self.search(current_pos, goal, warehouse, robots)
            if path and len(path) > 0:
                return path[0]
        return current_pos

    def find_waiting_spot(self, warehouse, robots):
        queue = deque()
        visited = set()
        queue.append(self.pickup_point)
        visited.add(self.pickup_point)

        while queue:
            current = queue.popleft()
            for neighbor in warehouse.get_neighbors(current):
                if neighbor not in visited:
                    if not warehouse.is_occupied(neighbor, robots):
                        return neighbor
                    queue.append(neighbor)
                    visited.add(neighbor)
        return self.pickup_point

    def update_phase(self, warehouse):
        if self.phase == 'start':
            self.phase = 'pickup'
            return

        if self.phase == 'pickup' and (self.x, self.y) == self.pickup_point:
            if warehouse.packages_to_deliver > 0:
                self.carrying_package = True
                self.phase = 'deliver'
            else:
                self.phase = 'rest'

        elif self.phase == 'deliver' and (self.x, self.y) == self.dropoff_point:
            self.carrying_package = False
            warehouse.packages_to_deliver -= 1
            if warehouse.packages_to_deliver == 0:
                self.phase = 'rest'
            else:
                self.phase = 'pickup'

        elif self.phase == 'rest' and (self.x, self.y) == self.rest_place:
            self.phase = 'done'

    def search(self, start, goal, warehouse, robots):
        if self.method == 'bfs':
            return self.bfs(start, goal, warehouse, robots)
        elif self.method == 'dfs':
            return self.dfs(start, goal, warehouse, robots)
        elif self.method == 'greedy':
            return self.greedy(start, goal, warehouse, robots)
        elif self.method == 'astar':
            return self.astar(start, goal, warehouse, robots)
        else:
            return self.bfs(start, goal, warehouse, robots)

    def bfs(self, start, goal, warehouse, robots):
        queue = deque()
        queue.append((start, []))
        visited = set()
        visited.add(start)

        while queue:
            (current, path) = queue.popleft()
            if current == goal:
                return path

            for neighbor in warehouse.get_neighbors(current):
                if neighbor not in visited and not warehouse.is_occupied(neighbor, robots):
                    queue.append((neighbor, path + [neighbor]))
                    visited.add(neighbor)
        return []

    def dfs(self, start, goal, warehouse, robots):
        stack = [(start, [])]
        visited = set()
        visited.add(start)

        while stack:
            (current, path) = stack.pop()
            if current == goal:
                return path

            for neighbor in warehouse.get_neighbors(current):
                if neighbor not in visited and not warehouse.is_occupied(neighbor, robots):
                    stack.append((neighbor, path + [neighbor]))
                    visited.add(neighbor)
        return []

    def greedy(self, start, goal, warehouse, robots):
        heap = [(self.heuristic(start, goal), start, [])]
        visited = set()
        visited.add(start)

        while heap:
            (_, current, path) = heapq.heappop(heap)
            if current == goal:
                return path

            for neighbor in warehouse.get_neighbors(current):
                if neighbor not in visited and not warehouse.is_occupied(neighbor, robots):
                    heapq.heappush(heap, (self.heuristic(neighbor, goal), neighbor, path + [neighbor]))
                    visited.add(neighbor)
        return []

    def astar(self, start, goal, warehouse, robots):
        heap = [(self.heuristic(start, goal), 0, start, [])]
        visited = set()
        visited.add(start)

        while heap:
            (f, g, current, path) = heapq.heappop(heap)
            if current == goal:
                return path

            for neighbor in warehouse.get_neighbors(current):
                if neighbor not in visited and not warehouse.is_occupied(neighbor, robots):
                    new_g = g + 1
                    new_f = new_g + self.heuristic(neighbor, goal)
                    heapq.heappush(heap, (new_f, new_g, neighbor, path + [neighbor]))
                    visited.add(neighbor)
        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
