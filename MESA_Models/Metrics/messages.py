
from mesa import Model

def messagesSent(model):
    
    totalMessages = 0

    for agent in model.schedule.agents:
        if agent.agentType == 'order' and not agent.void:
            totalMessages += agent.totalMessagesSent / agent.size
        elif not agent.void:
            totalMessages += agent.totalMessagesSent
    

    return totalMessages


def maxMessagesSentFromNode(model):

    maxMessages = 0


    for agent in model.schedule.agents:
        
        if agent.maxMessagesSent > maxMessages and not agent.void:
            maxMessages = agent.maxMessagesSent

    return maxMessages



def maxMessagesReceivedByNode(model):

    maxMessages = 0

    for agent in model.schedule.agents:
        if agent.maxMessagesReceived > maxMessages and not agent.void:
            maxMessages = agent.maxMessagesReceived 

    return maxMessages







