from mesa import Agent, Model
from .order_agent import OrderAgent
'''
	-this is the holarchy representing a manufacturing company
    -it manages product agents, schedule staff agents and resource agents 
    -it is responsible for creating order agents
'''
class FactoryAgent(Agent):
    
    agentType = 'factory'

    def __init__(self, unique_id, model, coordinates):
        super().__init__(unique_id, model)
        
        self.coordinates = coordinates

        self.receivedMessages = []
        self.messagesSent = 0
        self.scheduleStaffIds = []
        self.productAgentIds = []

    

    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])

    @property
    def newOrderCoordinates(self):
        changedX = self.coordinates[0] + 1
        return (changedX,self.coordinates[1])

    
    def step(self):
        # Check messages for a new order request then delegate with product agents and schedule staff agent to see if this factory can carry out the work
        for message in self.receivedMessages:
            if(message['messageType'] == 'order_request'):
                canCarryOutOrder = False 
                canFitIntoSchedule = False
                
                for agent in self.model.schedule.agents:
                    # Search for product agents in this factory
                    if agent.unique_id in self.productAgentIds:
                        # If the product agent type matches the order request we can carry out the order
                        if(message['productType'] == agent.productType):
                            print('Have capabilities to create order request')
                            canCarryOutOrder = True

                    # Search for schedule agents in this factory
                    if(agent.unique_id in self.scheduleStaffIds):
                        canFitIntoSchedule = agent.canFitIntoSchedule()
                        if(canFitIntoSchedule):
                            print('Can fit order request into schedule')
                            # Create a new product order into the system
                        else:
                            print('Cannot fit order request into schedule')
            
                if(canCarryOutOrder and canFitIntoSchedule):
                    # If both answer come back positive then create a new order agent into the factory with the customer requirements
                    orderNumber = self.model.schedule.get_agent_count() + 1
                    newOrderAgent = OrderAgent(orderNumber,self.model,message['productType'])
                    self.model.schedule.add(newOrderAgent)
                    self.model.grid.place_agent(newOrderAgent,self.newOrderCoordinates)

        
        self.receivedMessages.clear()

        