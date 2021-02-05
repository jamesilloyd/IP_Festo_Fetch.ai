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

        # Register the machine with a scheduler
        for agent in self.model.schedule.agents:
            if(agent.agentType == 'scheduler'):
                if(agent.typeOfOperation == self.typeOfOperation):
                    agent.machineIds.append(self.unique_id)
        

        

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


