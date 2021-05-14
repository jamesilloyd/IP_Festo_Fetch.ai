from mesa import Agent, Model
from .message import Message
from .operations import operationDictionary
import random

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

    def __init__(self, unique_id, model, typeOfOperation, coordinates, factoryId,schedulingType):
        super().__init__(unique_id, model)
        self.typeOfOperation = typeOfOperation
        # self.timeToComplete = timeToComplete
        self.coordinates = coordinates
        self.factoryId = factoryId
        self.schedulingType = schedulingType
        self.isOperating = False
        self.hourlyRate = random.randrange(operationDictionary[self.typeOfOperation]['resourceHourlyRate'][0],operationDictionary[self.typeOfOperation]['resourceHourlyRate'][1])
        self.timeLeftOnOperation = 0
        self.timeFree = 0
        self.timeWorking = 0
        self.receivedMessages = []
        self.backLogOrders = []
        self.order = None
        self.messagesSent = 0
        self.messagesReceived = 0
        self.timeUntilFree = 0
        self.void = False

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
            self.backLogOrders.pop(0)
            self.order.inOperation = True
            print('Machine {} - moving order {}'.format(self.unique_id,self.order.unique_id))
            self.model.grid.move_agent(self.order,self.coordinates)
            self.isOperating = True
            self.timeLeftOnOperation = self.order.timeToComplete * self.order.quantity
        
        for message in self.receivedMessages:
            if message.type == 'unsuccessfulBid':
                print('Machine {} - received unsuccessful bid notice from order {}'.format(self.unique_id,message.fromId))
                
                self.timeUntilFree -= message.orderAgent.quantity * message.orderAgent.timeToComplete
        
        self.receivedMessages.clear()

 

        # Operate as normal
        if(self.isOperating):
            self.timeLeftOnOperation -= 1
            self.timeWorking += 1
            if(self.timeLeftOnOperation <= 0):

                self.isOperating = False
                # Add the operation to the completed pile
                self.order.completed = True
                self.order.completedDate = self.model.schedule.steps
                self.order.status = 'completed'
                
                for agent in self.model.schedule.agents:
                    if agent.unique_id == self.factoryId:
                        self.model.grid.move_agent(self.order,agent.completedOrderCoordinates)
                

                # LOOK AT RESCHEDULING REMAINING ORDERS
                if(self.schedulingType == 'SPT'):
                    # SPT => minimise the flow time
                    print('Machine {} - finished order {} - Carrying out SPT schedule'.format(self.unique_id,self.order.unique_id))
                    self.backLogOrders.sort(key=lambda x: x.timeToComplete * x.quantity, reverse=False)


                elif(self.schedulingType == 'LIFO'):
                    # # EDD = minimise the max lateness of a job
                    print('Machine {} - finished order {} - Carrying out LIFO schedule'.format(self.unique_id,self.order.unique_id))
                    print('Old backlog {}'.format(self.backLogOrders))
                    self.backLogOrders.sort(key=lambda x: x.dueDate, reverse=True)
                    print('Old backlog {}'.format(self.backLogOrders))
                
                elif(self.schedulingType == 'EDD'):
                    # # EDD = minimise the max lateness of a job
                    print('Machine {} - finished order {} - Carrying out EDD schedule'.format(self.unique_id,self.order.unique_id))
                    self.backLogOrders.sort(key=lambda x: x.dueDate, reverse=False)
                
                elif(self.schedulingType == 'Moores'):
                    # Moore's => minimise the number of late jobs
                    print('Machine {} - finished order {} - Carrying out Moores schedule'.format(self.unique_id,self.order.unique_id))
                    self.backLogOrders.sort(key=lambda x: x.dueDate, reverse=False)
                    removedOrderList = []
                    longestProcessingTimeOrder = {'time':0,'order':None}
                    notFinished = True
                    while notFinished:
                        hadToBreak = False
                        currentTime = self.model.schedule.steps
                        for order in self.backLogOrders:
                            currentTime += order.timeToComplete * order.quantity
                            # are any orders late, if not put th
                            if order.quantity * order.timeToComplete > longestProcessingTimeOrder['time']:
                                # this is accumulative
                                longestProcessingTimeOrder = {'time':order.quantity * order.timeToComplete,'order':order}
                            
                            if order.dueDate < currentTime:
                                # it's going to be late
                                hadToBreak = True
                                break
                        
                        if hadToBreak:
                            # Remove the the longest order from the backlog and add it to the removedOrderList
                            removedOrderList.append(longestProcessingTimeOrder['order'])
                            self.backLogOrders.remove(longestProcessingTimeOrder['order'])
                            longestProcessingTimeOrder = {'time':0,'order':None}

                        else:
                            notFinished = False

                    self.backLogOrders.extend(removedOrderList)
                
                

                elif(self.schedulingType == 'MDD'):
                    print('Machine {} - finished order {} - Carrying out MDD schedule'.format(self.unique_id,self.order.unique_id))
                    self.backLogOrders.sort(key=lambda x: x.dueDate, reverse=False)
                    MDDList = []
                    lowestMDD = {'time':None,'order':None}
                    currentTime = self.model.schedule.steps
                    while self.backLogOrders:
                        
                        for order in self.backLogOrders:
                            # Go through and check their MDDs
                            mdd = max(currentTime + order.quantity * order.timeToComplete,order.dueDate)
                            # Pick out the lowest and repeat
                            if lowestMDD['time'] is None or mdd < lowestMDD['time']:
                                lowestMDD = {'time':mdd,'order':order}
                        
                        # Remove the the shortest mm from the backlog and add it to the mddlist
                        # UPDATE THE CURRENT TIME
                        currentTime = lowestMDD['time']
                        MDDList.append(lowestMDD['order'])
                        self.backLogOrders.remove(lowestMDD['order'])
                        lowestMDD = {'time':None,'order':None}


                    self.backLogOrders.extend(MDDList)
                
                self.order = None
            
        else:
            self.timeFree += 1

        
        # Just recalculating the timeUntilFree
        backLogSize = self.model.schedule.steps
        backLogOrder = []
        if self.order is not None:
            backLogSize += self.timeLeftOnOperation

        for order in self.backLogOrders:
            backLogSize += order.quantity * order.timeToComplete
            backLogOrder.append(order.unique_id)


        if backLogSize > self.timeUntilFree:
            self.timeUntilFree = backLogSize

        
        # Just update this in case we don't have any orders
        if self.timeUntilFree < self.model.schedule.steps:
            self.timeUntilFree = self.model.schedule.steps



