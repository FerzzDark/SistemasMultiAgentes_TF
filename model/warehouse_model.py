from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from random import randint, random

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
        
        self.reservations = set()
        self.obstacles = []       # posicion de los shelfs
        self.packages_delivered = 0 

        # Pathfinding (A*)
        self.pathfinder = AStarPathfinder(width, height)

        # spawn de estantes
        self.spawn_shelves(num_shelves)

        # crear robots
        for i in range(num_robots):
            r = RobotAgent(i, self)
            self.schedule.add(r)
            pos = self.get_random_free_cell()
            self.grid.place_agent(r, pos)

        self.datacollector = DataCollector(
            model_reporters={"Entregas": "packages_delivered"}
        )

    def get_random_free_cell(self):
        while True:
            pos = (randint(0, self.width-1), randint(0, self.height-1))
            if self.grid.is_cell_empty(pos):
                return pos

    def spawn_shelves(self, num_shelves_ignored):
        shelf_id = 1000
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if x % 2 != 0: continue
                if y % 5 == 0: continue
                
                if random() < 0.70: 
                    if self.grid.is_cell_empty((x, y)):
                        # Crear el Agente
                        sh = ShelfAgent(shelf_id, self)
                        self.grid.place_agent(sh, (x, y))
                        self.obstacles.append((x, y))                       
                        shelf_id += 1

    def spawn_target(self, pos, kind):
        t = Target(self.next_id() + 5000, self, kind)
        self.grid.place_agent(t, pos)

    def remove_target_at(self, pos):
        for a in self.grid.get_cell_list_contents(pos):
            if isinstance(a, Target):
                self.grid.remove_agent(a)

    def step(self):
        self.datacollector.collect(self) 
        self.schedule.step()