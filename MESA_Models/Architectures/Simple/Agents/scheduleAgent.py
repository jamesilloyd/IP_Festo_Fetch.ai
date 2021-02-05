from mesa import Agent, Model

class ScheduleAgent(Agent):
    
    agentType = 'scheduler'

    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, coordinates):
        super().__init__(unique_id, model)
        self.orders = []
        self.coordinates = coordinates

    def step(self):
        for nextAgent in self.orders:
            foundMachine = False
            print('Schedule Agent {0} - Order Agent {1} requesting resource'.format(self.unique_id, nextAgent.unique_id))
            if not nextAgent.operations:
                print('Schedule Agent {0} - Order Agent {1} is completed'.format(self.unique_id, nextAgent.unique_id))
                nextAgent.completed = True
                self.model.grid.move_agent(nextAgent,(0,0))
                self.orders.remove(nextAgent)
            else:
                print('Schedule Agent {0} - Order Agent {1} is looking for {2}'.format(self.unique_id, nextAgent.unique_id,nextAgent.operations[0]))
                for agent in self.model.schedule.agents:
                    if(agent.agentType == 'machine'and not foundMachine):
                        if(agent.typeOfOperation == nextAgent.operations[0]):
                            print('Schedule Agent {0} - Found matching Machine Agent {1} for Order Agent {2}'.format(self.unique_id,agent.unique_id,nextAgent.unique_id))
                            # Move agent to this machine and start the operation
                            if not agent.inProgress:
                                print('Schedule Agent {0} - Machine Agent {1} is free!'.format(self.unique_id,agent.unique_id))
                                self.model.grid.move_agent(nextAgent,agent.coordinates)
                                agent.timeLeftOnOperation = agent.timeToComplete
                                agent.inProgress = True
                                agent.order = nextAgent
                                self.orders.remove(nextAgent)
                                foundMachine = True
                            else:
                                print('Schedule Agent {0} - Machine Agent {1} is is busy, waiting till free'.format(self.unique_id,agent.unique_id))
                                nextAgent.waitTime += 1
                        