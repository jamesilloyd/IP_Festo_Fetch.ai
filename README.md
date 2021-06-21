# IP_Festo_Fetch.ai

# Prerequisites
```bash
pip install mesa
```

# File structure

## __main.py__
Simulations can be run here. They can be run as a batch or in visualisation mode by setting the booleans at the top of the file. 

## __ArchitectureModel.py__ file
This contains the architecture configuration. The factories and their capabilities are chosen by the list at the top of the file. Currently the architecture is setup to have 50% of the machines running fast/expensive and 50% of the machines running slow/cheap, this is based on the quantity of factories specified on initialisation. Additionally, at each "step" in the model new orders are generated based on the number of orders per week. 

## _agents_ folder
### __factory_agent.py__
The class for company / factory agents.
### __machine_agent.py__
The class for machine agents.
### __order_agent.py__
The class for order agents.
### __SOEF.py__
The class for the SOEF.
### __operations.py__
Contains the dictionary of capability parameters.
### __message.py__
Class for sending messages between agents. 


## __metrics.py__ file 
This contains the functions that iterate through the agents in the architecture and collects their attributes to create the performance metrics

## Results
Results can be created and stored as pandas in the the _results_ folder. 

## Visualisation
The __agentPortrayal.py__ file determines how the agents are displayed in the simulations.

## __run_results.py__ file
This file is used to access the saved results and render matplotlib 2D and 3D plots.
