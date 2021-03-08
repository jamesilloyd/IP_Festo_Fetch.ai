from mesa import Model, Agent

def ordersComplete(model):

    total_orders = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed):
            total_orders += 1


    return total_orders



def successfulOrders(model):

    total_orders = 0
    total_successful_orders = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed):
            total_orders += 1
            if(agent.successful):
                total_successful_orders +=1


    if total_orders == 0:
        return 0
    else:
        return total_successful_orders / total_orders

def lateOrders(model):

    late_orders = 0
    complete_orders = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed):
            complete_orders += 1
            if(agent.completedDate > agent.dueDate):
                late_orders +=1

    if complete_orders == 0:
        return 0
    else:
        return late_orders/complete_orders

    

def averageOrderWaitTime(model):
    
    total_orders = 0
    total_wait_time = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'order'):
            total_orders += 1
            total_wait_time += agent.waitTime

    if(total_orders != 0):
        return total_wait_time/total_orders
    else:
        return 0


def individualOrderWaitTime(agent):

    if agent.agentType == 'order':
        return  agent.waitTime
    else:
        return None

    
