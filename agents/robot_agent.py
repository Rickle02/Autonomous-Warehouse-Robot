import random
from collections import deque
import heapq
import time

class RobotAgent:
    def __init__(self, start_pos, color, pickup_point, dropoff_point, method='default', running_mode=1):
        self.running_mode = running_mode
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

        self.items_handled = 0
        self.rest_target = None
        self.rest_start_time = None

        self.pickup_count = 0
        self.shelf_delivery_count = 0

    def get_action(self, current_pos, warehouse, robots):
        if self.phase == 'done':
            return current_pos

        if self.phase == 'going_to_rest' and self.rest_target:
            if (self.x, self.y) == self.rest_target:
                self.phase = 'charging'
                self.rest_start_time = time.time()
                self.status_text = "Charging at rest place..."
                return current_pos
            else:
                path = self.search(current_pos, self.rest_target, warehouse, robots)
                if path and len(path) > 0:
                    return path[0]
                else:
                    return current_pos

        goal = None
        if self.phase == 'pickup_from_source':
            goal = self.pickup_point
        elif self.phase == 'store_in_shelf' and self.target_shelf:
            goal = self.target_shelf
        elif self.phase == 'pickup_from_shelf' and self.task_shelf:
            goal = self.task_shelf
        elif self.phase == 'deliver_to_dropoff':
            goal = self.dropoff_point

        if goal:
            path = self.search(current_pos, goal, warehouse, robots)
            if path and len(path) > 0:
                return path[0]
        return current_pos

    def update_phase(self, warehouse, robots):
        self.check_and_update_mission(warehouse)

        if self.phase == 'pickup_from_source':
            if warehouse.pickup_items_count() == 0 and warehouse.live_items_in_shelves() == 0:
                self.rest_target = self.find_rest_place_for_charging(warehouse, robots)
                if self.rest_target:
                    self.phase = 'going_to_rest'
                    self.rest_start_time = None
                    self.status_text = "No work. Moving to rest place..."
                else:
                    self.phase = 'charging'
                    self.rest_start_time = time.time()
                    self.status_text = "No work and no path. Charging here..."
                return

            if warehouse.pickup_items_count() == 0 and warehouse.live_items_in_shelves() > 0:
                self.phase = 'pickup_from_shelf'
                self.task_shelf = warehouse.find_filled_shelf()
                if self.task_shelf:
                    warehouse.reserve_item(self.task_shelf, id(self))
                    self.status_text = f"Switched: Taking from {self.task_shelf}"
                else:
                    self.status_text = "No shelves found. Waiting..."
                return

            if warehouse.find_empty_shelf() is None:
                self.phase = 'pickup_from_shelf'
                self.task_shelf = warehouse.find_filled_shelf()
                if self.task_shelf:
                    warehouse.reserve_item(self.task_shelf, id(self))
                    self.status_text = f"No empty shelf! Taking from {self.task_shelf}"
                else:
                    self.status_text = "No empty shelf! Waiting..."
            elif (self.x, self.y) == self.pickup_point:
                if len(warehouse.pickup_queue) > 0:
                    warehouse.pickup_item_done()
                    self.carrying_package = True
                    self.target_shelf = warehouse.find_empty_shelf()
                    if self.target_shelf:
                        self.phase = 'store_in_shelf'
                        self.status_text = f"Picked from Pickup, storing at {self.target_shelf}"
                        self.pickup_count += 1
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
                    warehouse.reserve_item(self.task_shelf, id(self))
                    self.status_text = f"Order: Take from {self.task_shelf}"
                else:
                    self.status_text = "Waiting for order"

        elif self.phase == 'pickup_from_shelf':
            if warehouse.live_items_in_shelves() == 0 and warehouse.pickup_items_count() == 0:
                self.rest_target = self.find_rest_place_for_charging(warehouse, robots)
                if self.rest_target:
                    self.phase = 'going_to_rest'
                    self.rest_start_time = None
                    self.status_text = "No shelves. Moving to rest place..."
                else:
                    self.phase = 'charging'
                    self.rest_start_time = time.time()
                    self.status_text = "No shelves and no rest path. Charging..."
                return

            if self.task_shelf and not warehouse.items.get(self.task_shelf, False):
                self.task_shelf = warehouse.find_filled_shelf()
                if self.task_shelf:
                    warehouse.reserve_item(self.task_shelf, id(self))
                    self.status_text = f"Reassigned: Taking from {self.task_shelf}"
                else:
                    self.status_text = "Waiting for new task"
                return

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
                self.shelf_delivery_count += 1

                if self.running_mode in [2, 3] and self.items_handled % 5 == 0:
                    self.rest_target = self.find_rest_place_for_charging(warehouse, robots)
                    if self.rest_target:
                        self.phase = 'going_to_rest'
                        self.rest_start_time = None
                        self.status_text = "5 deliveries done. Moving to rest place..."
                    else:
                        self.phase = 'charging'
                        self.rest_start_time = time.time()
                        self.status_text = "5 deliveries done. Charging here..."
                else:
                    if warehouse.pickup_items_count() == 0 and warehouse.live_items_in_shelves() == 0:
                        self.rest_target = self.find_rest_place_for_charging(warehouse, robots)
                        if self.rest_target:
                            self.phase = 'going_to_rest'
                            self.rest_start_time = None
                            self.status_text = "No more work. Moving to rest place..."
                        else:
                            self.phase = 'charging'
                            self.rest_start_time = time.time()
                            self.status_text = "No work. Charging here..."
                    else:
                        self.phase = 'pickup_from_source'
                        self.status_text = "Delivered. Going to Pickup Point."

        elif self.phase == 'going_to_rest':
            if self.rest_target is None or self.rest_target_occupied(warehouse, robots):
                self.rest_target = self.find_rest_place_for_charging(warehouse, robots)

            if self.rest_target:
                if (self.x, self.y) == self.rest_target:
                    self.phase = 'charging'
                    self.status_text = "Charging at rest place..."
            else:
                self.phase = 'charging'
                self.rest_start_time = time.time()
                self.status_text = "No path to rest place. Charging here."

        elif self.phase == 'charging':
            if self.rest_start_time is None:
                self.rest_start_time = time.time()

            elapsed = time.time() - self.rest_start_time

            if elapsed >= 5:
                if warehouse.pickup_items_count() > 0 or warehouse.live_items_in_shelves() > 0:
                    self.phase = 'pickup_from_source'
                    self.rest_target = None
                    self.rest_start_time = None
                    self.status_text = "Charging complete! New task available."
                else:
                    self.status_text = "Charging done. Waiting..."
            else:
                self.status_text = f"Charging... ({int(elapsed)} sec)"

    def check_and_update_mission(self, warehouse):
        pass

    def find_rest_place_for_charging(self, warehouse, robots):
        occupied = {(r.x, r.y) for r in robots}
        available_places = [p for p in warehouse.rest_places if p not in occupied]

        if not available_places:
            return None

        current_pos = (self.x, self.y)
        random.shuffle(available_places)  # Randomize

        for place in available_places:
            path = self.search(current_pos, place, warehouse, robots)
            if path and len(path) > 0:
                return place

        return None

    def rest_target_occupied(self, warehouse, robots):
        for r in robots:
            if (r.x, r.y) == self.rest_target and r != self:
                return True
        return False

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
