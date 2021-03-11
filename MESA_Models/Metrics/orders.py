from mesa import Model, Agent

def ordersComplete(model):

    total_orders = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and agent.successful and not agent.void):
            total_orders += 1 / agent.size


    return total_orders

def totalWIPSize(model):

    totalWIPSize = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'machine'):
            totalWIPSize += len(agent.backLogOrders)
            if(agent.isOperating):
                totalWIPSize += 1
    
    return totalWIPSize



def successfulOrders(model):

    total_orders = 0
    total_successful_orders = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void):
            total_orders += 1 / agent.size
            if(agent.successful):
                total_successful_orders +=1 / agent.size


    if total_orders == 0:
        return 0
    else:
        return total_successful_orders / total_orders

def lateOrders(model):

    late_orders = 0
    complete_orders = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void):
            complete_orders += 1 / agent.size
            if(agent.completedDate > agent.dueDate):
                late_orders +=1 / agent.size

    if complete_orders == 0:
        return 0
    else:
        return late_orders/complete_orders

    

def averageOrderWaitTime(model):
    
    total_orders = 0
    total_wait_time = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and not agent.void):
            total_orders += 1  / agent.size
            total_wait_time += agent.waitTime  / agent.size

    if(total_orders != 0):
        return total_wait_time/total_orders
    else:
        return 0


def individualOrderWaitTime(agent):

    if agent.agentType == 'order' and not agent.void:
        return  agent.waitTime  / agent.size
    else:
        return None

    
