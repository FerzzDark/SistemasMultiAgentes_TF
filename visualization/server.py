from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model.warehouse_model import WarehouseModel
from .portrayals import agent_portrayal

# Grid 
grid = CanvasGrid(agent_portrayal, 25, 25, 800 , 800)

server = ModularServer(
    WarehouseModel,
    [grid],
    "Sistema MultiAgente - Robots en Almacen",
    {"width": 25, "height": 25, "num_robots": 5, "num_shelves": 100}
)
server.description = """
Trabajo Final de Tópicos en Ciencias de la Computación
Esta simulación demuestra el uso de Sistemas Multiagentes 
para la gestión de un almacen. Los robots utilizan un algoritmo A* con reservas espacio-temporales para evitar colisiones.
"""

server.port = 8521

def run_server():
    server.launch()

#TRIALGITT