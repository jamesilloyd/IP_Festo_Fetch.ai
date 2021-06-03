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

TEST 4
- prioritises bids based on effect on overal schedule
'''

# MES SHOULD 

class TrustOrderAgent(Agent):

    '''Some description here'''

    agentType = 'order'

    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model,facotryCapabilities,factoryId,splitSize = 1,method = 'cheapest'):
        super().__init__(unique_id, model)

        self.operations = []
        self.completedOperations = []
        self.productType = random.choice(facotryCapabilities)

        self.splitSize = splitSize

        if splitSize > 1:
            self.canSplit = True
        else:
            self.canSplit = False

        self.lookingForResource = True
        self.completed = False

        self.method = method

        self.factoryId = factoryId

        self.receivedOffers = []

        self.size = 1

        self.status = 'new'


        self.successful = True
        self.waitTime = 0
        self.receivedMessages = []
        self.requestedIds = []
        self.messagesSent = 0
        self.messagesReceived = 0
        self.inOperation = False
        self.receivedOperations = False
        self.void = False
        
        self.negotiationTimer = 0

        # From data requests this seems to be the standard size of orders
        self.quantity = random.randrange(operationDictionary[self.productType]['usualQuantity'][0],operationDictionary[self.productType]['usualQuantity'][1])
        self.timeToComplete = random.randrange(operationDictionary[self.productType]['unitOperationTimes'][0],operationDictionary[self.productType]['unitOperationTimes'][1])
        self.dueDate = self.model.schedule.steps + random.randrange(self.timeToComplete,int(self.timeToComplete*1.5) + 1) * self.quantity
        self.latestStartDate = self.dueDate - self.timeToComplete

        self.completedDate = 0

        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0
    
    
    
    def step(self):
        if not self.void:
            messagesSent = 0
            messagesReceived = 0

            for message in self.receivedMessages:
                self.messagesReceived += 1
                messagesReceived += 1
                if message.type == 'findResources':
                    # Initial factory cannot complete me so I need to find other ids
                    print('Order {} - Asking Federator for ids'.format(self.unique_id))
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
                    for factoryId in message.requestedIds:
                        if factoryId != self.factoryId:
                            self.requestedIds.append(factoryId)

                    if(self.requestedIds):
                        print('Order {} - received request ids'.format(self.unique_id))
                        self.status = 'receivedIds'
                        # Send messages out to those ids
                        print('Order {} - Sending resource requests to {}'.format(self.unique_id,self.requestedIds))
                        for factoryAgent in self.model.schedule.agents:
                            if factoryAgent.unique_id in self.requestedIds:
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
                        self.receivedOffers.append({'factory':message.fromId,'price':message.price,'machine':message.machineId,'completeTime':message.completeTime})
                    
            self.receivedMessages.clear()


            if self.status == 'receivedOffers':
                if self.negotiationTimer == 0:
                    print('Order {} - Choosing winning bid'.format(self.unique_id))

                    # If the offers list is empty then send the order to the bad pile
                    if not self.receivedOffers or len(self.receivedOffers) < self.size:
                        if self.canSplit:
                            # Set the attribute to false so it doesn't repeat
                            self.canSplit = False
                            print('Order {} - Recieved no viable offers - going to split production'.format(self.unique_id))
                            # TODO: be careful here ****************************
                            self.size = self.splitSize
                            self.quantity = self.quantity / self.splitSize
                            # We can split, so let's try sending those offers out again, but we need to be looking for double the amount nows
                            print('Order {} - Sending resource requests to {}'.format(self.unique_id,self.requestedIds))
                            for factoryAgent in self.model.schedule.agents:
                                if factoryAgent.unique_id in self.requestedIds:
                                    # TODO: feel uneasy about dropping the object in the message
                                    message = Message(self.unique_id,'resourceRequest',capability=self.productType,orderAgent=self)
                                    factoryAgent.receivedMessages.append(message)
                                    self.messagesSent += 1
                                    messagesSent += 1
                            self.status = 'waitingForResponseFromFactories'
                            

                        else:
                            print('Order {} - Recieved no viable offers - unsuccessful'.format(self.unique_id))
                            self.size = 1
                            self.status = 'Completed'
                            self.completed = True
                            self.successful = False
                            for agent in self.model.schedule.agents:
                                if agent.unique_id == self.factoryId:
                                    self.model.grid.move_agent(self,agent.unsuccessfulOrderCoordinates)

                    else:                    
                        # We have enough offers
                        # - Choose machine that can complete cheapest (as is)
                        chosenOffers = {}
                        notChosenOffers = {}
                        self.status = 'successfullyOutsourced'
                        if(self.method == 'cheapest'):
                            print('CHOOSING CHEAPEAST BID')
                            self.receivedOffers.sort(key=lambda x: x['price'],reverse=False)
                            for index,offer in enumerate(self.receivedOffers): 
                                if(index < self.size):
                                    chosenOffers.update({offer['machine']:offer})
                                else:
                                    notChosenOffers.update({offer['machine']:offer})

                        # - Choose machine that can complete first
                        elif(self.method == 'first'):
                            print('CHOOSING EARLIEST BID')
                            self.receivedOffers.sort(key=lambda x: x['completeTime'],reverse=False)
                            print(self.receivedOffers[0])
                            for index, offer in enumerate(self.receivedOffers):
                                if(index == 0):
                                    chosenOffers.update({offer['machine']:offer})
                                else:
                                    notChosenOffers.update({offer['machine']:offer})
                            
                        # - Choose machine that can complete closest to due date
                        elif(self.method == 'dueDate'):
                            # Evaluate which order is closest to the due date
                            # Add that to chosen offers
                            # Ignore other offers 
                            timeDifference = False 
                            bestOffer = {}
                            for index,offer in enumerate(self.receivedOffers):
                                print('CHOOSING BIDS: Due Date {} - CompleteTime {}'.format(self.dueDate,offer['completeTime']))
                                if not timeDifference:
                                    bestOffer = offer
                                    timeDifference = abs( self.dueDate - offer['completeTime'])
                                else:
                                    if(abs(self.dueDate - offer['completeTime']) < timeDifference):
                                        timeDifference = abs( self.dueDate - offer['completeTime'])
                                        bestOffer = offer
                            
                            for offer in self.receivedOffers:
                                if offer == bestOffer:
                                    chosenOffers.update({offer['machine']:offer})
                                else:
                                    notChosenOffers.update({offer['machine']:offer})

                            print('Chosen bid: {}'.format(bestOffer['completeTime']))


                                

                        for agent in self.model.schedule.agents:
                            if agent.unique_id in chosenOffers.keys():
                                print('Order {0} - Chosen factory {1} - machine {2} at a bid of €{3}'.format(self.unique_id,chosenOffers[agent.unique_id]['factory'],agent.unique_id,chosenOffers[agent.unique_id]['price']))
                                if self.size == 1:
                                    self.model.grid.move_agent(self,agent.backlogCoordinates)
                                    agent.backLogOrders.append(self)
                                    self.messagesSent += 1
                                    messagesSent += 1
                                else:
                                    # Spawn new agents
                                    newAgent = TrustOrderAgent(self.model.schedule.get_agent_count()+1,self.model,['CNC'],self.factoryId)
                                    print('Order {} - creating new order {} to finish the job'.format(self.unique_id,newAgent.unique_id))
                                    newAgent.status = self.status
                                    newAgent.productType = self.productType
                                    newAgent.lookingForResource = self.lookingForResource
                                    newAgent.completed = self.completed
                                    newAgent.size = self.size
                                    newAgent.successful = self.successful
                                    newAgent.waitTime = self.waitTime
                                    newAgent.requestedIds = self.requestedIds
                                    newAgent.messagesSent = self.messagesSent
                                    newAgent.messagesReceived = self.messagesReceived
                                    newAgent.quantity = self.quantity
                                    newAgent.timeToComplete = self.timeToComplete
                                    newAgent.dueDate = self.dueDate
                                    newAgent.latestStartDate = self.latestStartDate

                                    self.model.schedule.add(newAgent)
                                    self.model.grid.place_agent(newAgent,agent.backlogCoordinates)
                                    agent.backLogOrders.append(newAgent)
                                    self.messagesSent += 1
                                    messagesSent += 1

                            # Need to let the other machines know they were unsuccessful so that they can readjust their timeTillFree
                            elif agent.unique_id in notChosenOffers.keys():
                                unsuccessfulMessage = Message(self.unique_id,'unsuccessfulBid',orderAgent=self)
                                agent.receivedMessages.append(unsuccessfulMessage)
                                self.messagesSent += 1
                                messagesSent += 1
                        
                        if self.size != 1:
                            print('Order {} - created sub agents, time for me to die'.format(self.unique_id))
                            self.model.grid.remove_agent(self)
                            self.void = True
                            

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
                print('ORDER {} WAITING {} - {} - Due Date {} - Complete time {}'.format(self.unique_id,self.waitTime,self.status,self.dueDate,self.quantity*self.timeToComplete))
                self.waitTime += 1
                    