from mesa import Agent, Model
import random
from .message import Message

'''
	- Assists other holons in performing their work
	- Considered an external expert that gives advice
	- But the basic holon still makes the decision
	- Allows for centralised elements in the architecture
		○ Solves problems that are almost impossible in a distributed manner
	- They may request information from orders and resources so they have a full-view of the system
		○ This can allow orders or resources to have a schedule
		○ But it is advice, not commands
...Could be used to represent the MES, or shop floor control
'''
class TrustFederationAgent(Agent):
    
    agentType = 'federator'

    def __init__(self, unique_id, model, coordinates):
        super().__init__(unique_id, model)
        
        self.coordinates = coordinates

        self.receivedMessages = []
        self.messagesSent = 0
        self.messagesReceived = 0
        self.factoryCapabilities = {}

        self.maxMessagesSent = 0
        self.maxMessagesReceived = 0


        

    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])

    
    def step(self):
        messagesReceived = 0
        messagesSent = 0
        for message in self.receivedMessages:
            self.messagesReceived += 1
            messagesReceived += 1
            if message.type == 'idsRequest':
                print('Federator {} - received ids request from order {} for capability {}'.format(self.unique_id,message.fromId,message.capability))
                factoryIds = []
                if message.capability in self.factoryCapabilities:
                    factoryIds.extend(self.factoryCapabilities[message.capability])
                
        
                newMessage = Message(self.unique_id,'idsResponse',requestedIds=factoryIds)
                
                for agent in self.model.schedule.agents:
                    if agent.unique_id == message.fromId:
                        agent.receivedMessages.append(newMessage)
                        self.messagesSent += 1
                        messagesSent  += 1
                else:
                    # TODO: handle capability not existing
                    pass
                    
            if message.type == 'announceCapabiliesFactory':
                for capability in message.capabilities:
                    if capability in self.factoryCapabilities:
                        if(message.fromId not in self.factoryCapabilities[capability]):
                            self.factoryCapabilities[capability].append(message.fromId)
                    else:
                        self.factoryCapabilities.update({capability:[message.fromId]})


        

        self.receivedMessages.clear()

        if self.model.schedule.steps > 5:
            if messagesSent > self.maxMessagesSent:
                self.maxMessagesSent = messagesSent
            if messagesReceived > self.maxMessagesReceived:
                self.maxMessagesReceived = messagesReceived


        



    


