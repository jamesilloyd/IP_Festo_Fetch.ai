import pandas as pd
from matplotlib import pyplot as plt



agent_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/Architectures/results/test_0/agent_data.pkl')
model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/Architectures/results/test_0/model_data.pkl')



plt.scatter(model_data_pickle.probability,model_data_pickle.Utilisation)
plt.show()