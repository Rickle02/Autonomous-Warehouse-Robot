from collections import deque
import heapq
import time

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

        # Resting related
        self.items_handled = 0
        self.need_rest = False
        self.rest_target = None
        self.rest_start_time = None

    def get_action(self, current_pos, warehouse, robots):
        if self.phase == 'pickup_from_source':
            goal = self.pickup_point
        elif self.phase == 'store_in_shelf' and self.target_shelf:
            goal = self.target_shelf
        elif self.phase == 'pickup_from_shelf' and self.task_shelf:
            goal = self.task_shelf
        elif self.phase == 'deliver_to_dropoff':
            goal = self.dropoff_point
        elif self.phase == 'going_to_rest' and self.rest_target:
            goal = self.rest_target
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
                self.items_handled += 1

                # Need to rest after every 5 items
                if self.items_handled % 5 == 0:
                    self.need_rest = True
                    self.rest_target = self.find_nearest_rest_place(warehouse, robots)
                    if self.rest_target:
                        self.phase = 'going_to_rest'
                        self.status_text = "Going to rest place..."
                    else:
                        self.phase = 'pickup_from_source'
                        self.status_text = "No rest available, continue working"
                else:
                    self.phase = 'pickup_from_source'
                    self.status_text = "Delivered, going to Pickup Point"

        elif self.phase == 'going_to_rest':
            if self.rest_target is None or self.rest_target_occupied(warehouse, robots):
                self.rest_target = self.find_nearest_rest_place(warehouse, robots)

            if self.rest_target and (self.x, self.y) == self.rest_target:
                self.phase = 'resting'
                self.rest_start_time = time.time()
                self.status_text = "Resting..."

        elif self.phase == 'resting':
            if time.time() - self.rest_start_time >= 5:
                self.need_rest = False
                self.rest_target = None
                self.rest_start_time = None
                self.phase = 'pickup_from_source'
                self.status_text = "Rest finished, going to Pickup Point"

    def rest_target_occupied(self, warehouse, robots):
        for r in robots:
            if (r.x, r.y) == self.rest_target and r != self:
                return True
        return False

    def find_nearest_rest_place(self, warehouse, robots):
        occupied = {(r.x, r.y) for r in robots}
        available = [place for place in warehouse.rest_places if place not in occupied]

        if not available:
            return None

        def manhattan(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        current_pos = (self.x, self.y)
        available.sort(key=lambda pos: manhattan(current_pos, pos))
        return available[0]

    def search(self, start, goal, warehouse, robots):
        if self.method == 'bfs':
            return self.bfs(start, goal, warehouse, robots)
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
