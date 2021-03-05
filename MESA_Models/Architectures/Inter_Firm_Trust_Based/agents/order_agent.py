
from mesa import Agent, Model


'''
	- Represents a task in the manufacturing system 
    - Could be customer order, make-to-stock, prototype order etc. 
    - Consider it a workpiece 
	- Ensure it is done on time and correctly
	
	- They negotiate with each other to compete for a resource
	- It is referred to only one product agent
	- Contains data on
		○ State of physical product
		○ Progress of the task
		○ Historical data on tasks
'''

class OrderAgent(Agent):

    agentType = 'order'

    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, productType,timeToComplete):
        super().__init__(unique_id, model)

        self.productType = productType

        self.operations = []
        self.completedOperations = []
        self.timeToComplete = timeToComplete

        self.lookingForResource = True
        self.completed = False
        self.successful = True
        self.waitTime = 0
        self.receivedMessages = []
        self.messagesSent = 0
        self.inOperation = False
        self.receivedOperations = False
    

    def step(self):
        
        
        # Check if it needs to get it's operations
        # if(not self.receivedOperations):
        #     print('Order {0}, requesting operations'.format(self.unique_id))
        #     # Send message to the appropriate product agent asking for operations
        #     for agent in self.model.schedule.agents:
        #         if agent.agentType == 'product':
        #             if agent.productType == self.productType:
        #                 message = {'messageType':'request_operations','id':self.unique_id}
        #                 agent.receivedMessages.append(message)
        #                 self.model.grid.move_agent(self,agent.backlogCoordinates)
                        

        # elif(not self.operations):
        #     # Order is completed 
        #     self.completed = True
        #     self.model.grid.move_agent(self,(0,0))
        
        # else:
        #     # Has received orders
        #     if(self.lookingForResource):
        #         # Increment variable
        #         self.waitTime += 1
        #         # Order contacts the broker 
        #         print('OrderAgent {0} - looking for resources'.format(self.unique_id))
                
        #         # Initialise variables
        #         timeTillStart = None
        #         chosenMachine = {'time':None,'machineAgent':None}

        #         # Take the first uncompleted order 
        #         # Find the associated machines, start working on it
        #         for agent in self.model.schedule.agents:
        #             if(agent.unique_id in self.operations[0]['machineIds']):
        #                 # Check how long it will be before the machine can work on us
        #                 timeTillStart = agent.timeLeftOnOperation + len(agent.backLogOrders) * agent.timeToComplete
        #                 # First viable order
        #                 if chosenMachine['time'] is None:
        #                     chosenMachine['machineAgent'] = agent
        #                     chosenMachine['time'] = timeTillStart

        #                 #  Best offer available
        #                 elif(timeTillStart < chosenMachine['time']):
        #                     chosenMachine['machineAgent'] = agent
        #                     chosenMachine['time'] = timeTillStart
                
        #         if(chosenMachine['machineAgent'] is not None):
        #             print('Order {0} - Found machine to move to {1}'.format(self.unique_id, chosenMachine['machineAgent'].unique_id))
        #             # If we have found a machine, append to it
        #             self.model.grid.move_agent(self,chosenMachine['machineAgent'].backlogCoordinates)
        #             chosenMachine['machineAgent'].backLogOrders.append(self)
        #             self.lookingForResource = False


        if(self.inOperation or self.completed):
            # In operation or completed
            pass

        else:
            # Waiting for operation
            self.waitTime += 1
                


               
