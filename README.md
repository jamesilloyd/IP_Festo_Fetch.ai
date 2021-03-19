# IP_Festo_Fetch.ai

# Prerequisites
```bash
pip install mesa
```

# File structure

## __main.py__
Simulations can be run here. They can be run as a batch or in visualisation mode by setting the booleans at the top of the file. 

## _Architectures_ folder
This contains the agent and architecture classes. The most developed architecture is labelled _Inter-Firm / Trust_. Other architectures developed are included in the _old_archs_ sub-directory.

## _Metrics_ folder 

This contains the functions that iterate through the agents in the architecture and collects their attributes to return the performance metrics

## Results
The main results used in the Block 2 report can be found in the Excel file, other results are stored as pandas in the the _results_ folder. 

## Ignore  
The _tutorial_ folder was used to learn how to use MESA from their documentary https://mesa.readthedocs.io.
