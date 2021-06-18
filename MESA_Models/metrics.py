from os import stat
from mesa import Model, Agent
from functools import lru_cache

@lru_cache(maxsize=30)
def loopThroughModel(model,count): #The count is used to restart the cache for every step in the simulation
    #print('looping')
    stats = {}
    total_orders = 0
    total_successful_orders = 0
    totalWIPSize = 0
    total_outsourced_orders = 0
    total_price = 0
    total_makespan = 0
    total_late_orders = 0
    total_wait_time = 0
    total_satisfaction_score = 0
    total_successful_satisfaction_score = 0

    total_machine_time_working = 0

    total_order_unsuccessful_due_to_no_bids = 0

    total_machine_time_free = 0
    total_messages_sent = 0

    max_messages_sent_order = 0
    max_messages_received_order = 0
    max_messages_sent_factory = 0
    max_messages_received_factory = 0


    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void):
            total_orders += 1 / agent.size
            total_wait_time += agent.waitTime / agent.size
            total_satisfaction_score += agent.finalSatisfactionScore
            
            if(agent.orderUnsuccessfulDueToNoProposals):
                total_order_unsuccessful_due_to_no_bids += 1
            
            if(agent.successful):
                total_successful_orders += 1 / agent.size
                total_price += agent.winningPrice
                total_makespan += (agent.completedDate - agent.createdDate)
                total_successful_satisfaction_score += agent.finalSatisfactionScore
                
                if(agent.completedDate > agent.dueDate):
                    total_late_orders += 1 / agent.size
                if(agent.outsourced):
                    total_outsourced_orders +=1 / agent.size


        if(agent.agentType == 'machine'):
            totalWIPSize += len(agent.backLogOrders)
            total_machine_time_free += agent.timeFree
            total_machine_time_working += agent.timeWorking
            if(agent.isOperating):
                totalWIPSize += 1

        if agent.agentType == 'order' and not agent.void:
            total_messages_sent += agent.totalMessagesSent / agent.size
        elif not agent.void:
            total_messages_sent += agent.totalMessagesSent

        if agent.maxMessagesSent > max_messages_sent_order and not agent.void and agent.agentType == 'order':
            max_messages_sent_order = agent.maxMessagesSent
        
        if agent.maxMessagesReceived > max_messages_received_order and not agent.void and agent.agentType == 'order':
            max_messages_received_order = agent.maxMessagesReceived 

        
        if agent.maxMessagesSent > max_messages_sent_factory and not agent.void and agent.agentType == 'factory':
            max_messages_sent_factory = agent.maxMessagesSent

        if agent.maxMessagesReceived > max_messages_received_factory and not agent.void and agent.agentType == 'factory':
            max_messages_received_factory = agent.maxMessagesReceived 

        
    
    stats['ordersComplete'] = total_orders
    stats['totalWIPSize'] = totalWIPSize
    stats['totalMessagesSent'] = total_messages_sent
    stats['averageMessagesSent'] = total_messages_sent / model.schedule.get_agent_count()

    stats['maxMessagesSentFromOrder'] = max_messages_sent_order
    stats['maxMessagesReceivedByOrder'] = max_messages_received_order
    stats['maxMessagesSentFromFactory'] = max_messages_sent_factory
    stats['maxMessagesReceivedByFactory'] = max_messages_received_factory

    if(total_machine_time_working != 0 and total_machine_time_free != 0):
        stats['machineUtilisation'] = total_machine_time_working / (total_machine_time_working + total_machine_time_free)
    else:
        stats['machineUtilisation'] = 0 

    if total_orders == 0:
        stats['successfulOrders'] = 0
        stats['averageOrderWaitTime'] = 0
        stats['averageSatisfactionScore'] = 0
        
    else:
        stats['successfulOrders'] = total_successful_orders / total_orders
        stats['averageOrderWaitTime'] = total_wait_time / total_orders
        stats['averageSatisfactionScore'] = total_satisfaction_score / total_orders

    if total_orders - total_successful_orders == 0:
        stats['orderFailedDueToNoProposals'] = 0
    else:
        stats['orderFailedDueToNoProposals'] = total_order_unsuccessful_due_to_no_bids / (total_orders - total_successful_orders)

    if total_successful_orders == 0:
        stats['outsourcedOrders'] = 0
        stats['averageSuccessfulOrderPrice'] = 0
        stats['averageSuccessfulOrderMakeSpan'] = 0
        stats['lateOrders'] = 0
        stats['averageSuccessfulSatisfactionScore'] = 0
    else:
        stats['outsourcedOrders'] = total_outsourced_orders / total_successful_orders
        stats['averageSuccessfulOrderPrice'] = total_price / total_successful_orders
        stats['averageSuccessfulOrderMakeSpan'] = total_makespan / total_successful_orders
        stats['lateOrders'] = total_late_orders / total_successful_orders
        stats['averageSuccessfulSatisfactionScore'] = total_successful_satisfaction_score / total_successful_orders

    return stats

def modelStatistics(model,output):

    #print('running model statistics')

    statistics = {}
    
    statistics = loopThroughModel(model,model.schedule.steps)

    return statistics[output]


'''MACHINE METRICS'''

def noProposalOrders(model):

    return modelStatistics(model,'orderFailedDueToNoProposals')

def machineUtilisation(model):

    return modelStatistics(model,'machineUtilisation')

def totalWIPSize(model):
    
    return modelStatistics(model,'totalWIPSize')


def averageOrderWaitTime(model):
    return modelStatistics(model,'averageOrderWaitTime')


'''ORDER METRICS'''
def ordersComplete(model):
    return modelStatistics(model,'ordersComplete')


def successfulOrders(model):

    return modelStatistics(model,'successfulOrders')


def outsourcedOrders(model):
    # Out of all unsuccessful this is the number of ones that have been outsourced
    return modelStatistics(model,'outsourcedOrders')


def averageSuccessfulOrderPrice(model):
    # How much does a successful order usually sell for
    return modelStatistics(model,'averageSuccessfulOrderPrice')

def averageSuccessfulOrderMakeSpan(model):
    # How much does a successful order usually take to produce
    return modelStatistics(model,'averageSuccessfulOrderMakeSpan')

def lateOrders(model):

    return modelStatistics(model,'lateOrders')

def averageSatisfactionScore(model):

    return modelStatistics(model,'averageSatisfactionScore')


def averageSuccessfulSatisfactionScore(model):

    return modelStatistics(model,'averageSuccessfulSatisfactionScore')


'''MESSAGE METRICS'''
def totalMessagesSent(model):

     return modelStatistics(model,'totalMessagesSent')

def averageMessagesSent(model):

     return modelStatistics(model,'averageMessagesSent')


def maxMessagesSentFromOrder(model):

    return modelStatistics(model,'maxMessagesSentFromOrder')

def maxMessagesReceivedByOrder(model):
    return modelStatistics(model,'maxMessagesReceivedByOrder')


def maxMessagesSentFromFactory(model):
    return modelStatistics(model,'maxMessagesSentFromFactory')


def maxMessagesReceivedByFactory(model):
    return modelStatistics(model,'maxMessagesReceivedByFactory')




'''WEIGHT CHECK METRICS'''
def averageSuccessfulOrderPriceAsap(model):
    # How much does a successful order usually sell for
    total_successful_orders = 0
    price = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful and agent.requirementType == 'asap'):
            price += agent.winningPrice
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return price / total_successful_orders

def averageSuccessfulOrderMakespanAsap(model):
    # How much does a successful order usually sell for

    total_successful_orders = 0
    makeSpan = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful and agent.requirementType == 'asap'):
            makeSpan += (agent.completedDate - agent.createdDate)
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return makeSpan / total_successful_orders

def averageSuccessfulOrderPriceCheap(model):
    # How much does a successful order usually sell for

    total_successful_orders = 0
    price = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful and agent.requirementType == 'cheap'):
            price += agent.winningPrice
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return price / total_successful_orders

def averageSuccessfulOrderMakespanCheap(model):
    # How much does a successful order usually sell for

    total_successful_orders = 0
    makeSpan = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful and agent.requirementType == 'cheap'):
            makeSpan += (agent.completedDate - agent.createdDate)
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return makeSpan / total_successful_orders


def averageSuccessfulOrderPriceNeutral(model):
    # How much does a successful order usually sell for

    total_successful_orders = 0
    price = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful and agent.requirementType == 'neutral'):
            price += agent.winningPrice
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return price / total_successful_orders

def averageSuccessfulOrderMakespanNeutral(model):
    # How much does a successful order usually sell for

    total_successful_orders = 0
    makeSpan = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful and agent.requirementType == 'neutral'):
            makeSpan += (agent.completedDate - agent.createdDate)
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return makeSpan / total_successful_orders




def cheapOrdersWithCheapMachines(model):

    total_successful_agents = 0
    total_cheap_cheap_agents = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and not agent.void and agent.completed and agent.successful and agent.requirementType == 'cheap'):
            total_successful_agents += 1
            
            if(agent.winningMachineType == agent.requirementType):
                total_cheap_cheap_agents += 1
    
    if(total_successful_agents == 0):
        return 0
    else:
        return total_cheap_cheap_agents/total_successful_agents


def asapOrdersWithFastMachines(model):

    total_successful_agents = 0
    total_asap_asap_agents = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and not agent.void and agent.completed and agent.successful and agent.requirementType == 'asap'):
            total_successful_agents += 1
            
            if(agent.winningMachineType == agent.requirementType):
                total_asap_asap_agents += 1
    
    if(total_successful_agents == 0):
        return 0
    else:
        return total_asap_asap_agents/total_successful_agents





def percentageOfSuccessfulASAPOrders(model):

    total_asap_orders = 0
    total_successful_asap_orders = 0
    
    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and not agent.void and agent.requirementType == 'asap'and agent.completed):
            total_asap_orders += 1
            if(agent.successful):
                total_successful_asap_orders += 1


    if(total_asap_orders == 0):
        return 0
    else:
        return total_successful_asap_orders / total_asap_orders

def percentageOfSuccessfulCheapOrders(model):

    total_cheap_orders = 0
    total_successful_cheap_orders = 0
    
    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and not agent.void and agent.requirementType == 'cheap' and agent.completed):
            total_cheap_orders += 1
            if(agent.successful):
                total_successful_cheap_orders += 1


    if(total_cheap_orders == 0):
        return 0
    else:
        return total_successful_cheap_orders / total_cheap_orders





def percentageOfSuccessfulNeutralOrders(model):

    total_cheap_orders = 0
    total_successful_cheap_orders = 0
    
    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and not agent.void and agent.requirementType == 'neutral' and agent.completed):
            total_cheap_orders += 1
            if(agent.successful):
                total_successful_cheap_orders += 1


    if(total_cheap_orders == 0):
        return 0
    else:
        return total_successful_cheap_orders / total_cheap_orders