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

runBatch = False
runSingleBatch = False
architecture = 'Inter-Firm'
saveResults = True


if __name__ == '__main__':

    if(runBatch):
        # TODO: need to look a bit more into how the agent_reporters work and what they could be used for 
        #   - they seem useful for tracking the journey of an individiaul agent
        #   - additional use could be for reducing run time for model reporters
        fixed_params = {'width': 40, 'height': 40, 'distributed':True}
                        # 'operationTypes': operationTypes.operationTypes}

        variable_params = {'communicationMethod':['Trust','PROSA']}

        batch_run = BatchRunner(
            TrustBasedArchitecture,
            variable_params,
            fixed_params,
            iterations=20,
            max_steps=900,
            model_reporters={
                "Utilisation": utilisation.machine_utilisation, 
                "Complete_Orders": orders.ordersComplete,
                'Average_Order_Wait_Time': orders.averageOrderWaitTime, 
                "Successful_Orders":orders.successfulOrders,
                'Messages_Sent': messages.messagesSent, 
                'Late_Orders':orders.lateOrders,
                'WIP_Backlog':orders.totalWIPSize, 
                'Max_Messages_Sent': messages.maxMessagesSentFromNode, 
                'Max_Messages_Received': messages.maxMessagesReceivedByNode},
            # agent_reporters={"WaitTime": "unique_id"}
            agent_reporters={
                'id':'unique_id',
                'messages_sent':'messagesSent'
                # TODO: add in other agent reports that you would like to use
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
                                    "Successful Orders":orders.successfulOrders,
                                    'Messages Sent': messages.messagesSent, 
                                    'Late Orders':orders.lateOrders,
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
        grid = CanvasGrid(agent_portrayal, 40, 40, 600, 600)
        chart = ChartModule([{'Label': 'Utilisation', "Color": 'Black'}],
                            data_collector_name='datacollector')
        chart2 = ChartModule(
            [{'Label': 'Complete Orders', 'Color': 'Red'}], data_collector_name='datacollector')
        chart3 = ChartModule([{'Label': 'Average Order Wait Time',
                               'Color': 'Green'}], data_collector_name='datacollector')
        chart4 = ChartModule([{'Label': 'Messages Sent',
                               'Color': 'Green'}], data_collector_name='datacollector')
        chart5 = ChartModule([{'Label': 'Successful Orders',
                               'Color': 'Green'}], data_collector_name='datacollector')
        chart6 = ChartModule([{'Label': 'Late Orders',
                               'Color': 'Red'}], data_collector_name='datacollector')

        chart7 = ChartModule([{'Label': 'WIP Backlog',
                               'Color': 'Green'}], data_collector_name='datacollector')
        chart8 = ChartModule([{'Label': 'Max Messages Sent',
                               'Color': 'Blue'}], data_collector_name='datacollector')

        chart9 = ChartModule([{'Label': 'Max Messages Received',
                               'Color': 'Blue'}], data_collector_name='datacollector')

        server = ModularServer(TrustBasedArchitecture,
                               [grid, chart9, chart8,chart7,chart, chart4, chart2, chart5, chart3, chart6],
                               'Festo-Fetch.ai',
                               {'width': 40, 'height': 50, 'distributed':True,'communicationMethod':'PROSA',
                                'model_reporters_dict': {
                                    "Utilisation": utilisation.machine_utilisation, "Complete Orders": orders.ordersComplete,'Average Order Wait Time': orders.averageOrderWaitTime, "Successful Orders":orders.successfulOrders,'Messages Sent': messages.messagesSent, 'Late Orders':orders.lateOrders,'WIP Backlog':orders.totalWIPSize, 'Max Messages Sent': messages.maxMessagesSentFromNode, 'Max Messages Received': messages.maxMessagesReceivedByNode}})

        server.port = 8521
        server.launch()