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

def outsourcedOrders(model):
    # Out of all orders (successful or unsuccessful) this is the number of ones that have been outsourcee

    total_orders = 0
    total_outsourced_orders = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void):
            total_orders += 1 / agent.size
            if(agent.outsourced):
                total_outsourced_orders +=1 / agent.size


    if total_orders == 0:
        return 0
    else:
        return total_outsourced_orders / total_orders

def averageSuccessfulOrderPrice(model):
    # How much does a successful order usually sell for

    total_successful_orders = 0
    price = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful):
            price += agent.winningPrice
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return price / total_successful_orders

def averageSuccessfulOrderMakeSpan(model):
    # How much does a successful order usually sell for

    total_successful_orders = 0
    makeSpan = 0

    for agent in model.schedule.agents:
        if(agent.agentType == 'order' and agent.completed and not agent.void and agent.successful):
            makeSpan += (agent.completedDate - agent.createdDate)
            total_successful_orders += 1

    if total_successful_orders == 0:
        return 0
    else:
        return makeSpan / total_successful_orders



def averageSuccessfulOrderPriceASAP(model):
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

def averageSuccessfulOrderMakeSpanASAP(model):
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

def averageSuccessfulOrderMakeSpanCheap(model):
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

    

# Test this works - add into the visual run  mode of the simulator

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
