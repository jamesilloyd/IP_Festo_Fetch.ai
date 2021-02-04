from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from agentPortrayal import agent_portrayal
from simpleModel import MyModel
from Metrics import utilisation, orders

# TODO: this is an example of a visualisation run, need to create another for running a batch on the same model
if __name__ == '__main__':

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
