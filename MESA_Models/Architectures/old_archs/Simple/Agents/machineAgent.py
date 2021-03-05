from mesa import Agent, Model
# import orderAgent

class MachineAgent(Agent):

    agentType = 'machine'


    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, typeOfOperation, timeToComplete, coordinates):
        super().__init__(unique_id, model)
        self.typeOfOperation = typeOfOperation
        self.timeToComplete = timeToComplete
        self.inProgress = False
        self.timeLeftOnOperation = 0
        self.coordinates = coordinates
        self.timeFree = 0
        self.timeWorking = 0
        # TODO: is this a safe way of initilaising the machine with an no order?
        self.order = None        

    def step(self):
        if(self.inProgress and self.order is not None):
            self.timeWorking += 1
            print('Machine {0} - time left on operation {1}'.format(self.unique_id, self.timeLeftOnOperation))
            self.timeLeftOnOperation -= 1
            if(self.timeLeftOnOperation == 0):
                print('Machine {0} - Order finished'.format(self.unique_id))
                self.order.lookingForResource = True
                self.order.operations.pop(0)
                self.inProgress = False
        else:
            self.timeFree += 1

