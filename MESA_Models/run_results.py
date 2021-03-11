import pandas as pd
from matplotlib import pyplot as plt


# TODO: have way of changing this path
agent_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Inter-Firm/test_15/agent_data.pkl')
model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Inter-Firm/test_15/model_data.pkl')

print(model_data_pickle)


plt.scatter(model_data_pickle.distributed,model_data_pickle.Utilisation.where(model_data_pickle['distributed']==1),label='DM')
plt.scatter(model_data_pickle.distributed,model_data_pickle.Utilisation.where(model_data_pickle['distributed']==0),label='CM')
plt.title('Utilisation')
plt.legend()
plt.show()
plt.scatter(model_data_pickle.distributed,model_data_pickle.Complete_Orders.where(model_data_pickle['distributed']==1),label='DM')
plt.scatter(model_data_pickle.distributed,model_data_pickle.Complete_Orders.where(model_data_pickle['distributed']==0),label='CM')

plt.title('Total Successful Orders')
plt.legend()
plt.show()

plt.scatter(model_data_pickle.distributed,model_data_pickle.Successful_Orders.where(model_data_pickle['distributed']==1),label='DM')
plt.scatter(model_data_pickle.distributed,model_data_pickle.Successful_Orders.where(model_data_pickle['distributed']==0),label='CM')
plt.title('% Successful Orders')
plt.legend()
plt.show()

plt.scatter(model_data_pickle.distributed,model_data_pickle.Average_Order_Wait_Time.where(model_data_pickle['distributed']==1),label='DM')
plt.scatter(model_data_pickle.distributed,model_data_pickle.Average_Order_Wait_Time.where(model_data_pickle['distributed']==0),label='CM')
plt.title('Average_Order_Wait_Time')
plt.legend()
plt.show()

plt.scatter(model_data_pickle.distributed,model_data_pickle.Messages_Sent.where(model_data_pickle['distributed']==1),label='DM')
plt.scatter(model_data_pickle.distributed,model_data_pickle.Messages_Sent.where(model_data_pickle['distributed']==0),label='CM')
plt.title('Messages_Sent')
plt.legend()
plt.show()
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Late_Orders.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Late_Orders.where(model_data_pickle['distributed']==0),label='CM')
# plt.title('Late_Orders')
# plt.legend()
# plt.show()

# plt.scatter(model_data_pickle.distributed,model_data_pickle.Max_Messages_Sent.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Max_Messages_Sent.where(model_data_pickle['distributed']==0),label='CM')
# plt.title('Max_Messages_Sent')
# plt.legend()
# plt.show()
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Max_Messages_Received.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Max_Messages_Received.where(model_data_pickle['distributed']==0),label='CM')
# plt.title('Max_Messages_Received')
# plt.legend()
# plt.show()
# plt.scatter(agent_data_pickle.id,agent_data_pickle.id)
# plt.show()

# TODO: these tests are agent based, not model based as you
# plt.scatter(model_data_pickle.distributed,model_data_pickle.WIP_Backlog)
# plt.title('WIP_Backlog')
# plt.show()


# # print(agent_data_pickle.head())

# # end_messages = agent_data_pickle.xs(5, level ="AgentID")
# # end_messages.messages_sent.plot()


# plt.show()