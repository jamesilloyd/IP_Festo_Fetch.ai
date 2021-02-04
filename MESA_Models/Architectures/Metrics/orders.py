from mesa import Model

def ordersComplete(model):

    total_orders = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'order'):
            total_orders += 1


    return total_orders

    

def averageOrderWaitTime(model):
    
    total_orders = 0
    total_wait_time = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'order'):
            total_orders += 1
            total_wait_time += agent.waitTime
    


    
    return total_wait_time/total_orders