from mesa import Model

def machine_utilisation(model):
    
    total_time_working = 0
    total_time_free = 0
    for agent in model.schedule.agents:
        if(agent.agentType == 'machine'):
            total_time_free += agent.timeFree
            total_time_working += agent.timeWorking

    print('TOTAL FREE TIME {0} - TOTAL WORKING TIME {1}'.format(total_time_free,total_time_working))
    if(total_time_free != 0 and total_time_working != 0):
        utilisation = total_time_working / (total_time_working + total_time_free)
    else:
        utilisation = 0
    
    return utilisation