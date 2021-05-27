import sys
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
# from .agents.order_agent import OrderAgent
from .agents.machine_agent import MachineAgent
from .agents.factory_agent import FactoryAgent
from .agents.federation_agent import TrustFederationAgent

'''
Here we are testing whether the order agent can improve the overall system performance by considering scheduling as part of its decision (instead of bid price)
'''

factoriesAndCapabilities = [
    [(25,25),['CNC','CNC','CNC']],
    [(10,9),['IM','IM']],
    [(10,25),['3D_SLS','CNC','IM']],
    [(25,9),['3D_FDM']],
    [(15,35),['3D_DMLS','3D_FDM','CNC']],
    [(30,35),['IM','3D_SLS','CNC']],
    
    [(75,25),['CNC','CNC','CNC']],
    [(60,9),['IM','IM']],
    [(60,25),['3D_SLS','CNC','IM']],
    [(75,9),['3D_FDM']],
    [(65,35),['3D_DMLS','3D_FDM','CNC']],
    [(80,35),['IM','3D_SLS','CNC']],

    [(25,75),['CNC','CNC','CNC']],
    [(10,59),['IM','IM']],
    [(10,75),['3D_SLS','CNC','IM']],
    [(25,59),['3D_FDM']],
    [(15,85),['3D_DMLS','3D_FDM','CNC']],
    [(30,85),['IM','3D_SLS','CNC']],

    [(70,70),['CNC','CNC','CNC']],
    [(60,59),['IM','IM']],
    [(60,75),['3D_SLS','CNC','IM']],
    [(75,59),['3D_FDM']],
    [(65,85),['3D_DMLS','3D_FDM','CNC']],
    [(80,85),['IM','3D_SLS','CNC']],
    ]


class MASArchitecture(Model):

    def __init__(self, width, height, distributed, model_reporters_dict = None, agent_reporters_dict = None,newOrderProbability = 10,quantity = 1,splitSize = 1):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        
        federationCentre = TrustFederationAgent(1,self,(50,50))
        
        self.schedule.add(federationCentre)
        self.grid.place_agent(federationCentre,federationCentre.coordinates)


        while quantity != 0:
            quantity -= 1
            for factory in factoriesAndCapabilities:
                factoryNumber = self.schedule.get_agent_count() + 1
                
                newFactoryAgent = FactoryAgent(factoryNumber,self,factory[0],distributed,newOrderProbability,splitSize = splitSize)
                
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
                agent_reporters = agent_reporters_dict
            )
    
    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()
        
    
            
            

