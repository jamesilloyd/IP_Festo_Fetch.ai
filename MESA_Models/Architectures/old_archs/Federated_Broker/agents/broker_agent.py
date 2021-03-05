from mesa import Agent, Model

class BrokerAgent(Agent):
    
    agentType = 'broker'

    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, coordinates):
        super().__init__(unique_id, model)
        self.orders = []
        self.coordinates = coordinates
        self.receivedMessages = []
        self.messagesSent = 0


    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])

    
    def step(self):
        
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

                        