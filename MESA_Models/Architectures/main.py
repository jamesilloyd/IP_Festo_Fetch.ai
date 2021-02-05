from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.batchrunner import BatchRunner
from agentPortrayal import agent_portrayal
from simpleModel import MyModel
from Metrics import utilisation, orders
from matplotlib import pyplot as plt
import os


runBatch = True
if __name__ == '__main__':

    if(runBatch):
        # TODO: need to look a bit more into how the agent_reporters work and what they could be used for
        fixed_params = {'width': 20, 'height': 20}
        variable_params = {"probability": range(1, 30, 1)}
        batch_run = BatchRunner(
            MyModel,
            variable_params,
            fixed_params,
            iterations=5,
            max_steps=500,
            model_reporters={"Utilisation": utilisation.machine_utilisation,
                             "Complete Orders": orders.ordersComplete, 'Average_Order_Wait_Time': orders.averageOrderWaitTime},
            agent_reporters={"WaitTime": "unique_id"}
        )

        batch_run.run_all()

        model_data = batch_run.get_model_vars_dataframe()
        agent_data = batch_run.get_agent_vars_dataframe()

        # Save results
        number = 0
        while (os.path.exists('/Users/heisenberg/IP/MESA_Models/Architectures/results/test_{0}'.format(number)) == True):
            number += 1

        os.makedirs(
            '/Users/heisenberg/IP/MESA_Models/Architectures/results/test_{0}'.format(number))

        model_data.to_pickle(
            '/Users/heisenberg/IP/MESA_Models/Architectures/results/test_{0}/model_data.pkl'.format(number))
        agent_data.to_pickle(
            '/Users/heisenberg/IP/MESA_Models/Architectures/results/test_{0}/agent_data.pkl'.format(number))

    else:
        grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
        chart = ChartModule([{'Label': 'Utilisation', "Color": 'Black'}],
                            data_collector_name='datacollector')
        chart2 = ChartModule(
            [{'Label': 'Complete Orders', 'Color': 'Red'}], data_collector_name='datacollector')
        chart3 = ChartModule([{'Label': 'Average Order Wait Time',
                               'Color': 'Green'}], data_collector_name='datacollector')
        server = ModularServer(MyModel, [grid, chart, chart2, chart3], 'DM', {'width': 20, 'height': 20, 'probability': 5, 'model_reporters_dict': {
            "Utilisation": utilisation.machine_utilisation, "Complete Orders": orders.ordersComplete, 'Average Order Wait Time': orders.averageOrderWaitTime}})

        server.port = 8521
        server.launch()
