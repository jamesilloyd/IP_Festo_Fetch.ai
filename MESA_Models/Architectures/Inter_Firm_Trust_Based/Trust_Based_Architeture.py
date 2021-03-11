import sys
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
# from .agents.order_agent import OrderAgent
from .agents.machine_agent import MachineAgent
from .agents.product_agent import ProductAgent
from .agents.factory_agent import TrustFactoryAgent
from .agents.federation_agent import TrustFederationAgent

'''
Trust-based resource sharing mechanism for distributed manufacturing
- agents represent companies 
    - they can either offer their resources or request resources from other companies
    - they can choose the best from incoming offers

-there is a federartion 
    -this represents a group of agents that can collaborate together
-federation centre
    - manages entries and exits to and from the federation
    - updates the list of federation members
    - calculates reputation values for each member 
- Task
	- Specific production process that has to be performed by the agents
	- Has resource types needed to perform its operations
	- Amount of required resources
'''

factoriesAndCapabilities = [
    [(25,25),['CNC','CNC','CNC']],
    [(10,9),['IM','IM']],
    [(10,25),['3D_SLS','CNC','IM']],
    [(25,9),['3D_FDM']],
    [(15,35),['3D_DMLS','3D_FDM','CNC']],
    [(30,35),['IM','3D_SLS','CNC']],
    ]


class TrustBasedArchitecture(Model):

    def __init__(self, width, height, distributed, model_reporters_dict = None, agent_reporters_dict = None,newOrderProbability = 10,quantity = 1,schedulingType = 'FIFO',splitSize = 1):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        
        federationCentre = TrustFederationAgent(1,self,(15,15))
        
        self.schedule.add(federationCentre)
        self.grid.place_agent(federationCentre,federationCentre.coordinates)


        while quantity != 0:
            quantity -= 1
            for factory in factoriesAndCapabilities:
                factoryNumber = self.schedule.get_agent_count() + 1
                
                newFactoryAgent = TrustFactoryAgent(factoryNumber,self,factory[0],distributed,newOrderProbability,splitSize = splitSize)
                
                self.schedule.add(newFactoryAgent)
                self.grid.place_agent(newFactoryAgent,newFactoryAgent.coordinates)

                incrementedYCoordinate = 2
                for capability in factory[1]:
                    coordinates = (factory[0][0] + 3,factory[0][1] - incrementedYCoordinate)
                    newMachine = MachineAgent(self.schedule.get_agent_count() + 1,self,capability,coordinates,factoryNumber,schedulingType)
                    self.schedule.add(newMachine)
                    self.grid.place_agent(newMachine,newMachine.coordinates)
                    incrementedYCoordinate += 2
                
            

        if(model_reporters_dict is None):
            self.datacollector = DataCollector()
        else:
            self.datacollector = DataCollector(
                model_reporters = model_reporters_dict,
                agent_reporters = agent_reporters_dict
            )
    
    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()
        
    
            
            

