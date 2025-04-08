from collections import deque
import heapq

class RobotAgent:
    def __init__(self, start_pos, color, pickup_point, dropoff_point, method='default'):
        self.x, self.y = start_pos
        self.color = color
        self.pickup_point = pickup_point
        self.dropoff_point = dropoff_point
        self.method = method

        self.phase = 'pickup_from_source'
        self.carrying_package = False
        self.target_shelf = None
        self.task_shelf = None
        self.status_text = "Idle"

    def get_action(self, current_pos, warehouse, robots):
        if self.phase == 'pickup_from_source':
            goal = self.pickup_point
        elif self.phase == 'store_in_shelf' and self.target_shelf:
            goal = self.target_shelf
        elif self.phase == 'pickup_from_shelf' and self.task_shelf:
            goal = self.task_shelf
        elif self.phase == 'deliver_to_dropoff':
            goal = self.dropoff_point
        else:
            goal = None

        if goal:
            path = self.search(current_pos, goal, warehouse, robots)
            if path and len(path) > 0:
                return path[0]
        return current_pos

    def update_phase(self, warehouse, robots):
        if self.phase == 'pickup_from_source':
            if (self.x, self.y) == self.pickup_point:
                self.carrying_package = True
                self.target_shelf = warehouse.find_empty_shelf()
                if self.target_shelf:
                    self.phase = 'store_in_shelf'
                    self.status_text = f"Picked from P, storing at {self.target_shelf}"
                else:
                    self.status_text = "No empty shelf!"

        elif self.phase == 'store_in_shelf':
            if (self.x, self.y) == self.target_shelf:
                warehouse.store_item((self.x, self.y))
                self.carrying_package = False
                self.target_shelf = None
                self.phase = 'pickup_from_shelf'
                self.task_shelf = warehouse.find_filled_shelf()
                if self.task_shelf:
                    self.status_text = f"Order: Take from {self.task_shelf}"
                else:
                    self.status_text = "Waiting for order"

        elif self.phase == 'pickup_from_shelf':
            if self.task_shelf and (self.x, self.y) == self.task_shelf:
                warehouse.remove_item((self.x, self.y))
                self.carrying_package = True
                self.phase = 'deliver_to_dropoff'
                self.status_text = f"Picked from shelf {self.task_shelf}, delivering"

        elif self.phase == 'deliver_to_dropoff':
            if (self.x, self.y) == self.dropoff_point:
                warehouse.items_delivered += 1
                self.carrying_package = False
                self.task_shelf = None
                self.phase = 'pickup_from_source'
                self.status_text = "Delivered, going to Pickup Point"

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

            for neighbor in warehouse.get_neighbors(current, robot_phase=self.phase):
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

            for neighbor in warehouse.get_neighbors(current, robot_phase=self.phase):
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

            for neighbor in warehouse.get_neighbors(current, robot_phase=self.phase):
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

            for neighbor in warehouse.get_neighbors(current, robot_phase=self.phase):
                if neighbor not in visited and not warehouse.is_occupied(neighbor, robots):
                    new_g = g + 1
                    new_f = new_g + self.heuristic(neighbor, goal)
                    heapq.heappush(heap, (new_f, new_g, neighbor, path + [neighbor]))
                    visited.add(neighbor)
        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
