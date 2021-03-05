

class Message():

    def __init__(self,fromId,messageType, orderId = 0, capability = '', canCarryOutRequest = False, price = 0,requestedIds = [],capabilities = [],machineId=0):
        self.fromId = fromId
        self.type = messageType
        self.orderId = orderId
        self.capability = capability
        self.canCarryOutRequest = canCarryOutRequest
        self.price = price
        self.requestedIds = requestedIds
        self.capabilities = capabilities
        self.machineId = machineId
