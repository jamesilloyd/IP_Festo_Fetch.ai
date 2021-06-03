import random
from mesa import Agent, Model
from .message import Message, Bid
from .operations import operationDictionary
from .offer import Requirement


'''
Order agent
	- Represents a task in the manufacturing system 
    - Could be customer order, make-to-stock, prototype order etc. 
	- Ensure it is done on time and correctly
'''


class OrderAgent(Agent):

    agentType = 'order'

    def __init__(self, unique_id, model, facotryCapabilities, factoryId, requirements, splitSize=1):
        super().__init__(unique_id, model)

        self.operations = []
        self.completedOperations = []
        self.productType = random.choice(facotryCapabilities)

        self.createdDate = self.model.schedule.steps

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
        self.inOperation = False
        self.receivedOperations = False
        self.void = False

        self.outsourced = False

        self.negotiationTimer = 0

        self.logisticsTime = 16

        self.winningPrice = 0
        self.winningMachineType = ''

        # From data requests this seems to be the standard size of orders
        # TODO: need to initialise with the requirements and contraints
        self.quantity = random.randrange(
            operationDictionary[self.productType]['usualQuantity'][0], operationDictionary[self.productType]['usualQuantity'][1])

        # IS IT AN EASY OR COMPLEX PART?
        # In reality this would be calculated by the factory
        self.unitOperationTime = random.uniform(
            operationDictionary[self.productType]['unitOperationTimes'][0], operationDictionary[self.productType]['unitOperationTimes'][1])
        # TODO: this needs to be extended a bit more
        self.dueDate = self.model.schedule.steps + random.uniform(operationDictionary[self.productType]['unitOperationTimes'][1],operationDictionary[self.productType]['unitOperationTimes'][1]*1.2)* self.quantity + self.logisticsTime + 10  # Contingency for the time taken for the negotiation to finish
        print(self.quantity)
        print(self.dueDate)

        self.requirementType = requirements

        self.requirements = [
            Requirement('quantity', 'hard', 1, self.quantity),
            Requirement('productType', 'hard', 1, self.productType)
        ]

        if(requirements == 'cheap'):
            print('Order {} = cheap'.format(self.unique_id))

            self.requirements.extend(
                [Requirement('price', 'soft_cost', 1, 10000), Requirement(
                    'completeTime', 'soft_cost', 0, 1500)]
            )

        elif(requirements == 'asap'):
            print('Order {} = asap'.format(self.unique_id))
            self.requirements.extend(
                [Requirement('price', 'soft_cost', 0, 50000), Requirement(
                    'completeTime', 'soft_cost', 1, self.dueDate)]
            )


        self.completedDate = 0
        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0

    def step(self):
        if not self.void:
            self.maxMessagesSent = 0
            self.maxMessagesReceived = 0

            # Check messages
            for message in self.receivedMessages:
                self.totalMessagesReceived += 1
                self.maxMessagesReceived += 1
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

            if(self.status == 'dispatched'):
                if(self.logisticsTime <= 0):
                    self.completed = True
                    self.completedDate = self.model.schedule.steps
                    self.status = 'completed'
                    factoryAgent = self.model.schedule._agents[self.factoryId]
                    self.model.grid.move_agent(
                        self, factoryAgent.completedOrderCoordinates)
                else:
                    self.logisticsTime -= 1

            # Do nothing
            if(self.inOperation or self.completed):
                # In operation or completed
                pass
            else:
                # Waiting for operation
                # print('ORDER {} WAITING {} - {} - Due Date {} - Complete time {}'.format(self.unique_id,self.waitTime,self.status,self.dueDate,self.unitOperationTime * self.quantity))
                self.waitTime += 1

    def findResources(self, message):
        # Initial factory cannot complete me so I need to find other ids
        print('Order {} - Asking Federator for ids'.format(self.unique_id))
        # Ask federator for company ids

        for agent in self.model.schedule.agents:
            if agent.agentType == 'federator':
                message = Message(self.unique_id, 'idsRequest',
                                  capability=self.productType, orderId=self.unique_id)
                agent.receivedMessages.append(message)
                self.totalMessagesSent += 1
                self.maxMessagesSent += 1
                break
        self.status = 'waitingForResponseFromFederator'

    def sendProposalToFactories(self, message):
        # Check if the received factory Ids are empty or not
        for factoryId in message.requestedIds:
            if factoryId != self.factoryId:
                self.requestedIds.append(factoryId)

        if(self.requestedIds):
            print('Order {} - received request ids'.format(self.unique_id))
            self.status = 'receivedIds'
            # Send messages out to those ids
            print(
                'Order {} - Sending resource requests to {}'.format(self.unique_id, self.requestedIds))
            for id in self.requestedIds:
                factoryAgent = self.model.schedule._agents[id]
                # TODO: feel uneasy about dropping the object in the message
                message = Message(self.unique_id, 'resourceRequest',
                                  capability=self.productType, orderAgent=self)
                factoryAgent.receivedMessages.append(message)
                self.totalMessagesSent += 1
                self.maxMessagesSent += 1
            self.status = 'waitingForResponseFromFactories'
        else:
            # There are no factories with this capability
            print('Order {} - received no compatible ids'.format(self.unique_id))
            self.completed = True
            self.successful = False
            self.status = "Completed"
            factoryAgent = self.model.schedule._agents[self.factoryId]
            self.model.grid.move_agent(
                self, factoryAgent.unsuccessfulOrderCoordinates)

    def receivedBid(self, message):

        # add it to the hashmap
        if self.status != 'receivedOffers':
            self.status = 'receivedOffers'
            self.negotiationTimer = 2

        if message.canCarryOutRequest:
            bid = message.bid
            print('Order {} - received offer from factory {} on machine {} for £{} by {}'.format(
                self.unique_id, bid.factoryId, bid.machineId, bid.entries['price'], bid.entries['completeTime']))
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
                # TODO This is not implemented for order splitting!!!

                # Find a way to do this automatically
                allBidValues = {'price': [], 'completeTime': [],
                                'productType': [], 'quantity': []}
                # Add all the bids
                for bid in self.receivedOffers:
                    allBidValues['price'].append(bid.entries['price'])
                    allBidValues['completeTime'].append(
                        bid.entries['completeTime'])
                    allBidValues['productType'].append(
                        bid.entries['productType'])
                    allBidValues['quantity'].append(bid.entries['quantity'])

                for requirement in self.requirements:
                    print(requirement)

                for bid in self.receivedOffers:
                    for requirement in self.requirements:
                        # Evaluate the score for each requirement Type
                        score = requirement.weightedScore(bid.entries[requirement.requirementName], min(
                            allBidValues[requirement.requirementName]), max(allBidValues[requirement.requirementName]))
                        print(
                            'Requirement {} - Score {}'.format(requirement.requirementName, score))
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
                    self.outsourced = True
                    self.winningPrice = chosenOffer.entries['price']
                    chosenMachine = self.model.schedule._agents[chosenOffer.machineId]
                    print('Order {0} - Chosen factory {1} - machine {2} at a bid of €{3}'.format(
                        self.unique_id, chosenOffer.factoryId, chosenMachine.unique_id, chosenOffer.entries['price']))
                    if self.size == 1:
                        self.model.grid.move_agent(
                            self, chosenMachine.backlogCoordinates)
                        chosenMachine.backLogOrders.append(self)
                        self.totalMessagesSent += 1
                        self.maxMessagesSent += 1
                    else:
                        # Spawn new agents
                        # TODO: if you come back to this make sure to add in additional attributes (maybe theres a better way of doing this?)
                        newAgent = OrderAgent(self.model.schedule.get_agent_count(
                        )+1, self.model, ['CNC'], self.factoryId)
                        print('Order {} - creating new order {} to finish the job'.format(
                            self.unique_id, newAgent.unique_id))
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
                        newAgent.dueDate = self.dueDate
                        newAgent.outsourced = self.outsourced

                        self.model.schedule.add(newAgent)
                        self.model.grid.place_agent(
                            newAgent, chosenMachine.backlogCoordinates)
                        chosenMachine.backLogOrders.append(newAgent)
                        self.totalMessagesSent += 1
                        self.maxMessagesSent += 1

                    # Need to let the other machines know they were unsuccessful so that they can readjust their timeTillFree
                    for id in notChosenOffers:
                        machineAgent = self.model.schedule._agents[id]
                        unsuccessfulMessage = Message(
                            self.unique_id, 'unsuccessfulBid', orderAgent=self)
                        machineAgent.receivedMessages.append(
                            unsuccessfulMessage)
                        self.totalMessagesSent += 1
                        self.maxMessagesSent += 1

                    if self.size != 1:
                        print(
                            'Order {} - created sub agents, time for me to die'.format(self.unique_id))
                        self.model.grid.remove_agent(self)
                        self.void = True

        else:
            self.negotiationTimer -= 1
            print('Order {} - Waiting to receive all bids - {} hours left'.format(
                self.unique_id, self.negotiationTimer))

    def splitAndReproposeToFactories(self):
        # Set the attribute to false so it doesn't repeat
        self.canSplit = False
        print('Order {} - Recieved no viable offers - going to split production'.format(self.unique_id))
        # TODO: be careful here ****************************
        self.size = self.splitSize
        self.quantity = self.quantity / self.splitSize
        # We can split, so let's try sending those offers out again, but we need to be looking for double the amount nows
        print('Order {} - Sending resource requests to {}'.format(self.unique_id, self.requestedIds))

        for id in self.requestedIds:
            factoryAgent = self.model.schedule._agents[id]
            # TODO: feel uneasy about dropping the object in the message
            message = Message(self.unique_id, 'resourceRequest',
                              capability=self.productType, orderAgent=self)
            factoryAgent.receivedMessages.append(message)
            self.totalMessagesSent += 1
            self.maxMessagesSent += 1
        self.status = 'waitingForResponseFromFactories'

    def receivedNoViableOffers(self):
        print('Order {} - Recieved no viable offers - unsuccessful'.format(self.unique_id))
        self.size = 1
        self.status = 'Completed'
        self.completed = True
        self.successful = False
        factoryAgent = self.model.schedule._agents[self.factoryId]
        self.model.grid.move_agent(
            self, factoryAgent.unsuccessfulOrderCoordinates)
