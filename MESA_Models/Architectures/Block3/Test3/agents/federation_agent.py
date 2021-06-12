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
        self.totalMessagesSent = 0
        self.totalMessagesReceived = 0
        self.factoryCapabilities = {}

        self.maxMessagesSent = 0
        self.maxMessagesReceived = 0
        self.void = False


    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])

    
    def step(self):
        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0
        for message in self.receivedMessages:
            self.totalMessagesReceived += 1
            self.maxMessagesReceived += 1
            if message.type == 'idsRequest':
                #print('Federator {} - received ids request from order {} for capability {}'.format(self.unique_id,message.fromId,message.capability))
                factoryIds = []
                if message.capability in self.factoryCapabilities:
                    factoryIds.extend(self.factoryCapabilities[message.capability])
                
                newMessage = Message(self.unique_id,'idsResponse',requestedIds=factoryIds)
                
                
                # This returns an empty list if their are no factories with this capability
                agent = self.model.schedule._agents[message.fromId]
                agent.receivedMessages.append(newMessage)
                self.totalMessagesSent += 1
                self.maxMessagesSent  += 1
                    
            if message.type == 'announceCapabiliesFactory':
                for capability in message.capabilities:
                    if capability in self.factoryCapabilities:
                        if(message.fromId not in self.factoryCapabilities[capability]):
                            self.factoryCapabilities[capability].append(message.fromId)
                    else:
                        self.factoryCapabilities.update({capability:[message.fromId]})


        self.receivedMessages.clear()