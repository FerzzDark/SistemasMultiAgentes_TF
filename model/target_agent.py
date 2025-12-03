# model/target.py
from mesa import Agent

class Target(Agent):
    def __init__(self, unique_id, model, kind):
        super().__init__(unique_id, model)
        self.kind = kind  # "pickup" or "dropoff"
