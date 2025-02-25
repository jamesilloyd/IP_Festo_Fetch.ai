from mesa import Agent, Model
from .order_agent import OrderAgent
import random
from .message import Message
from .offer import Bid, Requirement


class FactoryAgent(Agent):
    
    agentType = 'factory'

    def __init__(self, unique_id, model, coordinates,distributed, newOrderProbability,splitSize = 1):
        super().__init__(unique_id, model)
        
        self.coordinates = coordinates
        
        self.capabilities = {}
        self.receivedMessages = []
        self.totalMessagesSent = 0
        self.totalMessegesReceived = 0

        self.splitSize = splitSize
        
        self.scheduleStaffIds = []
        self.productAgentIds = []

        self.newOrdersBacklog = []
        self.void = False

        self.newOrderProbability = newOrderProbability
    
        
        self.distributed = distributed

        self.maxMessagesReceived = 0
        self.maxMessagesSent = 0

        # TODO: calculate the time to deliver the product to the address (may not be necessary)
        self.logisticsTime = 16
    

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

    @property
    def dispatchOrderCoordinates(self):
        changedX = self.coordinates[0] + 2
        return (changedX,self.coordinates[1])
    
    def step(self):
        self.maxMessagesSent = 0
        self.maxMessagesReceived = 0
        if self.model.schedule.steps > 1 :
            self.newOrders()

        self.checkOrderBacklog()
        self.checkReceivedMessages()



    def checkOrderBacklog(self):
        # Check backlog
        for agent in self.newOrdersBacklog:
            # If we have the capabilities we will carry it out (and a 20 % chance that we don't have capacity)
            capableMachineIds = self.capabilityCheck(agent,inHouse=True)

            # TODO: just testing this

            # Choose which resource to allocate it to
            # TODO: we should compare the average in house score to the external score
            # # if capableMachineIds:
            #     chosenMachineDict = random.choice(capableMachineIds)
            #     chosenMachineId = chosenMachineDict['machineId']
            #     machineAgent = self.model.schedule._agents[chosenMachineId]
            #     price = machineAgent.hourlyRate * agent.unitOperationTime * agent.quantity * machineAgent.speedFactor
            #     print('Factory {} - Order {} can be done inhouse on machine {} for £{}'.format(self.unique_id,agent.unique_id,chosenMachineId,price))

            #     agent.winningPrice = price
            #     internalBid = Bid({'price':price,'completeTime':chosenMachineDict['completeTime'],'quantity':agent.quantity,'productType':agent.productType},self.unique_id,chosenMachineId)

            #     for requirement in agent.requirements:
            #             # Evaluate the score for each requirement Type
                    
            #             score = requirement.weightedScore(internalBid.entries[requirement.requirementName], 
            #                 internalBid.entries[requirement.requirementName], internalBid.entries[requirement.requirementName])
            #             print(
            #                 'Requirement {} - Score {}'.format(requirement.requirementName, score))
            #             if(score < 0):
            #                 # Broken hard constraint
            #                 internalBid.score = -1
            #                 break
            #             else:
            #                 internalBid.score += score
            
            #     agent.winningSatisfactionScore = internalBid.score
            #     machineAgent.backLogOrders.append(agent)
            #     agent.status = 'waitingInHouse'
            #     machineAgent.timeUntilFree += agent.quantity * agent.unitOperationTime * machineAgent.speedFactor
            #     self.model.grid.move_agent(agent,machineAgent.backlogCoordinates)
            
            # # If we don't have the capbailies tell the order the earliest date
            # elif(self.distributed):
            print('Factory {} - Order {} needs to be outsourced'.format(self.unique_id,agent.unique_id))
            newMessage = Message(self.unique_id,'findResources')
            agent.receivedMessages.append(newMessage)
            self.totalMessagesSent += 1
            # Remove the agent from the backlog
            self.newOrdersBacklog.remove(agent)
            # else:
            #     print('Factory {} - Order {} cannot be completed'.format(self.unique_id,agent.unique_id))
            #     self.model.grid.move_agent(agent,self.unsuccessfulOrderCoordinates)
            #     agent.completed = True
            #     agent.successful = False
            #     agent.status = 'unsuccessful'
        
        self.newOrdersBacklog.clear()

                    


    # TODO: just testing this
    def newOrders(self):
        pass
    #     # Give a probability that a new order will arrive into the system
    #     # Can only have orders that the company has resources for
    #     number = random.randrange(self.newOrderProbability)
    #     if(number == 0):
    #         capabilities = []
    #         for key in self.capabilities.keys():
    #             capabilities.append(key)
                
    #         orderAgent = OrderAgent(self.model.schedule.get_agent_count()+1,self.model,capabilities,self.unique_id,splitSize=self.splitSize)
    #         self.model.schedule.add(orderAgent)
    #         self.model.grid.place_agent(orderAgent,self.newOrderCoordinates)
    #         self.newOrdersBacklog.append(orderAgent)
    #         print('Factory {} - New order {} received for {} of quantity {} with due date {}'.format(self.unique_id,orderAgent.unique_id,orderAgent.productType,orderAgent.quantity,orderAgent.dueDate))
    


    # def checkReceivedMessages(self,messagesRece):
    def checkReceivedMessages(self):

        # check received messages
        for message in self.receivedMessages:
            self.totalMessegesReceived += 1
            self.maxMessagesReceived +=1

            if message.type == "resourceRequest":
                print('Factory {} - received resource request for order {}'.format(self.unique_id,message.fromId))
                
                # Check whether we can carry out the operation
                capableMachines = self.capabilityCheck(message.orderAgent)
                messages = []
                if capableMachines:
                    # Add all avaialable machines for negotiation
                    for machineDict in capableMachines:

                        bid = Bid({'price':machineDict['price'],'completeTime':machineDict['completeTime'],'quantity':message.orderAgent.quantity,'productType':message.orderAgent.productType},self.unique_id,machineDict['machineId'])

                        print('Factory {} - can carry out order {} for €{} on machine {} by time {}'.format(self.unique_id,message.fromId,bid.entries['price'],bid.machineId,bid.entries['completeTime']))
                        returnMessage = Message(self.unique_id,'bid',canCarryOutRequest=True,bid = bid)
                        
                        messages.append(returnMessage)
                else:
                    print('Factory {} - cannot do order {}'.format(self.unique_id,message.fromId))
                    returnMessage = Message(self.unique_id,'bid',canCarryOutRequest=False)
                    messages.append(returnMessage)

                agent = self.model.schedule._agents[message.fromId]
                for returnMessage in messages:
                    agent.receivedMessages.append(returnMessage)
                    self.totalMessagesSent += 1 
                    self.maxMessagesSent +=1
            
            elif message.type == 'accounceCapabilitiesMachine':

                print('Factory {} - New capability {} - machine {}'.format(self.unique_id,message.capability,message.fromId))
                if message.capability in self.capabilities:
                    self.capabilities[message.capability]['ids'].append(message.fromId)
                else:
                    self.capabilities.update({message.capability:{'ids':[message.fromId]}})

                # Let the SOEF know
                for agent in self.model.schedule.agents:
                    if agent.agentType == 'SOEF':
                        capabilitiesMessage = Message(self.unique_id,'announceCapabiliesFactory',capabilities=self.capabilities.keys())
                        agent.receivedMessages.append(capabilitiesMessage)
                        self.totalMessagesSent += 1
                        self.maxMessagesSent +=1
                        break

        self.receivedMessages.clear()


    def capabilityCheck(self,agent,inHouse = False):
        capableMachines = []
        if(agent.productType in self.capabilities):
            # Ask the resources if they can carry it out
            for machineid in self.capabilities[agent.productType]['ids']:
                machineAgent = self.model.schedule._agents[machineid]

                # TODO add in functionality that determines whether the order was rejected because the machine is waiting to hear back from another auction
                actualCompleteTime = agent.unitOperationTime * agent.quantity * machineAgent.speedFactor + machineAgent.backLogSize + self.logisticsTime
                
                completeTime = agent.unitOperationTime * agent.quantity * machineAgent.speedFactor + machineAgent.timeUntilFree
                
                if(inHouse):
                    print('Factory {} - Capability Check - Machien Agent {} - Capability {} - Time until free {} - Due date {} - Time to complete {} - Logistics time 0'.format(self.unique_id,machineAgent.unique_id,machineAgent.typeOfOperation,machineAgent.timeUntilFree,agent.dueDate,machineAgent.speedFactor *agent.quantity*agent.unitOperationTime))
                    
                else:
                    completeTime += self.logisticsTime
                    print('Factory {} - Capability Check - Machine Agent {} - Capability {} - Time until free {} - Due date {} - Time to complete {} - Logistics time {}'.format(self.unique_id,machineAgent.unique_id,machineAgent.typeOfOperation,machineAgent.timeUntilFree,agent.dueDate,machineAgent.speedFactor *agent.quantity*agent.unitOperationTime,self.logisticsTime))
                
                if completeTime < agent.dueDate:
                    capableMachines.append({'completeTime':completeTime,'machineId':machineAgent.unique_id,'price':machineAgent.hourlyRate * agent.quantity * agent.unitOperationTime * machineAgent.speedFactor})
                    if(not inHouse):
                        #We update this elsewhere if doing in house
                        machineAgent.timeUntilFree += agent.unitOperationTime * agent.quantity * machineAgent.speedFactor 
                elif actualCompleteTime < agent.dueDate:
                    print('**************ORDER REJECTED BECAUSE WE ARE WAITING OUT FOR ANOTHER BID**************')
                        

        return capableMachines





