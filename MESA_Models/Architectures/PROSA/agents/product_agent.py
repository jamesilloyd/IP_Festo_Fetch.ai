from mesa import Agent, Model

'''
- Represents the catalogue of products available within the factory 
- Holds the process and product knowledge to assure the correct making of the product with sufficient quality
- Contains information on:
    ○ Process plan
        § works these out based on the available resources
    ○ BOM
    ○ QC procedures
    ○ user requirements 
'''

class ProductAgent(Agent):

    agentType = 'product'

    def __init__(self, unique_id, model, productType, operations: list, needsQC: bool, bom:list,coordinates):
        super().__init__(unique_id, model)
        self.productType = productType
        self.operations = operations
        self.bom = bom
        self.needsQC = needsQC
        self.coordinates = coordinates

        self.receivedMessages = []
        self.messagesSent = 0
        self.machineIds = []


        # Register the product agent with the factory agent
        for agent in self.model.schedule.agents:
            if(agent.agentType == 'factory'):
                #TODO: This is the equivalent of sending a message (should we do that instead?)
                agent.productAgentIds.append(self.unique_id)
        

        
        # Other considerations:
        # - available resources to map out procedures for making the product
        # - user requirements for the product e.g. surface finish etc. 

    @property
    def operationsAndResources(self):
        # Here we need to know what machines are available for each operation 
        pass

    @property
    def backlogCoordinates(self):
        changedX = self.coordinates[0] - 1
        return (changedX,self.coordinates[1])


    def step(self):
        
        # Needs to check whether it has received a message from the HMS enquiring about a new order
        #   - this is handled by the factory agent
        
        # Needs to check whether it has received a message from an order asking what operation to carry out and which machines to go to
        for message in self.receivedMessages:
            if(message['messageType'] == 'request_operations'):
                returnMessage = []
                for operation in self.operations:
                    suitableMachineIds = []

                    for machineId in self.machineIds:
                        if machineId['capability'] == operation:
                            suitableMachineIds.append(machineId['unique_id'])

                    returnMessage.append({'operation':operation,'machineIds':suitableMachineIds})

                # Return the message
                for agent in self.model.schedule.agents:
                    if agent.unique_id == message['id']:
                        agent.operations = returnMessage
                        agent.receivedOperations = True

        self.receivedMessages.clear()

            




        


                


               
