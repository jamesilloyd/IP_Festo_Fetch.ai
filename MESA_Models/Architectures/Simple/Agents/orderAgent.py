
from mesa import Agent, Model

class OrderAgent(Agent):

    agentType = 'order'
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, operations):
        super().__init__(unique_id, model)
        self.operations = operations
        self.lookingForResource = True
        self.completed = False
        self.waitTime = 0


    def step(self):
        # Check if it needs 
        if(self.completed):
            pass
        else:
            if(self.lookingForResource):
                print('OrderAgent {0} - looking for resource'.format(self.unique_id))
                for agent in self.model.schedule.agents:
                    if(agent.agentType == 'scheduler'):
                        agent.orders.append(self)
                        self.model.grid.move_agent(self,agent.coordinates)

                self.lookingForResource = False
