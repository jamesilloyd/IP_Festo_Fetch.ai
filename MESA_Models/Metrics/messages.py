
from mesa import Model

def messagesSent(model):
    
    totalMessages = 0

    for agent in model.schedule.agents:
        totalMessages += agent.messagesSent
    

    return totalMessages


def maxMessagesSentFromNode(model):

    maxMessages = 0


    for agent in model.schedule.agents:
        
        if agent.maxMessagesSent > maxMessages:
            maxMessages = agent.maxMessagesSent

    return maxMessages



def maxMessagesReceivedByNode(model):

    maxMessages = 0

    for agent in model.schedule.agents:
        if agent.maxMessagesReceived > maxMessages:
            maxMessages = agent.maxMessagesReceived 

    return maxMessages







