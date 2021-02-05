import sys
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
from FedAgents.orderAgent import OrderAgent
from FedAgents.machineAgent import MachineAgent
from FedAgents.scheduleAgent import ScheduleAgent
import operationTypes

'''
Every machine has a scheduling agent that arranges it's activities.
'''

class FederatedModel(Model):
    """A model with some number of agents."""
    def __init__(self, width, height, probability, model_reporters_dict = None):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.probability = probability
        

        for i in range(6):
            operations = []
            # Choose random selection of operations
            for j in range(random.randrange(1,5,1)):
                operations.append(random.choice(operationTypes.operationTypes))

            orderAgent1 = OrderAgent(i,self,operations)
            self.schedule.add(orderAgent1)
            self.grid.place_agent(orderAgent1,(0,i))
        

        orderNumber = 6


        CNCScheduler = ScheduleAgent(orderNumber + 1,self,'CNC',(8,1))
        self.schedule.add(CNCScheduler)
        self.grid.place_agent(CNCScheduler,(6,1))

        IMScheduler = ScheduleAgent(orderNumber + 2,self,'IM',(8,1))
        self.schedule.add(IMScheduler)
        self.grid.place_agent(IMScheduler,(6,8))

        ThreeDScheduler = ScheduleAgent(orderNumber + 3,self,'3D',(8,1))
        self.schedule.add(ThreeDScheduler)
        self.grid.place_agent(ThreeDScheduler,(6,4))


        machineAgent1 = MachineAgent(orderNumber + 4,self,'CNC',4,(8,1))
        self.schedule.add(machineAgent1)
        self.grid.place_agent(machineAgent1,(8,1))

        machineAgent2 = MachineAgent(orderNumber + 5,self,'3D',8,(8,4))
        self.schedule.add(machineAgent2)
        self.grid.place_agent(machineAgent2,(8,4))

        machineAgent2 = MachineAgent(orderNumber + 6,self,'3D',8,(12,4))
        self.schedule.add(machineAgent2)
        self.grid.place_agent(machineAgent2,(12,4))

        machineAgent3 = MachineAgent(orderNumber + 7,self,'IM',7,(8,8))
        self.schedule.add(machineAgent3)
        self.grid.place_agent(machineAgent3,(8,8))

        machineAgent3 = MachineAgent(orderNumber + 8,self,'IM',7,(12,8))
        self.schedule.add(machineAgent3)
        self.grid.place_agent(machineAgent3,(12,8))

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

