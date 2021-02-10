from mesa import Agent, Model
# import orderAgent

'''
Resource agent
	- Physical part within the manufacturing system
	- A human can be part of many holarchies (very desirable)
	- Contains data on
		○ Capabilities 
		○ Running tasks
        -Sub-resources 
        -log of activities
'''
class MachineAgent(Agent):

    agentType = 'machine'


    def __init__(self, unique_id, model, typeOfOperation, timeToComplete, coordinates):
        super().__init__(unique_id, model)
        self.typeOfOperation = typeOfOperation
        self.timeToComplete = timeToComplete
        self.coordinates = coordinates

        self.inProgress = False
        self.timeLeftOnOperation = 0
        self.timeFree = 0
        self.timeWorking = 0
        self.receivedMessages = []
        self.backLogOrders = []
        # TODO: is this a safe way of initilaising the machine with an no order?
        self.order = None    
        self.messagesSent = 0

        
        # Register the machine with the product agents and what their capability is
        for agent in self.model.schedule.agents:
            if(agent.agentType == 'product'):
                #TODO: This is the equivalent of sending a message (should we do that instead?)
                agent.machineIds.append({'unique_id':self.unique_id,'capability':self.typeOfOperation})
        


    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])


    def step(self):

        # If it has an order in the backlog, start working on it 
        if (self.backLogOrders and not self.inProgress):
            self.order = self.backLogOrders[0]
            self.order.inOperation = True
            # TODO: may want to save results instead
            self.backLogOrders.pop(0)
            self.model.grid.move_agent(self.order,self.coordinates)
            self.inProgress = True
            self.timeLeftOnOperation = self.timeToComplete

        # Operate as normal
        if(self.inProgress):
            self.timeLeftOnOperation -= 1
            self.timeWorking += 1
            if(self.timeLeftOnOperation == 0):
                self.inProgress = False
                # Add the operation to the completed pile
                self.order.completedOperations.append(self.order.operations[0])
                self.order.operations.pop(0)
                self.order.lookingForResource = True
        
         
        else:
            self.timeFree += 1

        #Check for messages from the scheduler and respond with status and backlog (OR scheduler does this through live lookup)


