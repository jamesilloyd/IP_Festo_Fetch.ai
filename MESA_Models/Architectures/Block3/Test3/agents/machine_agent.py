from mesa import Agent, Model
from .message import Message
from .operations import operationDictionary
import random

'''
Machine 
	- Manages machine agents beneath it
'''

class MachineAgent(Agent):

    agentType = 'machine'

    def __init__(self, unique_id, model, typeOfOperation, coordinates, factoryId,fastOrCheap):
        super().__init__(unique_id, model)
        self.typeOfOperation = typeOfOperation
        self.coordinates = coordinates
        self.factoryId = factoryId
        
        self.isOperating = False
        self.fastOrCheap = fastOrCheap
        if(fastOrCheap == 'cheap'):
            self.hourlyRate = 0.7*random.randrange(operationDictionary[self.typeOfOperation]['resourceHourlyRate'][0],operationDictionary[self.typeOfOperation]['resourceHourlyRate'][1])
            # TODO: there will be some variation here but the actual time will be determined by the type of part
            # self.unitOperationTime = random.randrange(operationDictionary[self.typeOfOperation]['unitOperationTimes'][0],operationDictionary[self.typeOfOperation]['unitOperationTimes'][1])
            self.speedFactor = 1.3
        elif(fastOrCheap == 'asap'):
            self.hourlyRate = 1.3*random.randrange(operationDictionary[self.typeOfOperation]['resourceHourlyRate'][0],operationDictionary[self.typeOfOperation]['resourceHourlyRate'][1])
            # TODO: there will be some variation here but the actual time will be determined by the type of part
            # self.unitOperationTime = random.randrange(operationDictionary[self.typeOfOperation]['unitOperationTimes'][0],operationDictionary[self.typeOfOperation]['unitOperationTimes'][1])
            self.speedFactor = 0.7

        self.timeLeftOnOperation = 0
        self.timeFree = 0
        self.timeWorking = 0
        self.receivedMessages = []
        self.backLogOrders = []
        self.order = None
        self.totalMessagesSent = 0
        self.totalMessagesReceived = 0
        self.timeUntilFree = 0
        self.void = False

        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0

    
        
        # Register the machine with the factory agents and what their capability is
        factoryAgent = self.model.schedule._agents[self.factoryId]
        message = Message(self.unique_id,'accounceCapabilitiesMachine',capability=self.typeOfOperation)
        factoryAgent.receivedMessages.append(message)
        self.totalMessagesSent += 1
        


    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])



    def step(self):
        # If it has an order in the backlog, start working on it 
        if (self.backLogOrders and not self.isOperating):
            self.order = self.backLogOrders[0]
            self.backLogOrders.pop(0)
            print('Backlogsize {}'.format(len(self.backLogOrders)))
            self.order.inOperation = True
            print('Machine {} - moving order {}'.format(self.unique_id,self.order.unique_id))
            self.model.grid.move_agent(self.order,self.coordinates)
            self.isOperating = True
            self.timeLeftOnOperation = self.order.unitOperationTime * self.order.quantity * self.speedFactor
        
        for message in self.receivedMessages:
            if message.type == 'unsuccessfulBid':
                print('Machine {} - received unsuccessful bid notice from order {}'.format(self.unique_id,message.fromId))
                
                # Removed the reserved time for this order
                self.timeUntilFree -= message.orderAgent.quantity * message.orderAgent.unitOperationTime * self.speedFactor
        
        self.receivedMessages.clear()

        # Operate as normal
        if(self.isOperating):
            self.timeLeftOnOperation -= 1
            self.timeWorking += 1
            if(self.timeLeftOnOperation <= 0):
                self.isOperating = False
                # Add the operation to the completed pile
                # self.order.completed = True
                # self.order.completedDate = self.model.schedule.steps
                self.order.status = 'dispatched'
                self.order.winningMachineType = self.fastOrCheap
                agent = self.model.schedule._agents[self.factoryId]
                self.model.grid.move_agent(self.order,agent.dispatchOrderCoordinates)
                
                self.order = None
            
        else:
            self.timeFree += 1

        
        # Just recalculating the timeUntilFree
        backLogSize = self.model.schedule.steps
        if self.order is not None:
            backLogSize += self.timeLeftOnOperation

        for order in self.backLogOrders:
            backLogSize += order.quantity * order.unitOperationTime * self.speedFactor

        if backLogSize > self.timeUntilFree:
            self.timeUntilFree = backLogSize

        
        # Just update this in case we don't have any orders
        if self.timeUntilFree < self.model.schedule.steps:
            self.timeUntilFree = self.model.schedule.steps



