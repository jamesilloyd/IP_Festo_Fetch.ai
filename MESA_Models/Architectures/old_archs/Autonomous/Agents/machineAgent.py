from mesa import Agent, Model
# import orderAgent

class MachineAgent(Agent):

    agentType = 'machine'


    def __init__(self, unique_id, model, typeOfOperation, timeToComplete, coordinates):
        super().__init__(unique_id, model)
        self.typeOfOperation = typeOfOperation
        self.timeToComplete = timeToComplete
        self.inProgress = False
        self.timeLeftOnOperation = 0
        self.coordinates = coordinates
        self.timeFree = 0
        self.timeWorking = 0
        self.receivedMessages = []
        self.backLogOrders = []
        # TODO: is this a safe way of initilaising the machine with an no order?
        self.order = None    
        self.messagesSent = 0

    @property
    def backlogCoordinates(self):

        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])


    def step(self):
        
        if (self.backLogOrders and not self.inProgress):
            self.order = self.backLogOrders[0]
            self.order.inOperation = True
            self.backLogOrders.pop(0)
            self.model.grid.move_agent(self.order,self.coordinates)
            self.inProgress = True
            self.timeLeftOnOperation = self.timeToComplete

        
        if(self.inProgress):
            self.timeLeftOnOperation -= 1
            self.timeWorking += 1
            if(self.timeLeftOnOperation == 0):
                self.inProgress = False
                self.order.operations.pop(0)
                self.order.receivedMessages.clear()
                self.order.lookingForResource = True
                self.order.checkingMessages = False
                
        else:
            self.timeFree += 1

        # Check messages
        for message in self.receivedMessages:
            answer = "n"
            if(message['operation'] == self.typeOfOperation):
                # Reply saying yes i can do it and calculate time based on backlog
                answer = "y"

            # send message to agent with that id
            for agent in self.model.schedule.agents:
                if agent.unique_id == message['id']:
                    newMessage ={'answer':answer,'id':self.unique_id}
                    
                    agent.receivedMessages.append(newMessage)
                    print('Machine {0} - message sent to order {1} - {2}'.format(self.unique_id,agent.unique_id,newMessage))
                    self.messagesSent += 1
            
        self.receivedMessages.clear()

        # if(self.inProgress and self.order is not None):
        #     self.timeWorking += 1
        #     print('Machine {0} - time left on operation {1}'.format(self.unique_id, self.timeLeftOnOperation))
        #     self.timeLeftOnOperation -= 1
        #     if(self.timeLeftOnOperation == 0):
        #         print('Machine {0} - Order finished'.format(self.unique_id))
        #         self.order.lookingForResource = True
        #         self.order.operations.pop(0)
        #         self.inProgress = False
        # else:
        #     self.timeFree += 1

