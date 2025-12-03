from mesa import Agent

class RobotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.path = []
        self.current_pickup = None
        self.current_dropoff = None
        self.deliveries_count = 0 
        self.my_reservations = []

    def update_path(self, target):
        current_time = self.model.schedule.steps
        
        # 1. Liberar reservas antiguas
        for res in self.my_reservations:
            if res in self.model.reservations:
                self.model.reservations.remove(res)
        self.my_reservations = []

        # 2. Calcular ruta con A* (Espacio-Tiempo)
        print(f"Robot {self.unique_id}: Buscando ruta de {self.pos} a {target}...") # DEBUG
        
        raw_path = self.model.pathfinder.find_path(
            self.pos, 
            target, 
            self.model.obstacles, 
            self.model.reservations,
            current_time
        )
        
        # 3. VERIFICACIÓN CRÍTICA:
        if raw_path and raw_path[0] == self.pos:
            # Si el primer paso es "quédate donde estás", lo quitamos para empezar a movernos ya
            raw_path.pop(0)
            
        self.path = raw_path

        if not self.path:
            print(f"Robot {self.unique_id}: ¡NO ENCONTRÓ RUTA!") # DEBUG
        else:
            print(f"Robot {self.unique_id}: Ruta encontrada con {len(self.path)} pasos.") # DEBUG

        # 4. Registrar nuevas reservas
        if self.path:
            for t, step_pos in enumerate(self.path):
                # Reservamos para el futuro (t+1 porque nos moveremos en el siguiente step)
                future_time = current_time + 1 + t
                reservation = (step_pos[0], step_pos[1], future_time)
                self.model.reservations.add(reservation)
                self.my_reservations.append(reservation)

    def assign_new_pickup(self):
        self.current_pickup = self.model.get_random_free_cell()
        print(f"Robot {self.unique_id}: Nuevo Pickup en {self.current_pickup}") # DEBUG
        self.model.spawn_target(self.current_pickup, "pickup") 
        self.update_path(self.current_pickup)

    def assign_new_dropoff(self):
        self.current_dropoff = self.model.get_random_free_cell()
        print(f"Robot {self.unique_id}: Nuevo Dropoff en {self.current_dropoff}") # DEBUG
        self.model.spawn_target(self.current_dropoff, "dropoff")
        self.update_path(self.current_dropoff)

    def step(self):
        # 1. Gestión de Tareas
        if self.current_pickup is None and self.current_dropoff is None:
            self.assign_new_pickup()
        
        # 2. Movimiento
        if self.path:
            next_pos = self.path[0]
            
            # Verificamos si la celda está físicamente libre
            cell_contents = self.model.grid.get_cell_list_contents(next_pos)
            agents_in_cell = [a for a in cell_contents if isinstance(a, RobotAgent)]
            
            if not agents_in_cell:
                self.model.grid.move_agent(self, next_pos)
                self.path.pop(0) # ¡Paso completado!
            else:
                print(f"Robot {self.unique_id}: Esperando... celda {next_pos} ocupada.") # DEBUG
                # Si está ocupado, esperamos (no avanzamos en la lista path)
        
        # 3. Verificar Meta
        if self.current_pickup and self.pos == self.current_pickup:
            self.model.remove_target_at(self.current_pickup)
            self.current_pickup = None
            print(f"Robot {self.unique_id}: ¡Recogió paquete!") # DEBUG
            self.assign_new_dropoff()

        elif self.current_dropoff and self.pos == self.current_dropoff:
            self.model.remove_target_at(self.current_dropoff)
            self.current_dropoff = None
            
            self.deliveries_count += 1
            print(f"Robot {self.unique_id}: ¡ENTREGADO! Total: {self.deliveries_count}") # DEBUG
            
            self.assign_new_pickup()