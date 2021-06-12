from mesa import Agent

'''HOW TO VISUALISE THE MODEL'''
def agent_portrayal(agent):
    # TODO: do we need to add this agentType into the original class?
    if(agent.agentType == 'order'):
        color = ''
        textColor = 'white'
        if(agent.completed and agent.successful):
            color = 'green'
        elif(agent.completed and not agent.successful):
            color = 'red'
        elif(agent.outsourced):
            color = 'yellow'
            textColor = 'black'
        else:
            color = 'blue'
        
        if agent.size != 1:
            r = 0.5
        else:
            r = 1

        portrayal = {"Shape": "circle",
                "Color": color,
                "Filled": "true",
                'text_color':textColor,
                "Layer": 0.5,
                'text': str(agent.unique_id),
                "r": r}
    elif(agent.agentType == 'machine'):
        portrayal = {"Shape": "rect",
                "Color": 'green',
                "Filled": "true",
                'text': agent.typeOfOperation + ' - ' + str(agent.unique_id),
                'text_color':'black',
                "Layer": 0,
                "w": 1,'h':1 }
    elif(agent.agentType in ['scheduler','broker','staff','federator']):
        portrayal = {"Shape": "circle",
                "Color": 'green',
                "Filled": "true",
                'text': 'SOEF',
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
        portrayal = {"Shape": "rect",
                "Color": 'red',
                "Filled": "true",
                'text': 'Factory',
                'text_color':'black',
                "Layer": 0,
                "w": 3,'h':3}
    
    return portrayal