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


def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N-i) for i,xi in enumerate(x)) / (N*sum(x))
    return (1 + (1/N) - 2*B)


class MoneyAgent(Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,moore = True, include_center = False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self,new_position)
        
    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth-= 1
        
        

class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters = {"Gini":compute_gini},
            agent_reporters= {"Wealth":"wealth"}
        )
    
    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()
        



'''HOW TO VISUALISE THE MODEL'''
def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                "Color": 'red' if agent.wealth == 0 else 'green',
                "Filled": "true",
                "Layer": 0 if agent.wealth == 0 else 1,
                "r": 0.5 if agent.wealth == 0 else 0.2}
    return portrayal
    
# chart = ChartModule([{"Label": "Gini",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')
# grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# server = ModularServer(MoneyModel,[grid,chart],'MONEY',{"N":100, 'width':10,'height':10})
# server.port = 8521
# server.launch()





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

model = MoneyModel(50,10,10)
for i in range(5000):
    model.step()
gini = model.datacollector.get_model_vars_dataframe()
gini.plot()
plt.show()

agent_wealth = model.datacollector.get_agent_vars_dataframe()
print(agent_wealth.head())

one_agent_wealth = agent_wealth.xs(14,level="AgentID")
one_agent_wealth.Wealth.plot()
plt.show()


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