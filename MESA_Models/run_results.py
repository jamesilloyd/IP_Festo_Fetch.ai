import pandas as pd
from matplotlib import pyplot as plt


# TODO: have way of changing this path
agent_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Inter-Firm/test_2/agent_data.pkl')
model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Inter-Firm/test_2/model_data.pkl')




# plt.scatter(model_data_pickle.N,model_data_pickle.Utilisation)

plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Utilisation)
plt.title('Utilisation')
plt.show()
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Complete_Orders)
plt.title('Complete_Orders')
plt.show()
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Average_Order_Wait_Time)
plt.title('Average_Order_Wait_Time')
plt.show()
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Successful_Orders)
plt.title('Successful_Orders')
plt.show()
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Messages_Sent)
plt.title('Messages_Sent')
plt.show()
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Late_Orders)
plt.title('Late_Orders')
plt.show()

# TODO: these tests are agent based, not model based as you
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.WIP_Backlog)
plt.title('WIP_Backlog')
plt.show()
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Max_Messages_Sent)
plt.title('Max_Messages_Sent')
plt.show()
plt.scatter(model_data_pickle.communicationMethod,model_data_pickle.Max_Messages_Received)
plt.title('Max_Messages_Received')
plt.show()
# plt.scatter(agent_data_pickle.id,agent_data_pickle.id)
# plt.show()


# print(agent_data_pickle.head())

# end_messages = agent_data_pickle.xs(5, level ="AgentID")
# end_messages.messages_sent.plot()


# plt.show()