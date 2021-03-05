from mesa import Agent, Model
import random

'''
	- Assists other holons in performing their work
	- Considered an external expert that gives advice
	- But the basic holon still makes the decision
	- Allows for centralised elements in the architecture
		○ Solves problems that are almost impossible in a distributed manner
	- They may request information from orders and resources so they have a full-view of the system
		○ This can allow orders or resources to have a schedule
		○ But it is advice, not commands
...Could be used to represent the MES, or shop floor control
'''
class StaffAgent(Agent):
    
    agentType = 'staff'

    def __init__(self, unique_id, model, coordinates):
        super().__init__(unique_id, model)
        
        self.coordinates = coordinates

        self.receivedMessages = []
        self.messagesSent = 0
        
    
    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])

    
    def step(self):
        pass
        # Depending on what type of staff agent the following functionality will be differemt


        

class ScheduleStaffAgent(StaffAgent):

    def __init__(self, unique_id, model, coordinates, typeOfStaff):
        super().__init__(unique_id, model, coordinates)
        
        self.typeOfStaff = typeOfStaff
        self.receivedMessages = []
        self.messagesSent = 0

        # Register the scheduler with the factory
        for agent in self.model.schedule.agents:
            if(agent.agentType == 'factory'):
                #TODO: This is the equivalent of sending a message (should we do that instead?)
                agent.scheduleStaffIds.append(self.unique_id)

    
    def step(self):
        # Check for messages from the Factory agent when a new order comes in to verify whether we have the capacity to fulfil it
        # This decision is made by checking the order due date against the currnt available time between the resources up until that point
            # To make this decision, all orders within the system must book out the resources before it knows how to be made (how else is it going to know how to schedule?)
        # TODO: enter prioritisation algorithm that decides which orders in the system are most important


        # Based on machines' current workflow, return a recommendation of which machine 
        # TODO: (carry out fancy scheduling algorithm?)
    
        
        # Check messages
        for message in self.receivedMessages:
            machineIds = []
            
            # TODO: Would the broker be able to have an up to date storage or machine ON / OFF status? 
            for agent in self.model.schedule.agents:
                if agent.agentType == 'machine':
                    if(agent.typeOfOperation == message['operation']):
                        machineIds.append(agent.unique_id)

            # send message to agent with that id
            for agent in self.model.schedule.agents:
                if agent.unique_id == message['id']:
                    newMessage = {'id':self.unique_id, 'machineIds':machineIds}
                    agent.receivedMessages.append(newMessage)
                    print('Broker {0} - message sent to order {1} - {2}'.format(self.unique_id,agent.unique_id,newMessage))
                    self.messagesSent += 1
            
        self.receivedMessages.clear()


    
    def canFitIntoSchedule(self):
        # TODO: decide on a suitable scheduling algorithm??? Not really my job
        # if(dueDate > self.model.schedule.)
        if(random.randrange(3) == 1):
            return True
        else:
            return False





