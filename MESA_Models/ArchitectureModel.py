from hashlib import new
# from .agents.offer import Requirement
import sys, os
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
# from .agents.order_agent import OrderAgent
from agents.machine_agent import MachineAgent
from agents.factory_agent import FactoryAgent
from agents.SOEF import SOEF
from agents.order_agent import OrderAgent
from agents.message import Message


# Coordinates and capabilities of each factory
factoriesAndCapabilities = [
    [(25, 25), ['3D_SLS']],
]

class MASArchitecture(Model):

    def __init__(self, width, height, distributed, model_reporters_dict=None, agent_reporters_dict=None, newOrderProbability=10, quantity=1, splitSize=1,verbose = True,searchSize = 1,ordersPerWeek = 1):
        sys.stdout = sys.__stdout__
        print('New Order Probability {} - Quantity {} - Orders Per week {}'.format(newOrderProbability,quantity,ordersPerWeek))
        self.verbose = verbose
        if(verbose):
            sys.stdout = sys.__stdout__
        else:
            sys.stdout = open(os.devnull, 'w')

        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.minutes = 0
        self.hours = 0
        self.days = 0
        self.weeks = 0

        # This is the number of external orders the marketplace recieved per week
        self.ordersPerWeek = ordersPerWeek
        # This is the probability at any given step that a factory will produce a new order
        self.newOrderProbability = newOrderProbability
        self.splitSize = splitSize

        federationCentre = SOEF(1, self, (49, 49), searchSize)

        self.schedule.add(federationCentre)
        self.grid.place_agent(federationCentre, federationCentre.coordinates)

        numberOfCheap = round(quantity * 0.5)
        numberOfASAP = round(quantity * 0.5)

        # This fella is only used to produce orders, has no capabilities of it's own
        self.dummyFactoryId = self.schedule.get_agent_count() + 1
        self.dummyFactoryAgent = FactoryAgent(self.dummyFactoryId,self,(2,2),distributed,newOrderProbability,splitSize=splitSize)
        self.schedule.add(self.dummyFactoryAgent)
        self.grid.place_agent(self.dummyFactoryAgent,self.dummyFactoryAgent.coordinates)

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
        
        sys.stdout = sys.__stdout__
        print("Steps {} Weeks {} Days {} Hours {}".format(self.schedule.steps,
            self.weeks, self.days, self.hours))
        if(not self.verbose):
            sys.stdout = open(os.devnull, 'w')

        # Generate new orders
        if(self.ordersPerWeek <= 40):
            number = random.randrange(40//self.ordersPerWeek)
            if(number == 0):
                capabilities = ['3D_SLS']
                orderAgent = OrderAgent(self.schedule.get_agent_count()+1,self,capabilities,self.dummyFactoryId,splitSize=self.splitSize)
                self.schedule.add(orderAgent)
                self.grid.place_agent(orderAgent,self.dummyFactoryAgent.newOrderCoordinates)
                newMessage = Message(self.dummyFactoryId,'findResources')
                orderAgent.receivedMessages.append(newMessage)
        else:
            count = self.ordersPerWeek // 40
            while count != 0:
                count -= 1
                capabilities = ['3D_SLS']
                orderAgent = OrderAgent(self.schedule.get_agent_count()+1,self,capabilities,self.dummyFactoryId,splitSize=self.splitSize)
                self.schedule.add(orderAgent)
                self.grid.place_agent(orderAgent,self.dummyFactoryAgent.newOrderCoordinates)
                newMessage = Message(self.dummyFactoryId,'findResources')
                orderAgent.receivedMessages.append(newMessage)

        '''Advance the model by one step.'''
        # Way easier to convert to hours... 
        if(self.ordersPerWeek <= 40):

            number = random.randrange(40//self.ordersPerWeek)
            if(number == 0):
                capabilities = ['3D_SLS']
                orderAgent = OrderAgent(self.schedule.get_agent_count()+1,self,capabilities,self.dummyFactoryId,splitSize=self.splitSize)
                self.schedule.add(orderAgent)
                self.grid.place_agent(orderAgent,self.dummyFactoryAgent.newOrderCoordinates)
                newMessage = Message(self.dummyFactoryId,'findResources')
                orderAgent.receivedMessages.append(newMessage)
        else:
            count = self.ordersPerWeek // 40
            while count != 0:
                count -= 1
                capabilities = ['3D_SLS']
                orderAgent = OrderAgent(self.schedule.get_agent_count()+1,self,capabilities,self.dummyFactoryId,splitSize=self.splitSize)
                self.schedule.add(orderAgent)
                self.grid.place_agent(orderAgent,self.dummyFactoryAgent.newOrderCoordinates)
                newMessage = Message(self.dummyFactoryId,'findResources')
                orderAgent.receivedMessages.append(newMessage)

        
        
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