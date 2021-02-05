import sys
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
from Agents.orderAgent import OrderAgent
from Agents.scheduleAgent import ScheduleAgent
from Agents.machineAgent import MachineAgent
import operationTypes

class MyModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height, probability, model_reporters_dict = None):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.probability = probability
        

        for i in range(6):
            operations = []
            # Choose random selection of operations
            for j in range(random.randrange(5)):
                operations.append(random.choice(operationTypes.operationTypes))
            orderAgent1 = OrderAgent(i,self,operations)
            self.schedule.add(orderAgent1)
            self.grid.place_agent(orderAgent1,(0,i))
        

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

        # TODO: how can we refactor this out?
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
        self.newOrders()

    def newOrders(self):
        # Give a 20% probability that a new order will arrive into the system
        number = random.randrange(self.probability)
        if(number == 0):
            operations = []
            # Choose random selection of operations
            for j in range(random.randrange(5)):
                operations.append(random.choice(operationTypes.operationTypes))
            orderAgent = OrderAgent(self.schedule.get_agent_count()+1,self,operations)
            self.schedule.add(orderAgent)
            self.grid.place_agent(orderAgent,(0,19))

