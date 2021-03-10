from mesa import Agent, Model
from .order_agent import TrustOrderAgent, PROSAOrderAgent
import random
from .message import Message

'''
	-this is the holarchy representing a manufacturing company
    -it manages product agents, schedule staff agents and resource agents 
    -it is responsible for creating order agents
'''
class TrustFactoryAgent(Agent):
    
    agentType = 'factory'

    def __init__(self, unique_id, model, coordinates,distributed, newOrderProbability):
        super().__init__(unique_id, model)
        
        self.coordinates = coordinates

        self.capabilities = {}
        self.receivedMessages = []
        self.messagesSent = 0
        self.messagesReceived = 0
        
        self.scheduleStaffIds = []
        self.productAgentIds = []

        self.newOrdersBacklog = []

        self.newOrderProbability = newOrderProbability
        self.requestsBacklog = {}
        
        self.distributed = distributed

        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0
    

    @property
    def WIPBacklogCoordinates(self):
        changedX = self.coordinates[0] - 2
        return (changedX,self.coordinates[1])

    @property
    def WIPCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])

    @property
    def newOrderCoordinates(self):
        changedX = self.coordinates[0] - 2
        return (changedX,self.coordinates[1])

    @property
    def completedOrderCoordinates(self):
        changedY = self.coordinates[1] - 2
        return (self.coordinates[0],changedY)
    
    @property
    def unsuccessfulOrderCoordinates(self):
        changedY = self.coordinates[1] + 2
        return (self.coordinates[0],changedY)
    
    def step(self):
        messagesSent = 0
        messagesReceived = 0
        if self.model.schedule.steps > 1:
            self.newOrders()

        self.checkOrderBacklog()
        self.checkReceivedMessages(messagesReceived,messagesSent)
        
        if(self.distributed):
            self.checkRequests(messagesSent)
        

        if messagesSent > self.maxMessagesSent:
            self.maxMessagesSent = messagesSent
        if messagesReceived > self.maxMessagesReceived:
            self.maxMessagesReceived = messagesReceived
        
            


    def checkOrderBacklog(self):
        # Check backlog
        for agent in self.newOrdersBacklog:
            # If we have the capabilities we will carry it out (and a 20 % chance that we don't have capacity)
            capableMachineIds = self.capabilityCheck(agent)

            # Choose which resource to allocate it to
            if capableMachineIds:
                chosenMachineId = random.choice(capableMachineIds)
                
                print('Factory {} - Order {} can be done inhouse on Machine {}'.format(self.unique_id,agent.unique_id,chosenMachineId))
                for machineAgent in self.model.schedule.agents:
                    if machineAgent.unique_id == chosenMachineId:
                        machineAgent.backLogOrders.append(agent)
                        self.model.grid.move_agent(agent,machineAgent.backlogCoordinates)

            
            # If we don't have the capbailies we will outsource it
            elif(self.distributed):
                print('Factory {} - Order {} needs to be outsourced'.format(self.unique_id,agent.unique_id))
                self.requestsBacklog.update({agent.unique_id:{'agent':agent,'status':'needIds'}})
            else:
                print('Factory {} - Order {} cannot be completed'.format(self.unique_id,agent.unique_id))
                self.model.grid.move_agent(agent,self.unsuccessfulOrderCoordinates)
                agent.completed = True
                agent.successful = False
        
        self.newOrdersBacklog.clear()


    def checkRequests(self,messagesSent):
        # Check requests backlog
        for key in self.requestsBacklog.keys():
            backlogAgent = self.requestsBacklog[key]['agent']
            if self.requestsBacklog[key]['status'] == 'needIds':
                print('Factory {} - Asking Federator for ids for order {}'.format(self.unique_id,backlogAgent.unique_id))
                # Ask federator for company ids
                for agent in self.model.schedule.agents:
                    if agent.agentType == 'federator':
                        message = Message(self.unique_id,'idsRequest',capability=backlogAgent.productType,orderId=backlogAgent.unique_id)
                        agent.receivedMessages.append(message)
                        self.messagesSent += 1
                        messagesSent += 1
                
                self.requestsBacklog[key]['status'] = 'waitingForResponseFromFederator'


            elif self.requestsBacklog[key]['status'] == 'receivedOffers':
                
                if self.requestsBacklog[key]['timer'] == 0:
                    print('Factory {} - Choosing winning bid for order {}'.format(self.unique_id,backlogAgent.unique_id))

                    # If the offers list is empty then send the order to the bad pile
                    if not self.requestsBacklog[key]['offers']:
                        print('Factory {} - Recieved no viable offers for order {}'.format(self.unique_id,key))
                        self.requestsBacklog[key]['status'] = 'unsuccessful'
                        self.model.grid.move_agent(backlogAgent,self.unsuccessfulOrderCoordinates)
                        backlogAgent.completed = True
                        backlogAgent.successful = False
                        

                    else:
                        lowestBid = 101
                        factoryId = 0
                        
                        for offer in self.requestsBacklog[key]['offers']:
                            if offer['price'] < lowestBid:
                                lowestBid = offer['price']
                                factoryId = offer['factory']
                                machineId = offer['machine']
                        print('Factory {0} - Chosen factory {1} for order {2} at a bid of {3}'.format(self.unique_id,factoryId,key,lowestBid))
                        self.requestsBacklog[key]['status'] = 'successfullyOutsourced'

                        for agent in self.model.schedule.agents:
                            if agent.unique_id == machineId:
                                self.model.grid.move_agent(backlogAgent,agent.backlogCoordinates)
                                agent.backLogOrders.append(backlogAgent)
                                self.messagesSent += 1

                else:
                    self.requestsBacklog[key]['timer'] -= 1
                    print('Factory {} - Waiting to receive all bids -  {} steps'.format(self.unique_id, self.requestsBacklog[key]['timer']))
                    


    def newOrders(self):
        # Give a 20% probability that a new order will arrive into the system
        # Can only have orders that the company has resources for??? 
        number = random.randrange(self.newOrderProbability)
        if(number == 0):
            capabilities = []
            for key in self.capabilities.keys():
                capabilities.append(key)
            orderAgent = TrustOrderAgent(self.model.schedule.get_agent_count()+1,self.model,capabilities)
            self.model.schedule.add(orderAgent)
            self.model.grid.place_agent(orderAgent,self.newOrderCoordinates)
            self.newOrdersBacklog.append(orderAgent)
            print('Factory {} - New order {} received for {} of quantity {} with due date {}'.format(self.unique_id,orderAgent.unique_id,orderAgent.productType,orderAgent.quantity,orderAgent.dueDate))
    


    def checkReceivedMessages(self,messagesReceived,messagesSent):
        # check received messages
        for message in self.receivedMessages:
            self.messagesReceived += 1
            messagesReceived += 1
            if message.type == "idsResponse":
                # Check if the requestedIds are empty or not
                if(message.requestedIds):
                    # update hashmap of request backlog
                    print('Factory {} - received request ids for order {}'.format(self.unique_id,message.orderId))
                    self.requestsBacklog[message.orderId]['status'] = 'receivedIds'
                    self.requestsBacklog[message.orderId]['receivedIds'] = message.requestedIds
                    
                    # Find the order agent
                    orderAgent = self.requestsBacklog[message.orderId]['agent']
                    print('Factory {} - Sending resource requests for order {}'.format(self.unique_id,orderAgent.unique_id))
                    # Send message to those factory ids
                    for agent in self.model.schedule.agents:
                        if agent.unique_id in message.requestedIds and agent.unique_id != self.unique_id:
                            # TODO: feel uneasy adding the agent to the message payload, why aren't the orders doing the talking themselves?
                            message = Message(self.unique_id,'resourceRequest',orderId=orderAgent.unique_id,capability=orderAgent.productType,orderAgent=orderAgent)
                            agent.receivedMessages.append(message)
                            self.messagesSent += 1
                            messagesSent += 1
                

                else:
                    # There are no factories with this capability 
                    print('Factory {} - received no compatible ids for order {}'.format(self.unique_id,message.orderId))
                    self.requestsBacklog[message.orderId]['status'] = 'unsuccessful'
                    agent = self.requestsBacklog[message.orderId]['agent']
                    self.model.grid.move_agent(agent,self.unsuccessfulOrderCoordinates)
                    agent.completed = True
                    agent.successful = False

                

            elif message.type == "resourceRequest":
                print('Factory {} - received resource request for order {} from factory {}'.format(self.unique_id,message.orderId,message.fromId))
                # Check whether we can carry out the operation
                capableMachineIds = self.capabilityCheck(message.orderAgent)
                if capableMachineIds:
                    price = random.randrange(100)
                    chosenMachineId = random.choice(capableMachineIds)
                    print('Factory {} - can carry out order {} for €{} on machine {}'.format(self.unique_id,message.orderId,price,chosenMachineId))
                    returnMessage = Message(self.unique_id,'resourceRequestResponse',orderId=message.orderId,canCarryOutRequest=True,price=price,machineId=chosenMachineId)
                else:
                    print('Factory {} - cannot do order {}'.format(self.unique_id,message.orderId))
                    returnMessage = Message(self.unique_id,'resourceRequestResponse',orderId=message.orderId,canCarryOutRequest=False)


                for agent in self.model.schedule.agents:
                    if agent.unique_id == message.fromId:
                        agent.receivedMessages.append(returnMessage)
                        self.messagesSent +=1
                        messagesSent += 1
            
            elif message.type == 'resourceRequestResponse':
                # add it to the hashmap 
                if self.requestsBacklog[message.orderId]['status'] != 'receivedOffers':
                    self.requestsBacklog[message.orderId]['status'] = 'receivedOffers'
                    self.requestsBacklog[message.orderId]['offers'] = []
                    self.requestsBacklog[message.orderId]['timer'] = 2
                
                if message.canCarryOutRequest:
                    print('Factory {} - received offer for order {} from factory {}'.format(self.unique_id,message.orderId,message.fromId))
                    self.requestsBacklog[message.orderId]['offers'].append({'factory':message.fromId,'price':message.price,'machine':message.machineId})
            
            elif message.type == 'accounceCapabilitiesMachine':

                print('Factory {} - New capability {} - machine {}'.format(self.unique_id,message.capability,message.fromId))
                if message.capability in self.capabilities:
                    self.capabilities[message.capability]['ids'].append(message.fromId)
                else:
                    self.capabilities.update({message.capability:{'ids':[message.fromId]}})

                # Let the federator know
                for agent in self.model.schedule.agents:
                    if agent.agentType == 'federator':
                        capabilitiesMessage = Message(self.unique_id,'announceCapabiliesFactory',capabilities=self.capabilities.keys())
                        agent.receivedMessages.append(capabilitiesMessage)
                        messagesSent += 1
                        self.messagesSent +=1

        self.receivedMessages.clear()




    # TODO: this should probably be carried out by the machine ... depends on MES integration
    def capabilityCheck(self,agent):
        capableMachines = []
        if(agent.productType in self.capabilities):
            # Ask the resources if they can carry it out
            for machineAgent in self.model.schedule.agents:
                if machineAgent.unique_id in self.capabilities[agent.productType]['ids']:

                    if agent.dueDate - machineAgent.timeUntilFree > agent.timeToComplete * agent.quantity:
                        capableMachines.append(machineAgent.unique_id)
                        machineAgent.timeUntilFree += agent.timeToComplete * agent.quantity

        return capableMachines






class PROSAFactoryAgent(TrustFactoryAgent):

    '''This factory agent does not coordinate the order agent's activities
        instead it tells the order agent the earliest date it can be produced 
        and the order agent must negotiate with other parties'''

    agentType = 'factory'

    def __init__(self, unique_id, model, coordinates,distributed,newOrderProbability):
        super().__init__(unique_id, model,coordinates,distributed,newOrderProbability)
        


    def step(self):
        messagesSent = 0
        messagesReceived = 0
        if self.model.schedule.steps > 1:
            self.newOrders()

        self.checkOrderBacklog()
        self.checkReceivedMessages(messagesReceived,messagesSent)

        if messagesSent > self.maxMessagesSent:
            self.maxMessagesSent = messagesSent
        if messagesReceived > self.maxMessagesReceived:
            self.maxMessagesReceived = messagesReceived
        

    # DONE
    def checkOrderBacklog(self):
        # Check backlog
        for agent in self.newOrdersBacklog:
            # If we have the capabilities we will carry it out (and a 20 % chance that we don't have capacity)
            capableMachineIds = self.capabilityCheck(agent)

            # Choose which resource to allocate it to
            if capableMachineIds:
                chosenMachineId = random.choice(capableMachineIds)
                print('Factory {} - Order {} can be done inhouse on Machine {}'.format(self.unique_id,agent.unique_id,chosenMachineId))
                for machineAgent in self.model.schedule.agents:
                    if machineAgent.unique_id == chosenMachineId:
                        machineAgent.backLogOrders.append(agent)
                        self.model.grid.move_agent(agent,machineAgent.backlogCoordinates)

            
            # If we don't have the capbailies tell the order the earliest date
            elif(self.distributed):
                print('Factory {} - Order {} needs to be outsourced'.format(self.unique_id,agent.unique_id))
                newMessage = Message(self.unique_id,'findResources')
                agent.receivedMessages.append(newMessage)
                self.messagesSent += 1
                # Remove the agent from the backlog
                self.newOrdersBacklog.remove(agent)
            else:
                print('Factory {} - Order {} cannot be completed'.format(self.unique_id,agent.unique_id))
                self.model.grid.move_agent(agent,self.unsuccessfulOrderCoordinates)
                agent.completed = True
                agent.successful = False
        
        self.newOrdersBacklog.clear()



    # DONE
    def newOrders(self):
        # Give a 20% probability that a new order will arrive into the system
        # Can only have orders that the company has resources for??? 
        number = random.randrange(self.newOrderProbability)
        if(number == 0):
            capabilities = []
            for key in self.capabilities.keys():
                capabilities.append(key)
                
            orderAgent = PROSAOrderAgent(self.model.schedule.get_agent_count()+1,self.model,capabilities,self.unique_id)
            self.model.schedule.add(orderAgent)
            self.model.grid.place_agent(orderAgent,self.newOrderCoordinates)
            self.newOrdersBacklog.append(orderAgent)
            print('Factory {} - New order {} received for {} of quantity {} with due date {}'.format(self.unique_id,orderAgent.unique_id,orderAgent.productType,orderAgent.quantity,orderAgent.dueDate))
    

    # DONE
    def checkReceivedMessages(self,messagesReceived,messagesSent):
        # check received messages
        for message in self.receivedMessages:
            self.messagesReceived += 1
            messagesReceived +=1


            if message.type == "resourceRequest":
                print('Factory {} - received resource request for order {}'.format(self.unique_id,message.fromId))
                # Check whether we can carry out the operation
                capableMachineIds = self.capabilityCheck(message.orderAgent)
                if capableMachineIds:
                    price = random.randrange(100)
                    chosenMachineId = random.choice(capableMachineIds)
                    print('Factory {} - can carry out order {} for €{} on machine {}'.format(self.unique_id,message.fromId,price,chosenMachineId))
                    returnMessage = Message(self.unique_id,'resourceRequestResponse',canCarryOutRequest=True,price=price,machineId=chosenMachineId)
                else:
                    print('Factory {} - cannot do order {}'.format(self.unique_id,message.fromId))
                    returnMessage = Message(self.unique_id,'resourceRequestResponse',canCarryOutRequest=False)


                for agent in self.model.schedule.agents:
                    if agent.unique_id == message.fromId:
                        agent.receivedMessages.append(returnMessage)
                        self.messagesSent += 1 
                        messagesSent +=1
            
            elif message.type == 'accounceCapabilitiesMachine':

                print('Factory {} - New capability {} - machine {}'.format(self.unique_id,message.capability,message.fromId))
                if message.capability in self.capabilities:
                    self.capabilities[message.capability]['ids'].append(message.fromId)
                else:
                    self.capabilities.update({message.capability:{'ids':[message.fromId]}})

                # Let the federator know
                for agent in self.model.schedule.agents:
                    if agent.agentType == 'federator':
                        capabilitiesMessage = Message(self.unique_id,'announceCapabiliesFactory',capabilities=self.capabilities.keys())
                        agent.receivedMessages.append(capabilitiesMessage)
                        self.messagesSent += 1
                        messagesSent +=1

        self.receivedMessages.clear()

