import sys
from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import random
# from .agents.order_agent import OrderAgent
from .agents.machine_agent import MachineAgent
from .agents.product_agent import ProductAgent
from .agents.manufacturing_system_agent import FactoryAgent
from .agents.staff_agent import ScheduleStaffAgent

'''
Product Resource Order and Staff Architecture (PROSA)
- this is quite similar to a federated approach (mixture of heterarchical and hierarchical)
- product agents represent the product type containing information about process plans, BOM, ueser requirements etc.
- resource agents represent a manufacturing resource, it allocates its resource capacity to other holong
- order agent represents the task of making the product according to the customer order, e.g. physical state, controls logistic and production operations by negotiating with resource agents
- staff agent is considered an external expert that gives advice to the basic holons regarding the correct solution to a problem


Aggregation is used to cluster several simple agents into a more complex agent
'''

class PROSAModel(Model):

    def __init__(self, width, height, probability, operationTypes, model_reporters_dict = None):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.probability = probability
        self.operationTypes = operationTypes


        festoFactoryAgent = FactoryAgent(1,self,(6,12))
        self.schedule.add(festoFactoryAgent)
        self.grid.place_agent(festoFactoryAgent,(6,12))

        productAgent1 = ProductAgent(2,self,'product1',operations=['CNC','3D','IM'],needsQC=False,bom=[],coordinates =(8,18))
        self.schedule.add(productAgent1)
        self.grid.place_agent(productAgent1,(8,18))

        scheduleAgent1 = ScheduleStaffAgent(3,self,(8,4),'scheduler')
        self.schedule.add(scheduleAgent1)
        self.grid.place_agent(scheduleAgent1,(8,4))


        machineAgent1 = MachineAgent(4,self,'CNC',4,(12,5))
        self.schedule.add(machineAgent1)
        self.grid.place_agent(machineAgent1,machineAgent1.coordinates)

        machineAgent2 = MachineAgent(5,self,'3D',8,(12,8))
        self.schedule.add(machineAgent2)
        self.grid.place_agent(machineAgent2,machineAgent2.coordinates)

        machineAgent3 = MachineAgent(6,self,'3D',8,(16,8))
        self.schedule.add(machineAgent3)
        self.grid.place_agent(machineAgent3,machineAgent3.coordinates)

        machineAgent4 = MachineAgent(7,self,'IM',7,(12,12))
        self.schedule.add(machineAgent4)
        self.grid.place_agent(machineAgent4,machineAgent4.coordinates)

        machineAgent5 = MachineAgent(8,self,'IM',7,(16,12))
        self.schedule.add(machineAgent5)
        self.grid.place_agent(machineAgent5,machineAgent5.coordinates)
        

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
            print('new order request')
            # operations = []
            # # Choose random selection of operations
            # for j in range(random.randrange(5)):
            #     operations.append(random.choice(self.operationTypes))
            # orderAgent = OrderAgent(self.schedule.get_agent_count()+1,self,operations)
            # self.schedule.add(orderAgent)
            # self.grid.place_agent(orderAgent,(0,19))
            #TODO Find a way of representing these customers
            message = {'messageType':'order_request','productType':'product1','dueDate':'example_due_date'}
            # TODO: APPEND TO FESTO FACTORY AGENT
            for agent in self.schedule.agents:
                if(agent.agentType == 'factory'):
                    agent.receivedMessages.append(message)
            
            

