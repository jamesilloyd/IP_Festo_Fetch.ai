from mesa import Agent, Model
from .order_agent import TrustOrderAgent
import random
from .message import Message

'''
	-this is the holarchy representing a manufacturing company
    -it manages product agents, schedule staff agents and resource agents 
    -it is responsible for creating order agents
'''
class TrustFactoryAgent(Agent):
    
    agentType = 'factory'

    def __init__(self, unique_id, model, coordinates,distributed, newOrderProbability,method = 'cheapest',splitSize = 1,):
        super().__init__(unique_id, model)
        
        self.coordinates = coordinates
        
        self.capabilities = {}
        self.receivedMessages = []
        self.messagesSent = 0
        self.messagesReceived = 0

        self.splitSize = splitSize
        
        self.scheduleStaffIds = []
        self.productAgentIds = []

        self.newOrdersBacklog = []
        self.void = False

        self.newOrderProbability = newOrderProbability
    
        
        self.distributed = distributed

        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0

        self.method = method
    

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
        if self.model.schedule.steps > 1 :
            self.newOrders()

        self.checkOrderBacklog()
        self.checkReceivedMessages(messagesReceived,messagesSent)

        if self.model.schedule.steps > 5:
            if messagesSent > self.maxMessagesSent:
                self.maxMessagesSent = messagesSent
            if messagesReceived > self.maxMessagesReceived:
                self.maxMessagesReceived = messagesReceived
        
            


    def checkOrderBacklog(self):
        # Check backlog
        for agent in self.newOrdersBacklog:
            # If we have the capabilities we will carry it out (and a 20 % chance that we don't have capacity)
            capableMachineIds = self.capabilityCheck(agent,inHouse=True)

            # Choose which resource to allocate it to
            if capableMachineIds:
                chosenMachineDict = random.choice(capableMachineIds)
                chosenMachineId = chosenMachineDict['machineId']
                print('Factory {} - Order {} can be done inhouse on Machine {}'.format(self.unique_id,agent.unique_id,chosenMachineId))
                for machineAgent in self.model.schedule.agents:
                    if machineAgent.unique_id == chosenMachineId:
                        machineAgent.backLogOrders.append(agent)
                        agent.status = 'waitingInHouse'
                        machineAgent.timeUntilFree += agent.quantity * agent.timeToComplete
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
                agent.status = 'unsuccessful'
        
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
                
            orderAgent = TrustOrderAgent(self.model.schedule.get_agent_count()+1,self.model,capabilities,self.unique_id,splitSize=self.splitSize,method=self.method)
            self.model.schedule.add(orderAgent)
            self.model.grid.place_agent(orderAgent,self.newOrderCoordinates)
            self.newOrdersBacklog.append(orderAgent)
            print('Factory {} - New order {} received for {} of quantity {} with due date {}'.format(self.unique_id,orderAgent.unique_id,orderAgent.productType,orderAgent.quantity,orderAgent.dueDate))
    


    def checkReceivedMessages(self,messagesReceived,messagesSent):
        # check received messages
        for message in self.receivedMessages:
            self.messagesReceived += 1
            messagesReceived +=1


            if message.type == "resourceRequest":
                print('Factory {} - received resource request for order {}'.format(self.unique_id,message.fromId))
                # Check whether we can carry out the operation
                capableMachines = self.capabilityCheck(message.orderAgent)
                messages = []
                if capableMachines:
                    # Add all avaialable machines for negotiation
                    for machineDict in capableMachines:
                        machineId = machineDict['machineId']
                        machinePrice = machineDict['price']
                        completeTime = machineDict['completeTime']
                        print('Factory {} - can carry out order {} for €{} on machine {} at time {}'.format(self.unique_id,message.fromId,machinePrice,machineId,completeTime))
                        returnMessage = Message(self.unique_id,'resourceRequestResponse',canCarryOutRequest=True,price=machinePrice,machineId=machineId,completeTime=completeTime)
                        
                        messages.append(returnMessage)
                else:
                    print('Factory {} - cannot do order {}'.format(self.unique_id,message.fromId))
                    returnMessage = Message(self.unique_id,'resourceRequestResponse',canCarryOutRequest=False)
                    messages.append(returnMessage)


                for agent in self.model.schedule.agents:
                    if agent.unique_id == message.fromId:
                        for returnMessage in messages:
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




    # TODO: this should probably be carried out by the machine ... depends on MES integration
    def capabilityCheck(self,agent,inHouse = False):
        capableMachines = []
        if(agent.productType in self.capabilities):
            # Ask the resources if they can carry it out
            for machineAgent in self.model.schedule.agents:
                if machineAgent.unique_id in self.capabilities[agent.productType]['ids']:

                    print('{} - {} - {}'.format(machineAgent.timeUntilFree,agent.dueDate,agent.timeToComplete * agent.quantity))

                    # TEST 4 - still make a bid even if the order will be completed after it's due date

                    completeTime = agent.timeToComplete*agent.quantity + machineAgent.timeUntilFree 

                    chosen = False

                    if completeTime > agent.dueDate and inHouse:
                        # if completeTime > agent.dueDate and inHouse:
                        pass
                    
                    elif completeTime > agent.dueDate + agent.timeToComplete * agent.quantity:
                        pass
                    else:
                        chosen = True
                        capableMachines.append({'completeTime':completeTime,'machineId':machineAgent.unique_id,'price':machineAgent.hourlyRate * agent.quantity * agent.timeToComplete})

                    if(not inHouse and chosen):
                        machineAgent.timeUntilFree += agent.timeToComplete * agent.quantity

        return capableMachines





