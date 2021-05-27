import random
from mesa import Agent, Model
from .message import Message,Bid
from .operations import operationDictionary
from .offer import Requirement


'''
	- Represents a task in the manufacturing system 
    - Could be customer order, make-to-stock, prototype order etc. 
	- Ensure it is done on time and correctly
'''

class OrderAgent(Agent):

    '''Some description here'''

    agentType = 'order'

    def __init__(self, unique_id, model,facotryCapabilities,factoryId,splitSize = 1):
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

        self.factoryId = factoryId
        self.receivedOffers = []

        self.size = 1

        self.status = 'new'


        self.successful = True
        self.waitTime = 0
        self.receivedMessages = []
        self.requestedIds = []
        self.totalMessagesSent = 0
        self.totalMessagesReceived = 0
        self.messagesSent = 0
        self.messagesReceived = 0
        self.inOperation = False
        self.receivedOperations = False
        self.void = False
        
        self.negotiationTimer = 0

        # From data requests this seems to be the standard size of orders
        # TODO: need to initialise with the requirements and contraints
        self.quantity = random.randrange(operationDictionary[self.productType]['usualQuantity'][0],operationDictionary[self.productType]['usualQuantity'][1])
        # TODO: this metric needs to be calculated by the factory 
        self.timeToComplete = random.randrange(operationDictionary[self.productType]['unitOperationTimes'][0],operationDictionary[self.productType]['unitOperationTimes'][1])
        # TODO: this needs to be extended a bit more
        self.dueDate = self.model.schedule.steps + random.randrange(self.timeToComplete,int(self.timeToComplete*1.5) + 1) * self.quantity + 10 #Contingency
        self.latestStartDate = self.dueDate - self.timeToComplete

        # TODO: finish this off
        self.requirements = [
            Requirement('price','soft_cost',0.7,20000),
            Requirement('completeTime','soft_cost',0.2,self.dueDate),
            Requirement('quantity','hard',1,self.quantity),
            Requirement('productType','hard',1,self.productType)
        ]
 
        self.completedDate = 0
        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0
    
    
    
    def step(self):
        if not self.void:
            self.messagesSent = 0
            self.messagesReceived = 0

            # Check messages
            for message in self.receivedMessages:
                self.totalMessagesReceived += 1
                self.messagesReceived += 1
                if message.type == 'findResources':
                    self.findResources(message)
                    
                elif message.type == "idsResponse":
                    self.sendProposalToFactories(message)
                
                elif message.type == 'bid':
                    self.receivedBid(message)

            self.receivedMessages.clear()

            # Carry out action depending on current status
            if self.status == 'receivedOffers':

                self.matchmakingProcess()

                
            # Check if the number of messages sent / received in this round is the largest yet
            if self.messagesSent > self.maxMessagesSent:
                self.maxMessagesSent = self.messagesSent
            if self.messagesReceived > self.maxMessagesReceived:
                self.maxMessagesReceived = self.messagesReceived
            
            # Do nothing
            if(self.inOperation or self.completed):
                # In operation or completed
                pass
            else:
                # Waiting for operation
                # print('ORDER {} WAITING {} - {} - Due Date {} - Complete time {}'.format(self.unique_id,self.waitTime,self.status,self.dueDate,self.quantity*self.timeToComplete))
                self.waitTime += 1



    def findResources(self,message):
    # Initial factory cannot complete me so I need to find other ids
        print('Order {} - Asking Federator for ids'.format(self.unique_id))
        # Ask federator for company ids
        for agent in self.model.schedule.agents:
            if agent.agentType == 'federator':
                message = Message(self.unique_id,'idsRequest',capability=self.productType,orderId=self.unique_id)
                agent.receivedMessages.append(message)
                self.totalMessagesSent += 1
                self.messagesSent += 1
        self.status = 'waitingForResponseFromFederator'

    def sendProposalToFactories(self,message):
    # Check if the received factory Ids are empty or not
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
                    self.totalMessagesSent += 1
                    self.messagesSent += 1
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

    
    def receivedBid(self,message):

        # add it to the hashmap 
        if self.status != 'receivedOffers':
            self.status = 'receivedOffers'
            self.negotiationTimer = 2
        
        if message.canCarryOutRequest:
            bid = message.bid
            print('Order {} - received offer from factory {} on machine {}'.format(self.unique_id,bid.factoryId,bid.machineId))
            print(bid)
            self.receivedOffers.append(bid)

    def matchmakingProcess(self):
        if self.negotiationTimer == 0:
            print('Order {} - Choosing winning bid'.format(self.unique_id))

            # If the offers list is empty then send the order to the unsuccessful pile
            if not self.receivedOffers or len(self.receivedOffers) < self.size:
                if self.canSplit:
                    self.splitAndReproposeToFactories()
                    
                else:
                    self.receivedNoViableOffers()

            else:            
                # We have enough offers
                # - Choose machine that can complete cheapest (as is)
                #TODO This is not implemented for order splitting
                
                # Find a way to do this automatically
                allBidValues = {'price':[],'completeTime':[],'productType':[],'quantity':[]}
                # Add all the bids 
                for bid in self.receivedOffers:
                    allBidValues['price'].append(bid.entries['price'])
                    allBidValues['completeTime'].append(bid.entries['completeTime'])
                    allBidValues['productType'].append(bid.entries['productType'])
                    allBidValues['quantity'].append(bid.entries['quantity'])


                for requirement in self.requirements:
                    print(requirement)
                

                for bid in self.receivedOffers:
                    for requirement in self.requirements:
                         # Evaluate the score for each requirement Type 
                        score = requirement.weightedScore(bid.entries[requirement.requirementName],min(allBidValues[requirement.requirementName]),max(allBidValues[requirement.requirementName]))
                        print('Requirement {} - Score {}'.format(requirement.requirementName,score))
                        if(score < 0):
                            # Broken hard constraint
                            bid.score = -1
                            break
                        else:
                            bid.score += score
                    print(bid)
            
                

                # Check if any of the bids are positive
                chosenOffer = None
                notChosenOffers = []
                bestScore = 0
                foundWinningBid = False
                for bid in self.receivedOffers:
                    if bid.score > bestScore:
                        bestScore = bid.score
                        if(foundWinningBid):
                            # Remove the current offer
                            notChosenOffers.append(chosenOffer.machineId)
                            chosenOffer = bid
                        else:
                            foundWinningBid = True
                            chosenOffer = bid
                    else:
                        notChosenOffers.append(bid.machineId)


                if(not foundWinningBid):
                    self.receivedNoViableOffers()
                
                else:
                    self.status = 'successfullyOutsourced'


                    for agent in self.model.schedule.agents:
                        if agent.unique_id == chosenOffer.machineId:
                            print('Order {0} - Chosen factory {1} - machine {2} at a bid of €{3}'.format(self.unique_id,chosenOffer.factoryId,agent.unique_id,chosenOffer.entries['price']))
                            if self.size == 1:
                                self.model.grid.move_agent(self,agent.backlogCoordinates)
                                agent.backLogOrders.append(self)
                                self.totalMessagesSent += 1
                                self.messagesSent += 1
                            else:
                                # Spawn new agents
                                newAgent = OrderAgent(self.model.schedule.get_agent_count()+1,self.model,['CNC'],self.factoryId)
                                print('Order {} - creating new order {} to finish the job'.format(self.unique_id,newAgent.unique_id))
                                newAgent.status = self.status
                                newAgent.productType = self.productType
                                newAgent.lookingForResource = self.lookingForResource
                                newAgent.completed = self.completed
                                newAgent.size = self.size
                                newAgent.successful = self.successful
                                newAgent.waitTime = self.waitTime
                                newAgent.requestedIds = self.requestedIds
                                newAgent.totalMessagesSent = self.totalMessagesSent
                                newAgent.totalMessagesReceived = self.totalMessagesReceived
                                newAgent.quantity = self.quantity
                                newAgent.timeToComplete = self.timeToComplete
                                newAgent.dueDate = self.dueDate
                                newAgent.latestStartDate = self.latestStartDate

                                self.model.schedule.add(newAgent)
                                self.model.grid.place_agent(newAgent,agent.backlogCoordinates)
                                agent.backLogOrders.append(newAgent)
                                self.totalMessagesSent += 1
                                self.messagesSent += 1

                        # Need to let the other machines know they were unsuccessful so that they can readjust their timeTillFree
                        elif agent.unique_id in notChosenOffers:
                            unsuccessfulMessage = Message(self.unique_id,'unsuccessfulBid',orderAgent=self)
                            agent.receivedMessages.append(unsuccessfulMessage)
                            self.totalMessagesSent += 1
                            self.messagesSent += 1
                    
                    if self.size != 1:
                        print('Order {} - created sub agents, time for me to die'.format(self.unique_id))
                        self.model.grid.remove_agent(self)
                        self.void = True
                    

        else:
            self.negotiationTimer -= 1
            print('Order {} - Waiting to receive all bids -  {} steps'.format(self.unique_id, self.negotiationTimer))

    
    
    def splitAndReproposeToFactories(self):
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
                self.totalMessagesSent += 1
                self.messagesSent += 1
        self.status = 'waitingForResponseFromFactories'



    def receivedNoViableOffers(self):
        print('Order {} - Recieved no viable offers - unsuccessful'.format(self.unique_id))
        self.size = 1
        self.status = 'Completed'
        self.completed = True
        self.successful = False
        for agent in self.model.schedule.agents:
            if agent.unique_id == self.factoryId:
                self.model.grid.move_agent(self,agent.unsuccessfulOrderCoordinates)