from mesa import Agent

'''HOW TO VISUALISE THE MODEL'''
def agent_portrayal(agent):
    # TODO: do we need to add this agentType into the original class?
    if(agent.agentType == 'order'):
        color = ''
        if(agent.completed and agent.successful):
            color = 'green'
        elif(agent.completed and not agent.successful):
            color = 'red'
        else:
            color = 'blue'

        portrayal = {"Shape": "circle",
                "Color": color,
                "Filled": "true",
                'text_color':'white',
                "Layer": 0.5,
                'text': str(agent.unique_id),
                "r": 0.7}
    elif(agent.agentType == 'machine'):
        portrayal = {"Shape": "circle",
                "Color": 'green',
                "Filled": "true",
                'text': agent.typeOfOperation,
                'text_color':'black',
                "Layer": 0,
                "r": 0.7 }
    elif(agent.agentType in ['scheduler','broker','staff','federator']):
        portrayal = {"Shape": "circle",
                "Color": 'green',
                "Filled": "true",
                'text': agent.agentType,
                'text_color':'black',
                "Layer": 0,
                "r": 3}
    elif(agent.agentType == 'product'):
        portrayal = {"Shape": "circle",
                "Color": 'green',
                "Filled": "true",
                'text': agent.productType,
                'text_color':'black',
                "Layer": 0,
                "r": 0.7 }
    elif(agent.agentType == 'factory'):
        portrayal = {"Shape": "circle",
                "Color": 'red',
                "Filled": "true",
                'text': 'Factory',
                'text_color':'black',
                "Layer": 0,
                "r": 1.5}
    
    return portrayal