from .agents.offer import Requirement
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
    [(25, 25), ['3D_SLS']],
]



class MASArchitecture(Model):

    def __init__(self, width, height, distributed, model_reporters_dict=None, agent_reporters_dict=None, newOrderProbability=10, quantity=1, splitSize=1):

        print('New Order Probability {} - Quantity {}'.format(newOrderProbability,quantity))
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.minutes = 0
        self.hours = 0
        self.days = 0
        self.weeks = 0

        federationCentre = TrustFederationAgent(1, self, (49, 49))

        self.schedule.add(federationCentre)
        self.grid.place_agent(federationCentre, federationCentre.coordinates)

        numberOfCheap = round(quantity * 0.5)
        numberOfASAP = round(quantity * 0.5)

        # print(numberOfASAP)
        # print(numberOfCheap)

        while numberOfCheap != 0:
            numberOfCheap -= 1
            for factory in factoriesAndCapabilities:
                factoryNumber = self.schedule.get_agent_count() + 1

                newFactoryAgent = FactoryAgent(
                    factoryNumber, self, factory[0], distributed, newOrderProbability, splitSize=splitSize)

                self.schedule.add(newFactoryAgent)
                self.grid.place_agent(
                    newFactoryAgent, newFactoryAgent.coordinates)

                incrementedYCoordinate = 2
                for capability in factory[1]:
                    coordinates = (
                        factory[0][0] + 3, factory[0][1] - incrementedYCoordinate)
                    newMachine = MachineAgent(self.schedule.get_agent_count(
                    ) + 1, self, capability, coordinates, factoryNumber,asapOrCheap='cheap')
                    self.schedule.add(newMachine)
                    self.grid.place_agent(newMachine, newMachine.coordinates)
                    incrementedYCoordinate += 2


            

        while numberOfASAP != 0:
            numberOfASAP -= 1
            for factory in factoriesAndCapabilities:

                coordinates = (factory[0][0] +15,factory[0][1] +15)
                factoryNumber = self.schedule.get_agent_count() + 1

                newFactoryAgent = FactoryAgent(
                    factoryNumber, self, coordinates, distributed, newOrderProbability, splitSize=splitSize)

                self.schedule.add(newFactoryAgent)
                self.grid.place_agent(
                    newFactoryAgent, newFactoryAgent.coordinates)

                incrementedYCoordinate = 2
                for capability in factory[1]:
                    newCoordinates = (
                        coordinates[0] + 3, coordinates[1] - incrementedYCoordinate)
                    
                    newMachine = MachineAgent(self.schedule.get_agent_count(
                    ) + 1, self, capability, newCoordinates, factoryNumber,asapOrCheap='asap')
                    self.schedule.add(newMachine)
                    self.grid.place_agent(newMachine, newMachine.coordinates)
                    incrementedYCoordinate += 2

            
        if(model_reporters_dict is None):
            self.datacollector = DataCollector()
        else:
            self.datacollector = DataCollector(
                model_reporters=model_reporters_dict,
                agent_reporters=agent_reporters_dict
            )

    def step(self):
        # print("Weeks {} Days {} Hours {}".format(
        #     self.weeks, self.days, self.hours))

        '''Advance the model by one step.'''
        self.schedule.step()
        # Collect data
        self.datacollector.collect(self)
        self.hours += 1
        if(self.hours == 8):
            self.hours = 0
            self.days += 1

        if(self.days == 5):
            self.days = 0
            self.weeks += 1