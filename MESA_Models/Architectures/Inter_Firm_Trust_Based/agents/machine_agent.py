from mesa import Agent, Model
from .message import Message
import calendar

'''
Resource agent
	- Physical part within the manufacturing system
	- A human can be part of many holarchies (very desirable)
	- Contains data on
		○ Capabilities 
		○ Running tasks
        -Sub-resources 
        -log of activities
'''
class MachineAgent(Agent):

    agentType = 'machine'


    def __init__(self, unique_id, model, typeOfOperation, coordinates, factoryId, cost):
        super().__init__(unique_id, model)
        self.typeOfOperation = typeOfOperation
        # self.timeToComplete = timeToComplete
        self.coordinates = coordinates
        self.factoryId = factoryId
        
        
        self.isOperating = False
        self.cost = cost
        self.timeLeftOnOperation = 0
        self.timeFree = 0
        self.timeWorking = 0
        self.receivedMessages = []
        self.backLogOrders = []
        self.order = None    
        self.messagesSent = 0
        self.messagesReceived = 0
        self.timeUntilFree = 0

        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0

    
        
        # Register the machine with the factory agents and what their capability is
        for agent in self.model.schedule.agents:
            if(agent.unique_id == self.factoryId):

                message = Message(self.unique_id,'accounceCapabilitiesMachine',capability=self.typeOfOperation)
                agent.receivedMessages.append(message)
                self.messagesSent += 1
        


    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])



    def step(self):
        # If it has an order in the backlog, start working on it 
        if (self.backLogOrders and not self.isOperating):
            self.order = self.backLogOrders[0]
            self.order.inOperation = True
            self.model.grid.move_agent(self.order,self.coordinates)
            self.isOperating = True
            self.timeLeftOnOperation = self.order.timeToComplete * self.order.quantity

        
        for message in self.receivedMessages:
            if message.type == 'unsuccessfulBid':
                print('Machine {} - received unsuccessful bid notice from order {}'.format(self.unique_id,message.fromId))
                
                self.timeUntilFree -= message.orderAgent.quantity * message.orderAgent.timeToComplete
        
        self.receivedMessages.clear()
        
        # print('Machine {} time till free = {}'.format(self.unique_id,self.timeUntilFree))

                

        # Operate as normal
        if(self.isOperating):
            self.timeLeftOnOperation -= 1
            self.timeWorking += 1
            if(self.timeLeftOnOperation == 0):
                self.backLogOrders.pop(0)
                self.isOperating = False
                # Add the operation to the completed pile
                self.order.completed = True
                self.order.completedDate = self.model.schedule.steps
                for agent in self.model.schedule.agents:
                    if agent.unique_id == self.factoryId:
                        self.model.grid.move_agent(self.order,agent.completedOrderCoordinates)
                
        else:
            self.timeFree += 1

        if self.timeUntilFree < self.model.schedule.steps:
            self.timeUntilFree = self.model.schedule.steps


        #Check for messages from the scheduler and respond with status and backlog (OR scheduler does this through live lookup)


