from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.batchrunner import BatchRunner
from agentPortrayal import agent_portrayal
from federatedArchitecture import FederatedModel
from Metrics import utilisation, orders, messages
from matplotlib import pyplot as plt
import os


runBatch = True
saveResults = False
if __name__ == '__main__':

    if(runBatch):
        # TODO: need to look a bit more into how the agent_reporters work and what they could be used for
        fixed_params = {'width': 20, 'height': 20}
        variable_params = {"probability": range(1, 30, 1)}
        batch_run = BatchRunner(
            FederatedModel,
            variable_params,
            fixed_params,
            iterations=5,
            max_steps=500,
            model_reporters={"Utilisation": utilisation.machine_utilisation,
                             "Complete Orders": orders.ordersComplete, 'Average_Order_Wait_Time': orders.averageOrderWaitTime,'Messages_Sent': messages.messagesSent},
            agent_reporters={"WaitTime": "unique_id"}
        )

        batch_run.run_all()

        model_data = batch_run.get_model_vars_dataframe()
        agent_data = batch_run.get_agent_vars_dataframe()

        plt.scatter(model_data.probability,model_data.Utilisation)
        plt.show()
        plt.scatter(model_data.probability,model_data.Messages_Sent)
        plt.show()
        
        # Save results
        if(saveResults):
            number = 0
            while (os.path.exists('/Users/heisenberg/IP/MESA_Models/Architectures/Simple/results/test_{0}'.format(number)) == True):
                number += 1

            os.makedirs(
                '/Users/heisenberg/IP/MESA_Models/Architectures/Simple/results/test_{0}'.format(number))

            model_data.to_pickle(
                '/Users/heisenberg/IP/MESA_Models/Architectures/Simple/results/test_{0}/model_data.pkl'.format(number))
            agent_data.to_pickle(
                '/Users/heisenberg/IP/MESA_Models/Architectures/Simple/results/test_{0}/agent_data.pkl'.format(number))

    else:
        grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
        chart = ChartModule([{'Label': 'Utilisation', "Color": 'Black'}],
                            data_collector_name='datacollector')
        chart2 = ChartModule(
            [{'Label': 'Complete Orders', 'Color': 'Red'}], data_collector_name='datacollector')
        chart3 = ChartModule([{'Label': 'Average Order Wait Time',
                               'Color': 'Green'}], data_collector_name='datacollector')
        chart4 = ChartModule([{'Label': 'Messages Sent',
                               'Color': 'Green'}], data_collector_name='datacollector')
        server = ModularServer(FederatedModel, [grid, chart, chart4, chart2, chart3], 'DM', {'width': 20, 'height': 20, 'probability' : 2, 'model_reporters_dict': {
            "Utilisation": utilisation.machine_utilisation, "Complete Orders": orders.ordersComplete, 'Average Order Wait Time': orders.averageOrderWaitTime, 'Messages Sent': messages.messagesSent}})

        server.port = 8521
        server.launch()
