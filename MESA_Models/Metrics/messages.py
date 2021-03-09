
from mesa import Model

def messagesSent(model):
    
    totalMessages = 0

    for agent in model.schedule.agents:
        totalMessages += agent.messagesSent
    

    return totalMessages


def maxMessagesSentFromNode(model):

    maxMessages = 0


    for agent in model.schedule.agents:
        if model.schedule.steps == 0 :
            maxMessages = 0
        elif agent.messagesSent / model.schedule.steps > maxMessages:
            maxMessages = agent.messagesSent / model.schedule.steps

    return maxMessages



def maxMessagesReceivedByNode(model):

    maxMessages = 0

    for agent in model.schedule.agents:
        if model.schedule.steps == 0 :
            maxMessages = 0
        elif agent.messagesReceived / model.schedule.steps > maxMessages:
            maxMessages = agent.messagesReceived / model.schedule.steps

    return maxMessages







