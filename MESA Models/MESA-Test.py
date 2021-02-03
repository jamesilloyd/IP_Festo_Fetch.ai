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


# def compute_gini(model):
#     agent_wealths = [agent.wealth for agent in model.schedule.agents]
#     x = sorted(agent_wealths)
#     N = model.num_agents
#     B = sum(xi * (N-i) for i,xi in enumerate(x)) / (N*sum(x))
#     return (1 + (1/N) - 2*B)


class OrderAgent(Agent):

    agentType = 'order'
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.operations = ['CNC','3D','IM','3D','IM','3D','IM','CNC']
        self.lookingForResource = True
        self.completed = False


    def step(self):
        # Check if it needs 
        if(self.completed):
            pass
        else:
            if(self.lookingForResource):
                print('looking for resource')
                for agent in self.model.schedule.agents:
                    if(agent.unique_id  == 1):
                        agent.orders.append(self)
                        self.model.grid.move_agent(self,agent.coordinates)

                self.lookingForResource = False
            
        

        # self.move()
        # if self.wealth > 0:
        #     self.give_money()

    # def move(self):
    #     possible_steps = self.model.grid.get_neighborhood(
    #         self.pos,moore = True, include_center = False
    #     )
    #     new_position = self.random.choice(possible_steps)
    #     self.model.grid.move_agent(self,new_position)
        
    # def give_money(self):
    #     cellmates = self.model.grid.get_cell_list_contents([self.pos])
    #     if len(cellmates) > 1:
    #         other = self.random.choice(cellmates)
    #         other.wealth += 1
    #         self.wealth-= 1


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
        self.order = OrderAgent

    def step(self):
        if(self.inProgress):
            print(self.timeLeftOnOperation)
            self.timeLeftOnOperation -= 1
            if(self.timeLeftOnOperation == 0):
                print('Order finished')

                self.order.operations.pop(0)
                self.order.lookingForResource = True
                self.inProgress = False

                




class ScheduleAgent(Agent):
    
    agentType = 'scheduler'

    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, coordinates):
        super().__init__(unique_id, model)
        self.orders = []
        self.coordinates = coordinates

    def step(self):
        for nextAgent in self.orders:
            print('New agent found')
            if not nextAgent.operations:
                nextAgent.completed = True
                self.model.grid.move_agent(nextAgent,(0,0))
            else:
                for agent in self.model.schedule.agents:
                    if(agent.unique_id > 2):
                        if(agent.typeOfOperation == nextAgent.operations[0]):
                            print('Found matching machine')
                            # Move agent to this machine and start the operation
                            self.model.grid.move_agent(nextAgent,agent.coordinates)
                            agent.timeLeftOnOperation = agent.timeToComplete
                            agent.inProgress = True
                            agent.order = nextAgent
                            self.orders.clear()
                        


        

class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

    
        scheduleAgent = ScheduleAgent(1,self,(5,0))
        self.schedule.add(scheduleAgent)
        self.grid.place_agent(scheduleAgent,(5,0))

        orderAgent = OrderAgent(2,self)
        self.schedule.add(orderAgent)
        self.grid.place_agent(orderAgent,(0,5))

        
        machineAgent1 = MachineAgent(3,self,'CNC',4,(8,1))
        self.schedule.add(machineAgent1)
        self.grid.place_agent(machineAgent1,(8,1))

        machineAgent2 = MachineAgent(4,self,'3D',8,(8,4))
        self.schedule.add(machineAgent2)
        self.grid.place_agent(machineAgent2,(8,4))

        machineAgent3 = MachineAgent(5,self,'IM',7,(8,8))
        self.schedule.add(machineAgent3)
        self.grid.place_agent(machineAgent3,(8,8))


        # # Create agents
        # for i in range(3):
        #     a = MoneyAgent(i, self)
        #     self.schedule.add(a)
        #     # Add the agent to a random grid cell
        #     x = self.random.randrange(self.grid.width)
        #     y = self.random.randrange(self.grid.height)
        #     self.grid.place_agent(a, (x, y))

        # self.datacollector = DataCollector(
        #     model_reporters = {"Gini":compute_gini},
        #     agent_reporters= {"Wealth":"wealth"}
        # )
    
    def step(self):
        '''Advance the model by one step.'''
        # self.datacollector.collect(self)
        self.schedule.step()
        



'''HOW TO VISUALISE THE MODEL'''
def agent_portrayal(agent):
    if(agent.agentType == 'order'):
        portrayal = {"Shape": "circle",
                "Color": 'green' if agent.completed else 'blue',
                "Filled": "true",
                'text_color':'black',
                "Layer": 0,
                'text': str(agent.unique_id),
                "r": 0.3 }
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
    

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(MoneyModel,[grid],'DM',{'width':10,'height':10})
server.port = 8521
server.launch()


'''HOW TO RUN A BATCH'''
# fixed_params = {'width':10,'height':10}

# variable_params = {"N": range(10,500,10)}
# batch_run = BatchRunner(
#     MoneyModel,
#     variable_params,
#     fixed_params,
#     iterations=5,
#     max_steps=100,
#     model_reporters={"Gini": compute_gini}
# )

# batch_run.run_all()

# run_data = batch_run.get_model_vars_dataframe()
# run_data.head()
# plt.scatter(run_data.N,run_data.Gini)
# plt.show()

'''HOW TO SHOW THE DATA FROM DATACOLLECTOR'''

# model = MoneyModel(50,10,10)
# for i in range(100):
#     model.step()
# gini = model.datacollector.get_model_vars_dataframe()
# gini.plot()
# plt.show()

# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# print(agent_wealth.head())

# one_agent_wealth = agent_wealth.xs(14,level="AgentID")
# one_agent_wealth.Wealth.plot()
# plt.show()


'''USED FOR VISUALISING THE CELL CONTENTS IN A GRID'''
# agent_counts = np.zeros((model.grid.width,model.grid.height))
# for cell in model.grid.coord_iter():
#     cell_content, x, y = cell
#     agent_count = len(cell_content)
#     agent_counts[x][y] = agent_count

# plt.imshow(agent_counts,interpolation='nearest')
# plt.colorbar()
# plt.show()


# for i in range(20):
#     model.step()



# plt.hist(all_wealth, bins = range(max(all_wealth)+1))

# plt.show()