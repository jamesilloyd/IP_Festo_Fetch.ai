from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.batchrunner import BatchRunner
from agentPortrayal import agent_portrayal
from Metrics import utilisation, orders, messages
from matplotlib import pyplot as plt
from Architectures.Block3.Test3.ArchitectureModel import MASArchitecture
import os
import random
import sys

runBatch = False
runSingleBatch = False
architecture = 'Inter-Firm'
saveResults = True


if __name__ == '__main__':

    # orig_stdout = sys.stdout
    # f=open('out5.txt','w')
    # sys.stdout = f

    # {'width': 60, 'height': 60, 'distributed':True,'quantity':100,'splitSize':1,'newOrderProbability':80,'proportion_of_weights':1,

    if(runBatch):
        fixed_params = {'width': 60, 'height': 60,'splitSize':1,'quantity':100,'distributed':True, 'newOrderProbability':80,'proportion_of_weights':0.5}

        variable_params = {'quantity':range(10,500,20)}

        batch_run = BatchRunner(
            MASArchitecture,
            variable_params,
            fixed_params,
            iterations=10,
            max_steps=1000,
            model_reporters={
                "Utilisation": utilisation.machine_utilisation, 
                "Complete_Orders": orders.ordersComplete,
                'Average_Order_Wait_Time': orders.averageOrderWaitTime, 
                "Successful_Orders":orders.successfulOrders,
                'Messages_Sent': messages.messagesSent, 
                'Late_Orders':orders.lateOrders,
                'WIP_Backlog':orders.totalWIPSize, 
                'Outsourced_Orders':orders.outsourcedOrders,
                'Successful_Order_Price_Average':orders.averageSuccessfulOrderPrice,
                'Successful_Order_Price_ASAP_Agent':orders.averageSuccessfulOrderPriceASAP,
                'Successful_Order_Price_Cheap_Agent':orders.averageSuccessfulOrderPriceCheap,
                'Successful_Order_Makespan_Average':orders.averageSuccessfulOrderMakeSpan,
                'Successful_Order_Makespan_ASAP_Agent':orders.averageSuccessfulOrderMakeSpanASAP,
                'Successful_Order_Makespan_Cheap_Agent':orders.averageSuccessfulOrderMakeSpanCheap,
                'Max_Messages_Sent_Order': messages.maxMessagesSentFromOrder, 
                'Max_Messages_Received_Order': messages.maxMessagesReceivedByOrder,
                'Max_Messages_Sent_Factory': messages.maxMessagesSentFromFactory, 
                'Max_Messages_Received_Factory': messages.maxMessagesReceivedByFactory},
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
            while (os.path.exists('/Users/heisenberg/IP/MESA_Models/results/Block3/Test3/test_{0}'.format(number)) == True):
                number += 1

            # TODO: maybe make a text file that describes the test that has been run
            os.makedirs(
                '/Users/heisenberg/IP/MESA_Models/results/Block3/Test3/test_{0}'.format(number))

            model_data.to_pickle(
                '/Users/heisenberg/IP/MESA_Models/results/Block3/Test3/test_{0}/model_data.pkl'.format(number))
            agent_data.to_pickle(
                '/Users/heisenberg/IP/MESA_Models/results/Block3/Test3/test_{0}/agent_data.pkl'.format(number))

    
    elif(runSingleBatch):

        model = MASArchitecture(40,40,True,{
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
        grid = CanvasGrid(agent_portrayal, 60, 60, 600, 600)
        chart = ChartModule([{'Label': 'Utilisation', "Color": 'Black'}],data_collector_name='datacollector')
        chart2 = ChartModule([{'Label': 'Complete Orders', 'Color': 'Black'}], data_collector_name='datacollector')
        chart3 = ChartModule([{'Label': 'Average Order Wait Time','Color': 'Red'}], data_collector_name='datacollector')
        chart4 = ChartModule([{'Label': 'Messages Sent','Color': 'Red'}], data_collector_name='datacollector')
        chart5 = ChartModule([{'Label': 'Successful Orders','Color': 'Green'}], data_collector_name='datacollector')
        chart6 = ChartModule([{'Label': 'Late Orders','Color': 'Red'}], data_collector_name='datacollector')
        chart7 = ChartModule([{'Label': 'WIP Backlog','Color': 'Blue'}], data_collector_name='datacollector')
        chart8 = ChartModule([{'Label': 'Max Messages Sent - Order','Color': 'Blue'}], data_collector_name='datacollector')
        chart9 = ChartModule([{'Label': 'Max Messages Received - Order','Color': 'Blue'}], data_collector_name='datacollector')
        chart10 = ChartModule([{'Label': 'Max Messages Sent - Factory','Color': 'Red'}], data_collector_name='datacollector')
        chart11 = ChartModule([{'Label': 'Max Messages Received - Factory','Color': 'Red'}], data_collector_name='datacollector')
        chart12 = ChartModule([{'Label': 'Outsourced Orders','Color': 'Blue'}], data_collector_name='datacollector')
        chart13 = ChartModule([{'Label': '% Cheap orders with cheap machines','Color': 'Green'}], data_collector_name='datacollector')
        chart14 = ChartModule([{'Label': '% Asap orders with fast machines','Color': 'Green'}], data_collector_name='datacollector')

        
        server = ModularServer(MASArchitecture,
                            [grid, chart, chart4, chart5,  chart12, chart2, chart6, chart7, chart3,  chart8, chart9, chart10,chart11,chart13,chart14],
                            'Festo-Fetch.ai',
                            {'width': 60, 'height': 60, 'distributed':True,'quantity':100,'splitSize':1,'newOrderProbability':80,'proportion_of_weights':0.5,
                                'model_reporters_dict': {
                                    "Utilisation": utilisation.machine_utilisation,
                                    "Complete Orders": orders.ordersComplete,
                                    'Average Order Wait Time': orders.averageOrderWaitTime, 
                                    "Successful Orders":orders.successfulOrders,
                                    'Messages Sent': messages.messagesSent, 
                                    'Late Orders':orders.lateOrders,
                                    'WIP Backlog':orders.totalWIPSize, 
                                    'Max Messages Sent - Order': messages.maxMessagesSentFromOrder, 
                                    'Max Messages Received - Order': messages.maxMessagesReceivedByOrder,
                                    'Max Messages Sent - Factory': messages.maxMessagesSentFromFactory, 
                                    'Max Messages Received - Factory': messages.maxMessagesReceivedByFactory,
                                    'Outsourced Orders': orders.outsourcedOrders,
                                    '% Cheap orders with cheap machines':orders.cheapOrdersWithCheapMachines,
                                    '% Asap orders with fast machines':orders.asapOrdersWithFastMachines

                                    }})

        server.port = 8521
        server.launch()