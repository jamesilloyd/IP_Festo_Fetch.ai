
from .offer import Bid

class Message():

    def __init__(self,fromId,messageType, orderId = 0, capability = '', canCarryOutRequest = False, requestedIds = [],capabilities = [],machineId=0,orderAgent = None,bid=None):
        self.fromId = fromId
        self.type = messageType
        self.orderId = orderId
        self.capability = capability
        self.canCarryOutRequest = canCarryOutRequest
        self.requestedIds = requestedIds
        self.capabilities = capabilities
        self.machineId = machineId
        self.orderAgent = orderAgent

        self.bid = bid