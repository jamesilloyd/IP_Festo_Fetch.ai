
from mesa import Model

def messagesSent(model):
    
    totalMessages = 0

    for agent in model.schedule.agents:
        if agent.agentType == 'order' and not agent.void:
            totalMessages += agent.totalMessagesSent / agent.size
        elif not agent.void:
            totalMessages += agent.totalMessagesSent
    

    return totalMessages


def maxMessagesSentFromOrder(model):

    maxMessages = 0

    for agent in model.schedule.agents:
        if agent.maxMessagesSent > maxMessages and not agent.void and agent.agentType == 'order':
            maxMessages = agent.maxMessagesSent

    return maxMessages



def maxMessagesReceivedByOrder(model):

    maxMessages = 0

    for agent in model.schedule.agents:
        if agent.maxMessagesReceived > maxMessages and not agent.void and agent.agentType == 'order':
            maxMessages = agent.maxMessagesReceived 

    return maxMessages



def maxMessagesSentFromFactory(model):

    maxMessages = 0

    for agent in model.schedule.agents:
        
        if agent.maxMessagesSent > maxMessages and not agent.void and agent.agentType == 'factory':
            maxMessages = agent.maxMessagesSent

    return maxMessages



def maxMessagesReceivedByFactory(model):

    maxMessages = 0

    for agent in model.schedule.agents:
        if agent.maxMessagesReceived > maxMessages and not agent.void and agent.agentType == 'factory':
            maxMessages = agent.maxMessagesReceived 

    return maxMessages






