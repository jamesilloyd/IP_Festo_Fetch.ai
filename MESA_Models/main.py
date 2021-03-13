from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.batchrunner import BatchRunner
from agentPortrayal import agent_portrayal
from Metrics import utilisation, orders, messages
from matplotlib import pyplot as plt
from Architectures.Inter_Firm_Trust_Based.Trust_Based_Architeture import TrustBasedArchitecture
import os
import operationTypes
import random
import sys

runBatch = True
runSingleBatch = False
architecture = 'Inter-Firm'
saveResults = True

if __name__ == '__main__':

    # orig_stdout = sys.stdout
    # f=open('out5.txt','w')
    # sys.stdout = f


    if(runBatch):
        # TODO: need to look a bit more into how the agent_reporters work and what they could be used for 
        #   - they seem useful for tracking the journey of an individiaul agent
        #   - additional use could be for reducing run time for model reporters
        fixed_params = {'width': 40, 'height': 40,'distributed':False, 'schedulingType':'FIFO','splitSize':1}

        # variable_params = {'schedulingType':['FIFO','Moores','EDD','SPT','MDD'],'splitSize':range(1,5)}
        # variable_params = {'distributed':[True,False]}
        variable_params = {'quantity':[1,2,3,4,5]}
        # 'newOrderProbability':range(2,10)}
        # variable_params = {'distributed':[True,False]}

        batch_run = BatchRunner(
            TrustBasedArchitecture,
            variable_params,
            fixed_params,
            iterations=5,
            max_steps=900,
            model_reporters={
                "Utilisation": utilisation.machine_utilisation, 
                "Complete_Orders": orders.ordersComplete,
                # TODO this is a fake metric
                'Average_Order_Wait_Time': orders.averageOrderWaitTime, 
                "Successful_Orders":orders.successfulOrders,
                'Messages_Sent': messages.messagesSent, 
                'Late_Orders':orders.lateOrders,
                # TODO this is a fake metric
                'WIP_Backlog':orders.totalWIPSize, 
                'Max_Messages_Sent': messages.maxMessagesSentFromNode, 
                'Max_Messages_Received': messages.maxMessagesReceivedByNode},
            agent_reporters={
                'id':'unique_id',
            #     # 'messages_sent':'messagesSent'
            #     # TODO: add in other agent reports that you would like to use
            }
        )

        batch_run.run_all()

        model_data = batch_run.get_model_vars_dataframe()
        agent_data = batch_run.get_agent_vars_dataframe()

    
        # Save results
        if(saveResults):
            number = 0
            while (os.path.exists('/Users/heisenberg/IP/MESA_Models/results/{1}/test_{0}'.format(number, architecture)) == True):
                number += 1

            # TODO: maybe make a text file that describes the test that has been run
            os.makedirs(
                '/Users/heisenberg/IP/MESA_Models/results/{1}/test_{0}'.format(number, architecture))

            model_data.to_pickle(
                '/Users/heisenberg/IP/MESA_Models/results/{1}/test_{0}/model_data.pkl'.format(number, architecture))
            agent_data.to_pickle(
                '/Users/heisenberg/IP/MESA_Models/results/{1}/test_{0}/agent_data.pkl'.format(number, architecture))

    
    elif(runSingleBatch):

        model = TrustBasedArchitecture(40,40,True,{
                                    "Utilisation": utilisation.machine_utilisation, 
                                    "Complete Orders": orders.ordersComplete,
                                    'Average Order Wait Time': orders.averageOrderWaitTime, 
                                    "% Successful Orders":orders.successfulOrders,
                                    'Messages Sent': messages.messagesSent, 
                                    "% Late Orders":orders.lateOrders,
                                    'WIP Backlog':orders.totalWIPSize, 
                                    'Max Messages Sent': messages.maxMessagesSentFromNode, 
                                    'Max Messages Received': messages.maxMessagesReceivedByNode},
                                    {
                                    'id':'unique_id',
                                    'messages_sent':'messagesSent'}
                                    )

        for i in range(900):
            model.step()

        agent_data = model.datacollector.get_agent_vars_dataframe()


        one_agent_data = agent_data.xs(6, level="AgentID")
        one_agent_data.messages_sent.plot()
        plt.show()

        # specific_step_messages_sent = hello.xs(20, level="Step")["messages_sent"]
        # specific_step_messages_sent.hist(bins=range(50))
        # plt.show()

                               
    
    else:
        grid = CanvasGrid(agent_portrayal, 40, 40, 800, 800)
        chart = ChartModule([{'Label': 'Utilisation', "Color": 'Black'}],data_collector_name='datacollector')
        chart2 = ChartModule([{'Label': 'Complete Orders', 'Color': 'Black'}], data_collector_name='datacollector')
        chart3 = ChartModule([{'Label': 'Average Order Wait Time','Color': 'Red'}], data_collector_name='datacollector')
        chart4 = ChartModule([{'Label': 'Messages Sent','Color': 'Red'}], data_collector_name='datacollector')
        chart5 = ChartModule([{'Label': 'Successful Orders','Color': 'Green'}], data_collector_name='datacollector')
        chart6 = ChartModule([{'Label': 'Late Orders','Color': 'Red'}], data_collector_name='datacollector')
        chart7 = ChartModule([{'Label': 'WIP Backlog','Color': 'Blue'}], data_collector_name='datacollector')
        chart8 = ChartModule([{'Label': 'Max Messages Sent','Color': 'Blue'}], data_collector_name='datacollector')
        chart9 = ChartModule([{'Label': 'Max Messages Received','Color': 'Blue'}], data_collector_name='datacollector')

        server = ModularServer(TrustBasedArchitecture,
                            [grid, chart, chart4, chart5,  chart2, chart6, chart7, chart3,  chart9, chart8],
                            'Festo-Fetch.ai',
                            {'width': 40, 'height': 40, 'distributed':True,'quantity':20,'schedulingType':'FIFO','splitSize':2,
                                'model_reporters_dict': {
                                    "Utilisation": utilisation.machine_utilisation,
                                    "Complete Orders": orders.ordersComplete,
                                    'Average Order Wait Time': orders.averageOrderWaitTime, 
                                    "Successful Orders":orders.successfulOrders,
                                    'Messages Sent': messages.messagesSent, 
                                    'Late Orders':orders.lateOrders,
                                    'WIP Backlog':orders.totalWIPSize, 
                                    'Max Messages Sent': messages.maxMessagesSentFromNode, 
                                    'Max Messages Received': messages.maxMessagesReceivedByNode}})

        server.port = 8521
        server.launch()