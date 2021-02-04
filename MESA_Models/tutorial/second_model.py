from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

import matplotlib.pyplot as plt 
import numpy as np
import random


showPrints = False

operationTypes = [
    'CNC','3D','IM'
]

def machine_utilisation(model):
    
    total_time_working = 0
    total_time_free = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'machine'):
            total_time_free += agent.timeFree
            total_time_working += agent.timeWorking

    print('TOTAL FREE TIME {0} - TOTAL WORKING TIME {1}'.format(total_time_free,total_time_working))
    if(total_time_free != 0 and total_time_working != 0):
        utilisation = total_time_working / (total_time_working + total_time_free)
    else:
        utilisation = 0
    
    return utilisation


class OrderAgent(Agent):

    agentType = 'order'
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, operations):
        super().__init__(unique_id, model)
        self.operations = operations
        self.lookingForResource = True
        self.completed = False


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
            
        

class MachineAgent(Agent):

    agentType = 'machine'
    order: OrderAgent
    
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

    def step(self):
        if(self.inProgress):
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
                        


        

class MyModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height, probability):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.probability = probability
        

        for i in range(6):
            operations = []
            # Choose random selection of operations
            for j in range(random.randrange(5)):
                operations.append(random.choice(operationTypes))
            
            orderAgent = OrderAgent(i,self,operations)
            self.schedule.add(orderAgent)
            self.grid.place_agent(orderAgent,(0,i))
        

        orderNumber = 6
        scheduleAgent = ScheduleAgent(orderNumber + 1,self,(5,0))
        self.schedule.add(scheduleAgent)
        self.grid.place_agent(scheduleAgent,(5,0))
        
        machineAgent1 = MachineAgent(orderNumber + 2,self,'CNC',4,(8,1))
        self.schedule.add(machineAgent1)
        self.grid.place_agent(machineAgent1,(8,1))

        machineAgent2 = MachineAgent(orderNumber + 3,self,'3D',8,(8,4))
        self.schedule.add(machineAgent2)
        self.grid.place_agent(machineAgent2,(8,4))

        machineAgent2 = MachineAgent(orderNumber + 4,self,'3D',8,(12,4))
        self.schedule.add(machineAgent2)
        self.grid.place_agent(machineAgent2,(12,4))

        machineAgent3 = MachineAgent(orderNumber + 5,self,'IM',7,(8,8))
        self.schedule.add(machineAgent3)
        self.grid.place_agent(machineAgent3,(8,8))

        machineAgent3 = MachineAgent(orderNumber + 6,self,'IM',7,(12,8))
        self.schedule.add(machineAgent3)
        self.grid.place_agent(machineAgent3,(12,8))


        # # Create agents
        # for i in range(3):
        #     a = MoneyAgent(i, self)
        #     self.schedule.add(a)
        #     # Add the agent to a random grid cell
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters = {"Utilisation":machine_utilisation},
            # agent_reporters = {"Wealth":"wealth"}
        )
    
    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()
        self.newOrders()

    def newOrders(self):
        # Give a 20% probability that a new order will arrive into the system
        number = random.randrange(self.probability)
        if(number == 0):
            operations = []
            # Choose random selection of operations
            for j in range(random.randrange(5)):
                operations.append(random.choice(operationTypes))
            orderAgent = OrderAgent(self.schedule.get_agent_count()+1,self,operations)
            self.schedule.add(orderAgent)
            self.grid.place_agent(orderAgent,(0,19))

        


'''HOW TO VISUALISE THE MODEL'''
def agent_portrayal(agent):
    if(agent.agentType == 'order'):
        portrayal = {"Shape": "circle",
                "Color": 'green' if agent.completed else 'blue',
                "Filled": "true",
                'text_color':'white',
                "Layer": 0,
                'text': str(agent.unique_id),
                "r": 0.4}
    elif(agent.agentType == 'machine'):
        portrayal = {"Shape": "circle",
                "Color": 'green',
                "Filled": "true",
                'text': agent.typeOfOperation,
                'text_color':'black',
                "Layer": 0,
                "r": 0.5 }
    elif(agent.agentType == 'scheduler'):
        portrayal = {"Shape": "circle",
                "Color": 'red',
                "Filled": "true",
                'text': 'Scheduler',
                'text_color':'black',
                "Layer": 0,
                "r": 0.5 }
    
    return portrayal
    

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
chart = ChartModule([{'Label':'Utilisation',"Color":'Black'}],data_collector_name='datacollector')
server = ModularServer(MyModel,[grid,chart],'DM',{'width':20,'height':20,'probability':5})
server.port = 8521
server.launch()


# fixed_params = {'width':50,'height':50}
# variable_params = {"probability": range(1,50,1)}
# batch_run = BatchRunner(
#     MyModel,
#     variable_params,
#     fixed_params,
#     iterations=5,
#     max_steps=300,
#     model_reporters={"Utilisation": machine_utilisation}
# )

# batch_run.run_all()

# run_data = batch_run.get_model_vars_dataframe()

# print(run_data)
# run_data.head()
# plt.scatter(run_data.probability,run_data.Utilisation)
# plt.show()
