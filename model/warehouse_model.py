from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from random import randint, random

# Imports relativos
from .robot_agent import RobotAgent
from .shelf_agent import ShelfAgent
from .target_agent import Target
from .pathfinding import AStarPathfinder

class WarehouseModel(Model):
    def __init__(self, width=20, height=20, num_robots=3, num_shelves=20):
        super().__init__()
        self.width = width
        self.height = height
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        
        # --- Variables Clave ---
        self.reservations = set()
        self.obstacles = []       # Aquí guardaremos las posiciones de los estantes
        self.packages_delivered = 0 

        # Pathfinding
        self.pathfinder = AStarPathfinder(width, height)

        # 1. CREAR ESTANTES (Llamamos a la función, no la definimos aquí)
        self.spawn_shelves(num_shelves)

        # 2. CREAR ROBOTS
        for i in range(num_robots):
            r = RobotAgent(i, self)
            self.schedule.add(r)
            pos = self.get_random_free_cell()
            self.grid.place_agent(r, pos)

        # 3. RECOLECTOR DE DATOS
        self.datacollector = DataCollector(
            model_reporters={"Entregas": "packages_delivered"}
        )

    def get_random_free_cell(self):
        while True:
            pos = (randint(0, self.width-1), randint(0, self.height-1))
            if self.grid.is_cell_empty(pos):
                return pos

    # --- DEFINICIÓN CORRECTA DE SPAWN_SHELVES ---
    def spawn_shelves(self, num_shelves_ignored):
        shelf_id = 1000
        # Lógica de "Filas Rotas"
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if x % 2 != 0: continue
                if y % 5 == 0: continue
                
                if random() < 0.70: 
                    if self.grid.is_cell_empty((x, y)):
                        # Crear el Agente
                        sh = ShelfAgent(shelf_id, self)
                        self.grid.place_agent(sh, (x, y))
                        
                        # --- CRÍTICO: Agregar a la lista de obstáculos ---
                        self.obstacles.append((x, y)) 
                        # -----------------------------------------------
                        
                        shelf_id += 1

    def spawn_target(self, pos, kind):
        # IDs altos para no chocar con robots ni estantes
        t = Target(self.next_id() + 5000, self, kind)
        self.grid.place_agent(t, pos)

    def remove_target_at(self, pos):
        for a in self.grid.get_cell_list_contents(pos):
            if isinstance(a, Target):
                self.grid.remove_agent(a)

    def step(self):
        self.datacollector.collect(self) 
        self.schedule.step()