from mesa import Agent

'''HOW TO VISUALISE THE MODEL'''
def agent_portrayal(agent):
    # TODO: do we need to add this agentType into the original class?
    if(agent.agentType == 'order'):
        portrayal = {"Shape": "circle",
                "Color": 'green' if agent.completed else 'blue',
                "Filled": "true",
                'text_color':'white',
                "Layer": 0.5,
                'text': str(agent.unique_id),
                "r": 0.4}
    elif(agent.agentType == 'machine'):
        portrayal = {"Shape": "circle",
                "Color": 'green',
                "Filled": "true",
                'text': agent.typeOfOperation,
                'text_color':'black',
                "Layer": 0,
                "r": 0.7 }
    elif(agent.agentType == 'scheduler' or agent.agentType == 'broker'):
        portrayal = {"Shape": "circle",
                "Color": 'red',
                "Filled": "true",
                'text': 'Scheduler',
                'text_color':'black',
                "Layer": 0,
                "r": 1 }
    
    return portrayal