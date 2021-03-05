import sys
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
# from .agents.order_agent import OrderAgent
from .agents.machine_agent import MachineAgent
from .agents.product_agent import ProductAgent
from .agents.factory_agent import FactoryAgent
from .agents.federation_agent import FederationAgent

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
    [(10,25),['3D','CNC','IM']],
    [(25,9),['3D']],
    [(15,35),['3D','3D','CNC']],
    [(30,35),['IM','3D','CNC']],
    ]

class TrustBasedArchitecture(Model):

    def __init__(self, width, height, probability, operationTypes, distributed, model_reporters_dict = None):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.probability = probability
        self.operationTypes = operationTypes



        federationCentre = FederationAgent(1,self,(15,15))
        self.schedule.add(federationCentre)
        self.grid.place_agent(federationCentre,federationCentre.coordinates)

        for factory in factoriesAndCapabilities:
            factoryNumber = self.schedule.get_agent_count() + 1
            newFactoryAgent = FactoryAgent(factoryNumber,self,factory[0],distributed)
            self.schedule.add(newFactoryAgent)
            self.grid.place_agent(newFactoryAgent,newFactoryAgent.coordinates)

            incrementedYCoordinate = 2
            for capability in factory[1]:
                coordinates = (factory[0][0] + 3,factory[0][1] - incrementedYCoordinate)
                newMachine = MachineAgent(self.schedule.get_agent_count() + 1,self,capability,coordinates,factoryNumber)
                self.schedule.add(newMachine)
                self.grid.place_agent(newMachine,newMachine.coordinates)
                incrementedYCoordinate += 2
                
            

        if(model_reporters_dict is None):
            self.datacollector = DataCollector()
        else:
            self.datacollector = DataCollector(
                model_reporters = model_reporters_dict,
                # agent_reporters = {"Wait time":individualOrderWaitTime}
            )
    
    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()
        
        # self.newOrders()

    
            
            

