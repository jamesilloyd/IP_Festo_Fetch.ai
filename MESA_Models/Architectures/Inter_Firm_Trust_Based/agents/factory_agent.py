from mesa import Agent, Model
from .order_agent import OrderAgent
import random
from .message import Message

'''
	-this is the holarchy representing a manufacturing company
    -it manages product agents, schedule staff agents and resource agents 
    -it is responsible for creating order agents
'''
class FactoryAgent(Agent):
    
    agentType = 'factory'

    def __init__(self, unique_id, model, coordinates,distributed):
        super().__init__(unique_id, model)
        
        self.coordinates = coordinates

        self.capabilities = {}
        self.receivedMessages = []
        self.messagesSent = 0
        
        self.scheduleStaffIds = []
        self.productAgentIds = []

        self.newOrdersBacklog = []
        self.requestsBacklog = {}
        
        self.distributed = distributed
    

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
        print(self.model.schedule.steps)
        if self.model.schedule.steps > 1:
            self.newOrders()

        self.checkOrderBacklog()
        if(self.distributed):
            self.checkRequests()
        self.checkReceivedMessages()
        # self.workThroughWIP()
        
            


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


    def checkRequests(self):

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
                
                self.requestsBacklog[key]['status'] = 'waitingForResponseFromFederator'

            elif self.requestsBacklog[key]['status'] == 'receivedIds':
                print('Factory {} - Sending resource requests for order {}'.format(self.unique_id,backlogAgent.unique_id))
                # Send message to those ids
                for agent in self.model.schedule.agents:
                    if agent.unique_id in self.requestsBacklog[key]['receivedIds'] and agent.unique_id != self.unique_id:
                        # TODO: feel uneasy adding the agent to the message payload, why aren't the orders doing the talking themselves?
                        message = Message(self.unique_id,'resourceRequest',orderId=backlogAgent.unique_id,capability=backlogAgent.productType,orderAgent=backlogAgent)
                        agent.receivedMessages.append(message)
                        self.messagesSent += 1
                
                self.requestsBacklog[key]['status'] = 'waitingForResponseFromFactories'


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
        number = random.randrange(5)
        if(number == 0):
            capabilities = []
            for key in self.capabilities.keys():
                capabilities.append(key)
            orderAgent = OrderAgent(self.model.schedule.get_agent_count()+1,self.model,random.randrange(5,10),capabilities)
            self.model.schedule.add(orderAgent)
            self.model.grid.place_agent(orderAgent,self.newOrderCoordinates)
            self.newOrdersBacklog.append(orderAgent)
            print('Factory {} - New order received for {}'.format(self.unique_id,orderAgent.productType))
    


    def checkReceivedMessages(self):
        # check received messages
        for message in self.receivedMessages:
            if message.type == "idsResponse":
                # Check fi the requestedIds are empty or not
                if(message.requestedIds):
                    # update hashmap of request backlog
                    print('Factory {} - received request ids for order {}'.format(self.unique_id,message.orderId))
                    self.requestsBacklog[message.orderId]['status'] = 'receivedIds'
                    self.requestsBacklog[message.orderId]['receivedIds'] = message.requestedIds
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

        self.receivedMessages.clear()




    def capabilityCheck(self,agent):
        capableMachines = []
        if(agent.productType in self.capabilities):
            # Ask the resources if they can carry it out
            for machineAgent in self.model.schedule.agents:
                if machineAgent.unique_id in self.capabilities[agent.productType]['ids']:

                    if machineAgent.unique_id == 3:
                        print('TIME UNTIL NEXT FREE {}'.format(machineAgent.timeUntilFree))
                        print('ORDER DUE DATE {}'.format(agent.dueDate))
                        print('TIME TO COMPLETE ORDER {}'.format(agent.timeToComplete))
                    if agent.dueDate - machineAgent.timeUntilFree > agent.timeToComplete:
                        capableMachines.append(machineAgent.unique_id)
                        machineAgent.timeUntilFree += agent.timeToComplete
                        if machineAgent.unique_id == 3:
                            print('CAN CARRY OUT ORDER')
                            print('NEW TIME UNTIL NEXT FREE {}'.format(machineAgent.timeUntilFree))



        return capableMachines