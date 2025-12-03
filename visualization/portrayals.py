from model.robot_agent import RobotAgent
from model.shelf_agent import ShelfAgent
from model.target_agent import Target

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {}

    if isinstance(agent, RobotAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "#2196F3",
            "Filled": "true",
            "r": 0.8,
            "Layer": 2,
            "text": f"{agent.unique_id}\n({agent.deliveries_count})", 
            "text_color": "white"
        }

    elif isinstance(agent, ShelfAgent):
        portrayal = {
            "Shape": "rect",
            "Color": "#F9A825",
            "Filled": "true",
            "w": 0.85,
            "h": 0.85,
            "Layer": 0
        }

    elif isinstance(agent, Target):
        color = "#4CAF50" if agent.kind == "pickup" else "#E91E63"
        portrayal = {
            "Shape": "rect",
            "Color": color,
            "Filled": "true",
            "w": 0.6,
            "h": 0.6,
            "Layer": 1
        }

    return portrayal