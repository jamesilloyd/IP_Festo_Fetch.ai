from mesa import Agent, Model

class ScheduleAgent(Agent):
    
    agentType = 'scheduler'

    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, typeOfOperation, coordinates):
        super().__init__(unique_id, model)
        self.orders = []
        self.coordinates = coordinates
        self.typeOfOperation = typeOfOperation
        self.receivedMessages = []
        self.messagesSent = 0
        self.machineIds = []

    def step(self):
        
        # Check messages
        for message in self.receivedMessages:
            answer = "n"
            if(message['operation'] == self.typeOfOperation):
                # Reply saying yes i can do it and calculate time based on backlog
                answer = "y"

            # send message to agent with that id
            for agent in self.model.schedule.agents:
                if agent.unique_id == message['id']:
                    newMessage ={'answer':answer,'id':self.unique_id, 'machineIds':self.machineIds}
                    agent.receivedMessages.append(newMessage)
                    print('Scheduler {0} - message sent to order {1} - {2}'.format(self.unique_id,agent.unique_id,newMessage))
                    self.messagesSent += 1
            
        self.receivedMessages.clear()

                        