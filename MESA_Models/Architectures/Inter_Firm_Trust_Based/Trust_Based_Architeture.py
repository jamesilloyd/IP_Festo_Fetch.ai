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

        festoFactoryAgent1 = FactoryAgent(2,self,(21,15),distributed)
        self.schedule.add(festoFactoryAgent1)
        self.grid.place_agent(festoFactoryAgent1,festoFactoryAgent1.coordinates)

        festoFactoryAgent2 = FactoryAgent(3,self,(15,21),distributed)
        self.schedule.add(festoFactoryAgent2)
        self.grid.place_agent(festoFactoryAgent2,festoFactoryAgent2.coordinates)

        festoFactoryAgent3 = FactoryAgent(4,self,(9,15),distributed)
        self.schedule.add(festoFactoryAgent3)
        self.grid.place_agent(festoFactoryAgent3,festoFactoryAgent3.coordinates)

        festoFactoryAgent4 = FactoryAgent(5,self,(15,9),distributed)
        self.schedule.add(festoFactoryAgent4)
        self.grid.place_agent(festoFactoryAgent4,festoFactoryAgent4.coordinates)

        festoFactoryAgent5 = FactoryAgent(6,self,(11,11),distributed)
        self.schedule.add(festoFactoryAgent5)
        self.grid.place_agent(festoFactoryAgent5,festoFactoryAgent5.coordinates)

        festoFactoryAgent6 = FactoryAgent(7,self,(19,19),distributed)
        self.schedule.add(festoFactoryAgent6)
        self.grid.place_agent(festoFactoryAgent6,festoFactoryAgent6.coordinates)
        
        festoFactoryAgent7 = FactoryAgent(8,self,(11,19),distributed)
        self.schedule.add(festoFactoryAgent7)
        self.grid.place_agent(festoFactoryAgent7,festoFactoryAgent7.coordinates)

        festoFactoryAgent8 = FactoryAgent(9,self,(19,11),distributed)
        self.schedule.add(festoFactoryAgent8)
        self.grid.place_agent(festoFactoryAgent8,festoFactoryAgent8.coordinates)
        
        festoFactoryAgent9 = FactoryAgent(10,self,(5,5),distributed)
        self.schedule.add(festoFactoryAgent9)
        self.grid.place_agent(festoFactoryAgent9,festoFactoryAgent9.coordinates)


        festoFactoryAgent10 = FactoryAgent(11,self,(5,25),distributed)
        self.schedule.add(festoFactoryAgent10)
        self.grid.place_agent(festoFactoryAgent10,festoFactoryAgent10.coordinates)

        festoFactoryAgent11 = FactoryAgent(12,self,(25,5),distributed)
        self.schedule.add(festoFactoryAgent11)
        self.grid.place_agent(festoFactoryAgent11,festoFactoryAgent11.coordinates)

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

    
            
            

