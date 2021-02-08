
from mesa import Agent, Model

class OrderAgent(Agent):

    agentType = 'order'
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model, operations):
        super().__init__(unique_id, model)
        self.operations = operations
        self.lookingForResource = True
        self.completed = False
        self.waitTime = 0
        self.receivedMessages = []
        self.messagesSent = 0
        self.inOperation = False
        self.checkingMessages = False


    def step(self):
        # Check if it needs 
        if(not self.operations):
            self.completed = True
            self.model.grid.move_agent(self,(0,0))
        else:
            if(self.lookingForResource):
                print('OrderAgent {0} - looking for scheduler'.format(self.unique_id))
                for agent in self.model.schedule.agents:
                    if(agent.agentType == 'scheduler'):
                        message = {"operation":self.operations[0],'id':self.unique_id}
                        print('Order {0} - message sent to scheduler {1} - {2}'.format(self.unique_id,agent.unique_id,message))
                        agent.receivedMessages.append(message)
                        self.messagesSent += 1
                        

                self.lookingForResource = False
                self.checkingMessage = True
                self.waitTime += 1

            elif(self.checkingMessage):
                timeTillStart = None
                chosenMachine = {'time':None,'machineAgent':None}
                self.waitTime += 1
                # Finding machine that can do the job
                for message in self.receivedMessages:

                    if message['answer'] == 'y':
                        for agent in self.model.schedule.agents:
                            if(agent.unique_id in message['machineIds']):
                                # Check how long it will be before the machine can work on us
                                timeTillStart = agent.timeLeftOnOperation + len(agent.backLogOrders) * agent.timeToComplete
                                # First viable order
                                if chosenMachine['time'] is None:
                                    chosenMachine['machineAgent'] = agent
                                    chosenMachine['time'] = timeTillStart

                                #  Best offer available
                                elif(timeTillStart < chosenMachine['time']):
                                    chosenMachine['machineAgent'] = agent
                                    chosenMachine['time'] = timeTillStart
                        
                
                if(chosenMachine['machineAgent'] is not None):
                    print('Order {0} - Found machine to move to {1}'.format(self.unique_id, chosenMachine['machineAgent'].unique_id))
                    # If we have found a machine, append to it
                    self.receivedMessages.clear()
                    self.model.grid.move_agent(self,chosenMachine['machineAgent'].backlogCoordinates)
                    chosenMachine['machineAgent'].backLogOrders.append(self)
                    self.checkingMessage = False 

            elif(self.inOperation):
                
                # In operation
                pass
            else:
                # Waiting for operation
                self.waitTime += 1
                


               
