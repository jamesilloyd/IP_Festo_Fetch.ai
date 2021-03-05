
from mesa import Model

def messagesSent(model):
    
    totalMessages = 0

    for agent in model.schedule.agents:
        totalMessages += agent.messagesSent
    

    return totalMessages







