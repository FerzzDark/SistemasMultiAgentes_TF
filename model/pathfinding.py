import heapq

class AStarPathfinder:
    def __init__(self, grid_width, grid_height):
        self.w = grid_width
        self.h = grid_height

    def heuristic(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def get_neighbors(self, pos):
        x, y = pos
        steps = [(1,0), (-1,0), (0,1), (0,-1), (0,0)]
        neighbors = []
        for dx, dy in steps:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.w and 0 <= ny < self.h:
                neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start, goal, static_obstacles, reservations, start_time=0):
        static_obstacles = set(static_obstacles)
        
        frontier = []
        heapq.heappush(frontier, (0, (start[0], start[1], start_time)))
        
        came_from = {(start[0], start[1], start_time): None}
        cost = {(start[0], start[1], start_time): 0}
        
        max_time_depth = start_time + 100 

        while frontier:
            _, current = heapq.heappop(frontier)
            curr_x, curr_y, curr_t = current

            if (curr_x, curr_y) == goal:
                final_state = current
                break
            
            if curr_t > max_time_depth:
                continue

            next_t = curr_t + 1

            for next_pos in self.get_neighbors((curr_x, curr_y)):
                nx, ny = next_pos
                
                #verificar obstaculos
                if (nx, ny) in static_obstacles:
                    continue
                
                # verificar posiciones
                if (nx, ny, next_t) in reservations:
                    continue
                
                if (nx, ny, curr_t) in reservations and (curr_x, curr_y, next_t) in reservations:
                     continue

                new_cost = cost[current] + 1
                next_state = (nx, ny, next_t)

                if next_state not in cost or new_cost < cost[next_state]:
                    cost[next_state] = new_cost
                    priority = new_cost + self.heuristic(goal, (nx, ny))
                    heapq.heappush(frontier, (priority, next_state))
                    came_from[next_state] = current
        else:
            return []

        #camino declarado
        path = []
        curr = final_state
        while curr is not None:
            path.append((curr[0], curr[1]))
            curr = came_from[curr]
        path.reverse()
        return path