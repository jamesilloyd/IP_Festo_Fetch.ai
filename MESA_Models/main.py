from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.batchrunner import BatchRunner
from agentPortrayal import agent_portrayal
import metrics
from matplotlib import pyplot as plt
from ArchitectureModel import MASArchitecture
import os
import random
import sys

runBatch = True
architecture = 'Inter-Firm'
saveResults = True



if __name__ == '__main__':

    dir_path = os.path.dirname(os.path.realpath(__file__))
    

    if(runBatch):
        fixed_params = {'width': 60, 'height': 60,'splitSize':1,'distributed':True,'verbose':False,'searchSize':1,'batchRun':True}

        variable_params = {'quantity':[10,20,50,80,100,120,150],'ordersPerWeek':[1,5,20,40,80,120]}

        batch_run = BatchRunner(
            MASArchitecture,
            variable_params,
            fixed_params,
            iterations=10,
            max_steps=800,
            model_reporters={
                "Utilisation": metrics.machineUtilisation,
                "CompleteOrders": metrics.ordersComplete,
                'AverageOrderWaitTime': metrics.averageOrderWaitTime,
                'TotalMessagesSent': metrics.totalMessagesSent, 
                'AverageMessagesSent': metrics.averageMessagesSent, 
                "SuccessfulOrders":metrics.successfulOrders,
                "noProposalOrders":metrics.noProposalOrders,
                'OutsourcedOrders': metrics.outsourcedOrders,
                'LateOrders':metrics.lateOrders,
                'WIPBacklog':metrics.totalWIPSize, 
                'MaxMessagesSentOrder': metrics.maxMessagesSentFromOrder, 
                'MaxMessagesReceivedOrder': metrics.maxMessagesReceivedByOrder,
                'MaxMessagesSentFactory': metrics.maxMessagesSentFromFactory, 
                'MaxMessagesReceivedFactory': metrics.maxMessagesReceivedByFactory,
                
                'AverageSatisfactionScore':metrics.averageSatisfactionScore,
                'AverageSuccessfulSatisfactionScore':metrics.averageSuccessfulSatisfactionScore,
                'CheapOrdersWithCheapMachines':metrics.cheapOrdersWithCheapMachines,
                'AsapOrdersWithFastMachines':metrics.asapOrdersWithFastMachines,
                
                'AverageSuccessfulPrice': metrics.averageSuccessfulOrderPrice,
                'AverageSuccessfulOrderPriceCheap':metrics.averageSuccessfulOrderPriceCheap,
                'AverageSuccessfulOrderPriceNeutral':metrics.averageSuccessfulOrderPriceNeutral,
                'AverageSuccessfulOrderPriceAsap':metrics.averageSuccessfulOrderPriceAsap,
                
                'AverageSuccessfulMakespan': metrics.averageSuccessfulOrderMakeSpan,
                'AverageSuccessfulOrderMakespanCheap':metrics.averageSuccessfulOrderMakespanCheap,
                'AverageSuccessfulOrderMakespanNeutral':metrics.averageSuccessfulOrderMakespanNeutral,
                'AverageSuccessfulOrderMakespanAsap':metrics.averageSuccessfulOrderMakespanAsap,

                'SuccessfulAsapOrders':metrics.percentageOfSuccessfulASAPOrders,
                'SuccessfulCheapOrders':metrics.percentageOfSuccessfulCheapOrders,
                'SuccessfulNeutralOrders':metrics.percentageOfSuccessfulNeutralOrders
                },
            agent_reporters={
                'id':'unique_id',
            #     # TODO: add in other agent reports that you would like to use
            }
        )

        batch_run.run_all()

        model_data = batch_run.get_model_vars_dataframe()
        agent_data = batch_run.get_agent_vars_dataframe()

    
        # Save results
        if(saveResults):
            number = 0
            ### CHANGE PATH TO WHERE YOU WANT RESULTS TO BE SAVED
            while (os.path.exists('{}/results/test_{}'.format(dir_path,number)) == True):
                number += 1

            # TODO: maybe make a text file that describes the test that has been run
            os.makedirs(
                '{}/results/test_{}'.format(dir_path,number))

            model_data.to_pickle(
                '{}/results/test_{}/model_data.pkl'.format(dir_path,number))
            agent_data.to_pickle(
                '{}/results/test_{}/agent_data.pkl'.format(dir_path,number))

    
    
    else:
        # TODO: rename all of these
        grid = CanvasGrid(agent_portrayal, 60, 60, 600, 600)
        chart = ChartModule([{'Label': 'Utilisation', "Color": 'Black'}],data_collector_name='datacollector')
        chart2 = ChartModule([{'Label': 'Complete Orders', 'Color': 'Black'}], data_collector_name='datacollector')
        chart3 = ChartModule([{'Label': 'Average Order Wait Time','Color': 'Red'}], data_collector_name='datacollector')
        chart4 = ChartModule([{'Label': 'Total Messages Sent','Color': 'Red'}], data_collector_name='datacollector')
        averageMessagesSentChart = ChartModule([{'Label': 'Average Messages Sent','Color': 'Red'}], data_collector_name='datacollector')
        chart5 = ChartModule([{'Label': 'Successful Orders','Color': 'Green'}], data_collector_name='datacollector')
        chart6 = ChartModule([{'Label': 'Outsourced Orders','Color': 'Blue'}], data_collector_name='datacollector')
        chart7 = ChartModule([{'Label': 'Late Orders','Color': 'Red'}], data_collector_name='datacollector')
        chart8 = ChartModule([{'Label': 'WIP Backlog','Color': 'Blue'}], data_collector_name='datacollector')
        chart9 = ChartModule([{'Label': 'Max Messages Sent - Order','Color': 'Blue'}], data_collector_name='datacollector')
        chart10 = ChartModule([{'Label': 'Max Messages Received - Order','Color': 'Blue'}], data_collector_name='datacollector')
        chart11 = ChartModule([{'Label': 'Max Messages Sent - Factory','Color': 'Red'}], data_collector_name='datacollector')
        chart12 = ChartModule([{'Label': 'Max Messages Received - Factory','Color': 'Red'}], data_collector_name='datacollector')
        
        

        chart13 = ChartModule([{'Label': 'Average satisfaction score','Color': 'Blue'}], data_collector_name='datacollector')
        chart14 = ChartModule([{'Label': 'Average successful satisfaction score','Color': 'Blue'}], data_collector_name='datacollector')
        chart15 = ChartModule([{'Label': '% Cheap orders with cheap machines','Color': 'Green'}], data_collector_name='datacollector')
        chart16 = ChartModule([{'Label': '% Asap orders with fast machines','Color': 'Green'}], data_collector_name='datacollector')

        chart17 = ChartModule([{'Label': 'Average successful price','Color': 'Blue'}], data_collector_name='datacollector')
        chart18 = ChartModule([{'Label': 'Average successful price Cheap','Color': 'Blue'}], data_collector_name='datacollector')
        chart19 = ChartModule([{'Label': 'Average successful price Neutral','Color': 'Blue'}], data_collector_name='datacollector')
        chart20 = ChartModule([{'Label': 'Average successful price Asap','Color': 'Blue'}], data_collector_name='datacollector')

        chart21 = ChartModule([{'Label': 'Average successful makespan','Color': 'Green'}], data_collector_name='datacollector')
        chart22 = ChartModule([{'Label': 'Average successful makespan Cheap','Color': 'Green'}], data_collector_name='datacollector')
        chart23 = ChartModule([{'Label': 'Average successful makespan Neutral','Color': 'Green'}], data_collector_name='datacollector')
        chart24 = ChartModule([{'Label': 'Average successful makespan Asap','Color': 'Green'}], data_collector_name='datacollector')

        chart25 = ChartModule([{'Label': 'Successful Cheap Orders','Color': 'Red'}], data_collector_name='datacollector')
        chart26 = ChartModule([{'Label': 'Successful Neutral Orders','Color': 'Red'}], data_collector_name='datacollector')
        chart27 = ChartModule([{'Label': 'Successful Asap Orders','Color': 'Red'}], data_collector_name='datacollector')
        noProposalOrdersChart = ChartModule([{'Label': 'Orders that received no proposals','Color': 'Red'}], data_collector_name='datacollector')



        

        
        server = ModularServer(MASArchitecture,
                            [grid,
                             chart,
                             chart2,
                             chart3,
                             chart4,
                             averageMessagesSentChart,
                            chart5,  
                            noProposalOrdersChart,
                            chart6,
                            chart7, 
                             chart8, chart9, chart10,chart11, chart12,
                            chart13,chart14,
                            chart15,
                            chart16,chart17,
                            chart18, chart19, chart20,chart21,chart22,chart23,chart24,chart25,chart26,chart27
            ],
                            'Festo-Fetch.ai',

                            {'width': 60, 'height': 60, 'distributed':True,'quantity':10,'splitSize':1,'newOrderProbability':5,'verbose':True,'ordersPerWeek':40,
                                'model_reporters_dict': {
                                    "Utilisation": metrics.machineUtilisation,
                                    "Complete Orders": metrics.ordersComplete,
                                    'Average Order Wait Time': metrics.averageOrderWaitTime, 
                                    "Successful Orders":metrics.successfulOrders,
                                    'Total Messages Sent': metrics.totalMessagesSent, 
                                    'Average Messages Sent': metrics.averageMessagesSent, 
                                    'Late Orders':metrics.lateOrders,
                                    'WIP Backlog':metrics.totalWIPSize, 
                                    'Max Messages Sent - Order': metrics.maxMessagesSentFromOrder, 
                                    'Max Messages Received - Order': metrics.maxMessagesReceivedByOrder,
                                    'Max Messages Sent - Factory': metrics.maxMessagesSentFromFactory, 
                                    'Max Messages Received - Factory': metrics.maxMessagesReceivedByFactory,
                                    'Outsourced Orders': metrics.outsourcedOrders,
                                    'Orders that received no proposals':metrics.noProposalOrders,
                                    
                                    'Average successful satisfaction score':metrics.averageSuccessfulSatisfactionScore,
                                    'Average satisfaction score':metrics.averageSatisfactionScore,
                                    '% Cheap orders with cheap machines':metrics.cheapOrdersWithCheapMachines,
                                    '% Asap orders with fast machines':metrics.asapOrdersWithFastMachines,

                                    'Average successful price': metrics.averageSuccessfulOrderPrice,

                                    'Average successful price Cheap':metrics.averageSuccessfulOrderPriceCheap,
                                    'Average successful price Neutral':metrics.averageSuccessfulOrderPriceNeutral,
                                    'Average successful price Asap':metrics.averageSuccessfulOrderPriceAsap,
                                    
                                    'Average successful makespan': metrics.averageSuccessfulOrderMakeSpan,

                                    'Average successful makespan Cheap':metrics.averageSuccessfulOrderMakespanCheap,
                                    'Average successful makespan Neutral':metrics.averageSuccessfulOrderMakespanNeutral,
                                    'Average successful makespan Asap':metrics.averageSuccessfulOrderMakespanAsap,
                
                                    'Successful Cheap Orders':metrics.percentageOfSuccessfulASAPOrders,
                                    'Successful Neutral Orders':metrics.percentageOfSuccessfulCheapOrders,
                                    'Successful Asap Orders':metrics.percentageOfSuccessfulNeutralOrders

                                    }})

        server.port = 8521
        server.launch()