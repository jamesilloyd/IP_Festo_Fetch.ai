import random
from mesa import Agent, Model
from .message import Message
from .operations import operationDictionary


'''
	- Represents a task in the manufacturing system 
    - Could be customer order, make-to-stock, prototype order etc. 
    - Consider it a workpiece 
	- Ensure it is done on time and correctly
	
	- They negotiate with each other to compete for a resource
	- It is referred to only one product agent
	- Contains data on
		○ State of physical product
		○ Progress of the task
		○ Historical data on tasks
'''

class TrustOrderAgent(Agent):

    agentType = 'order'

    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model,facotryCapabilities,factoryId):
        super().__init__(unique_id, model)

        self.operations = []
        self.completedOperations = []
        self.productType = random.choice(facotryCapabilities)

        self.lookingForResource = True
        self.completed = False

        self.factoryId = factoryId

        self.receivedOffers = []

        self.status = 'new'


        self.successful = True
        self.waitTime = 0
        self.receivedMessages = []
        self.messagesSent = 0
        self.messagesReceived = 0
        self.inOperation = False
        self.receivedOperations = False
        
        self.negotiationTimer = 0

        # From data requests this seems to be the standard size of orders
        self.quantity = random.randrange(operationDictionary[self.productType]['usualQuantity'][0],operationDictionary[self.productType]['usualQuantity'][1])
        self.timeToComplete = random.randrange(operationDictionary[self.productType]['unitOperationTimes'][0],operationDictionary[self.productType]['unitOperationTimes'][1])
        self.dueDate = self.model.schedule.steps + random.randrange(self.timeToComplete ,self.timeToComplete + 5) * self.quantity
        self.latestStartDate = self.dueDate - self.timeToComplete

        self.completedDate = 0

        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0
    
    
    
    def step(self):
        messagesSent = 0
        messagesReceived = 0

        for message in self.receivedMessages:
            self.messagesReceived += 1
            messagesReceived += 1
            if message.type == 'findResources':
                # Initial factory cannot complete me so I need to find other ids
                print('Order {} - Asking Federator for ids'.format(self.unique_id,))
                # Ask federator for company ids
                for agent in self.model.schedule.agents:
                    if agent.agentType == 'federator':
                        message = Message(self.unique_id,'idsRequest',capability=self.productType,orderId=self.unique_id)
                        agent.receivedMessages.append(message)
                        self.messagesSent += 1
                        messagesSent += 1
                self.status = 'waitingForResponseFromFederator'
            
            elif message.type == "idsResponse":
                # Check if the requestedIds are empty or not
                receivedIds = []
                for factoryId in message.requestedIds:
                    if factoryId != self.factoryId:
                        receivedIds.append(factoryId)

                if(receivedIds):
                    print('Order {} - received request ids'.format(self.unique_id))
                    self.status = 'receivedIds'
                    # Send messages out to those ids
                    print('Order {} - Sending resource requests to {}'.format(self.unique_id,receivedIds))
                    for factoryAgent in self.model.schedule.agents:
                        if factoryAgent.unique_id in receivedIds:
                            # TODO: feel uneasy about dropping the object in the message
                            message = Message(self.unique_id,'resourceRequest',capability=self.productType,orderAgent=self)
                            factoryAgent.receivedMessages.append(message)
                            self.messagesSent += 1
                            messagesSent += 1
                    self.status = 'waitingForResponseFromFactories'

                else:
                    # There are no factories with this capability 
                    print('Order {} - received no compatible ids'.format(self.unique_id))
                    self.completed = True
                    self.successful = False
                    self.status = "Completed"
                    for agent in self.model.schedule.agents:
                        if agent.unique_id == self.factoryId:
                            self.model.grid.move_agent(self,agent.unsuccessfulOrderCoordinates)
                    
            
            elif message.type == 'resourceRequestResponse':
                # add it to the hashmap 
                if self.status != 'receivedOffers':
                    self.status = 'receivedOffers'
                    self.negotiationTimer = 2
                
                if message.canCarryOutRequest:
                    print('Order {} - received offer from factory {} on machine {}'.format(self.unique_id,message.fromId,message.machineId))
                    self.receivedOffers.append({'factory':message.fromId,'price':message.price,'machine':message.machineId})
                
        self.receivedMessages.clear()


        if self.status == 'receivedOffers':
            if self.negotiationTimer == 0:
                print('Order {} - Choosing winning bid'.format(self.unique_id))

                # If the offers list is empty then send the order to the bad pile
                if not self.receivedOffers:
                    print('Order {} - Recieved no viable offers'.format(self.unique_id))
                    self.status = 'Completed'
                    self.completed = True
                    self.successful = False
                    for agent in self.model.schedule.agents:
                        if agent.unique_id == self.factoryId:
                            self.model.grid.move_agent(self,agent.unsuccessfulOrderCoordinates)

                else:
                    lowestBid = None
                    factoryId = 0


                    listOfMachineIDs = []
                    for offer in self.receivedOffers:
                        listOfMachineIDs.append(offer['machine'])
                        if lowestBid is None or offer['price'] < lowestBid:
                            lowestBid = offer['price']
                            factoryId = offer['factory']
                            machineId = offer['machine']
                    print('Order {0} - Chosen factory {1} - machine {3} at a bid of €{2}'.format(self.unique_id,factoryId,lowestBid,machineId))
                    self.status = 'successfullyOutsourced'

                    for agent in self.model.schedule.agents:
                        if agent.unique_id == machineId:
                            self.model.grid.move_agent(self,agent.backlogCoordinates)
                            agent.backLogOrders.append(self)
                            self.messagesSent += 1
                            messagesSent += 1
                        # Need to let the other machines know they were unsuccessful so that they can readjust their timeTillFree
                        elif agent.unique_id in listOfMachineIDs:
                            unsuccessfulMessage = Message(self.unique_id,'unsuccessfulBid',orderAgent=self)
                            agent.receivedMessages.append(unsuccessfulMessage)

                    

            else:
                self.negotiationTimer -= 1
                print('Order {} - Waiting to receive all bids -  {} steps'.format(self.unique_id, self.negotiationTimer))
        
        if messagesSent > self.maxMessagesSent:
            self.maxMessagesSent = messagesSent
        if messagesReceived > self.maxMessagesReceived:
            self.maxMessagesReceived = messagesReceived
        
        if(self.inOperation or self.completed):
            # In operation or completed
            pass

        else:
            # Waiting for operation
            # print('ORDER {} WAITING {}'.format(self.unique_id,self.waitTime))
            self.waitTime += 1
                


        # Check if it needs to get it's operations
        # if(not self.receivedOperations):
        #     print('Order {0}, requesting operations'.format(self.unique_id))
        #     # Send message to the appropriate product agent asking for operations
        #     for agent in self.model.schedule.agents:
        #         if agent.agentType == 'product':
        #             if agent.productType == self.productType:
        #                 message = {'messageType':'request_operations','id':self.unique_id}
        #                 agent.receivedMessages.append(message)
        #                 self.model.grid.move_agent(self,agent.backlogCoordinates)


        # elif(not self.operations):
        #     # Order is completed 
        #     self.completed = True
        #     self.model.grid.move_agent(self,(0,0))
        
        # else:
        #     # Has received orders
        #     if(self.lookingForResource):
        #         # Increment variable
        #         self.waitTime += 1
        #         # Order contacts the broker 
        #         print('OrderAgent {0} - looking for resources'.format(self.unique_id))
                
        #         # Initialise variables
        #         timeTillStart = None
        #         chosenMachine = {'time':None,'machineAgent':None}

        #         # Take the first uncompleted order 
        #         # Find the associated machines, start working on it
        #         for agent in self.model.schedule.agents:
        #             if(agent.unique_id in self.operations[0]['machineIds']):
        #                 # Check how long it will be before the machine can work on us
        #                 timeTillStart = agent.timeLeftOnOperation + len(agent.backLogOrders) * agent.timeToComplete
        #                 # First viable order
        #                 if chosenMachine['time'] is None:
        #                     chosenMachine['machineAgent'] = agent
        #                     chosenMachine['time'] = timeTillStart

        #                 #  Best offer available
        #                 elif(timeTillStart < chosenMachine['time']):
        #                     chosenMachine['machineAgent'] = agent
        #                     chosenMachine['time'] = timeTillStart
                
        #         if(chosenMachine['machineAgent'] is not None):
        #             print('Order {0} - Found machine to move to {1}'.format(self.unique_id, chosenMachine['machineAgent'].unique_id))
        #             # If we have found a machine, append to it
        #             self.model.grid.move_agent(self,chosenMachine['machineAgent'].backlogCoordinates)
        #             chosenMachine['machineAgent'].backLogOrders.append(self)
        #             self.lookingForResource = False