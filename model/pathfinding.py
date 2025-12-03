import heapq

class AStarPathfinder:
    def __init__(self, grid_width, grid_height):
        self.w = grid_width
        self.h = grid_height

    def heuristic(self, a, b):
        # Manhattan
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def get_neighbors(self, pos):
        x, y = pos
        # AGREGAMOS (0,0) para permitir que el robot ESPERE en su sitio
        steps = [(1,0), (-1,0), (0,1), (0,-1), (0,0)]
        neighbors = []
        for dx, dy in steps:
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.w and 0 <= ny < self.h:
                neighbors.append((nx, ny))
        return neighbors

    # CAMBIO: Ahora recibimos 'reservations' en lugar de solo obstáculos fijos
    # reservations es un set de tuplas (x, y, t)
    def find_path(self, start, goal, static_obstacles, reservations, start_time=0):
        static_obstacles = set(static_obstacles)
        
        frontier = []
        # El estado ahora incluye TIEMPO: (x, y, time)
        heapq.heappush(frontier, (0, (start[0], start[1], start_time)))
        
        # came_from guarda estados con tiempo
        came_from = {(start[0], start[1], start_time): None}
        cost = {(start[0], start[1], start_time): 0}
        
        # Limite para evitar bucles infinitos esperando
        max_time_depth = start_time + 100 

        while frontier:
            _, current = heapq.heappop(frontier)
            curr_x, curr_y, curr_t = current

            # Si llegamos al goal (posición correcta, cualquier tiempo)
            if (curr_x, curr_y) == goal:
                final_state = current
                break
            
            # Si tardamos demasiado, abortamos
            if curr_t > max_time_depth:
                continue

            # El siguiente paso ocurre en t + 1
            next_t = curr_t + 1

            for next_pos in self.get_neighbors((curr_x, curr_y)):
                nx, ny = next_pos
                
                # 1. Verificar obstáculos estáticos (muros)
                if (nx, ny) in static_obstacles:
                    continue
                
                # 2. Verificar RESERVAS dinámicas (otros robots)
                # ¿Está la celda ocupada en el tiempo t+1?
                if (nx, ny, next_t) in reservations:
                    continue
                
                # Lógica para evitar choques de frente (edge collision)
                # Si yo voy de A->B y otro va de B->A al mismo tiempo
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
            return [] # No path found

        # Reconstruir camino
        path = []
        curr = final_state
        while curr is not None:
            # Solo guardamos (x, y), el tiempo está implícito en el índice de la lista
            path.append((curr[0], curr[1]))
            curr = came_from[curr]
        path.reverse()
        return path