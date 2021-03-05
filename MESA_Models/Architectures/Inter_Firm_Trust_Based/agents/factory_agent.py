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

        self.receivedMessages = []
        self.messagesSent = 0
        self.scheduleStaffIds = []
        self.productAgentIds = []

        self.newOrdersBacklog = []
        self.requestsBacklog = {}
        self.WIPBacklog = []
        self.isOperating = False
        self.currentOperation = 'placeholder'
        
        self.distributed = distributed

        self.timeFree = 0
        self.timeWorking = 0


        for agent in self.model.schedule.agents:
            if agent.agentType == 'federator':
                agent.factoryIds.append(self.unique_id)
    

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
        changedX = self.coordinates[0] + 2
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
        self.newOrders()
        self.checkOrderBacklog()
        if(self.distributed):
            self.checkRequests()
            self.checkReceivedMessages()
        self.workThroughWIP()
        
            


    def checkOrderBacklog(self):
        # Check backlog
        for agent in self.newOrdersBacklog:
            # Random probability that we can or cannot work on the order
            number = random.randrange(3)
            if(number != 0):
                print('Factory {} - Order {} can be done inhouse'.format(self.unique_id,agent.unique_id))
                self.WIPBacklog.append(agent)
                self.model.grid.move_agent(agent,self.WIPBacklogCoordinates)
                
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
                        message = Message(self.unique_id,'idsRequest',capability='',orderId=backlogAgent.unique_id)
                        agent.receivedMessages.append(message)
                        self.messagesSent += 1
                
                self.requestsBacklog[key]['status'] = 'waitingForResponseFromFederator'

            elif self.requestsBacklog[key]['status'] == 'receivedIds':
                print('Factory {} - Sending resource requests for order {}'.format(self.unique_id,backlogAgent.unique_id))
                # Send message to those ids
                for agent in self.model.schedule.agents:
                    if agent.unique_id in self.requestsBacklog[key]['receivedIds'] and agent.unique_id != self.unique_id:
                        message = Message(self.unique_id,'resourceRequest',orderId=backlogAgent.unique_id,capability='')
                        agent.receivedMessages.append(message)
                        self.messagesSent += 1
                
                self.requestsBacklog[key]['status'] = 'waitingForResponseFromFactories'


            elif self.requestsBacklog[key]['status'] == 'receivedOffers':
                
                if self.requestsBacklog[key]['timer'] == 0:
                    print('Factory {} - Choosing winning bid for order {}'.format(self.unique_id,backlogAgent.unique_id))

                    # If the offers list is empty then send the order to the bad pile
                    if not self.requestsBacklog[key]['offers']:
                        print('Factory {} - recieved no viable offers for order {}'.format(self.unique_id,key))
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
                        print('Factory {} - chosen factory {} for order {} at a bid of {}'.format(self.unique_id,key,factoryId,key,lowestBid))
                        self.requestsBacklog[key]['status'] = 'successfullyOutsourced'

                        for agent in self.model.schedule.agents:
                            if agent.unique_id == factoryId:
                                self.model.grid.move_agent(backlogAgent,agent.WIPBacklogCoordinates)
                                agent.WIPBacklog.append(backlogAgent)
                                self.messagesSent += 1

                else:
                    self.requestsBacklog[key]['timer'] -= 1
                    print('Factory {} - Waiting to receive all bids -  {} steps'.format(self.unique_id, self.requestsBacklog[key]['timer']))
                    print(len(self.requestsBacklog[key]['offers']))
                    


    def newOrders(self):
        # Give a 20% probability that a new order will arrive into the syste
        number = random.randrange(5)
        if(number == 0):
            print('Factory {} - New order received'.format(self.unique_id))
            orderAgent = OrderAgent(self.model.schedule.get_agent_count()+1,self.model,'',5)
            self.model.schedule.add(orderAgent)
            self.model.grid.place_agent(orderAgent,self.newOrderCoordinates)
            self.newOrdersBacklog.append(orderAgent)
    
    def workThroughWIP(self):
        # TODO: get a machine to do this part
        if(self.isOperating):
            self.timeWorking += 1
            self.currentOperation.timeToComplete -= 1
            if(self.currentOperation.timeToComplete == 0):
                self.currentOperation.completed = True
                self.isOperating = False
                self.WIPBacklog.pop(0)
                self.model.grid.move_agent(self.currentOperation,self.completedOrderCoordinates)

        else:
            self.timeFree +=1
            if self.WIPBacklog:
                self.isOperating = True
                self.currentOperation = self.WIPBacklog[0]
                self.currentOperation.inOperation = True
                self.model.grid.move_agent(self.currentOperation,self.WIPCoordinates)


    def checkReceivedMessages(self):
    

        # check received messages
        for message in self.receivedMessages:
            if message.type == "idsResponse":
                # update hashmap of request backlog
                print('Factory {} - received request ids for order {}'.format(self.unique_id,message.orderId))
                self.requestsBacklog[message.orderId]['status'] = 'receivedIds'
                self.requestsBacklog[message.orderId]['receivedIds'] = message.requestedIds

                

            elif message.type == "resourceRequest":
                print('Factory {} - received resource request for order {} from factory {}'.format(self.unique_id,message.orderId,message.fromId))
                # Check whether we can carry out the operation
                number = random.randrange(5)
                if(number == 0):
                    price = random.randrange(100)
                    print('Factory {} - can carry out order {} for {} '.format(self.unique_id,message.orderId,price))
                    returnMessage = Message(self.unique_id,'resourceRequestResponse',orderId=message.orderId,canCarryOutRequest=True,price=price)
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
                    self.requestsBacklog[message.orderId]['offers'].append({'factory':message.fromId,'price':message.price})



        self.receivedMessages.clear()