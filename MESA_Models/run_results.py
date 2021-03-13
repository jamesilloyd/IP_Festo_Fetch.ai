import pandas as pd
from matplotlib import pyplot as plt


# TODO: have way of changing this path
agent_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Inter-Firm/test_19/agent_data.pkl')
model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Inter-Firm/test_19/model_data.pkl')

print(model_data_pickle)

writer = pd.ExcelWriter('PythonExport3.xlsx')
model_data_pickle.to_excel(writer,'Sheet5')
writer.save()

# DF TO CSV
# yourdf.to_csv('PythonExport.csv', sep=',')

# resultsFile16 = open('resultsFile16',"w")
# resultsFile16.write('tray - part - type - description\n')

# resultsFile16.write('{0} - {1} - {2} - {3}\n'.format(tray,part,ty,fault))
# resultsFile16.close()


# scheduling = quantity
# quantity = scheduling
# plt.scatter(model_data_pickle.splitSize,model_data_pickle.Utilisation)
# plt.show()

# # plt.subplot(3,2,1)
# # plt.scatter(model_data_pickle.splitSize,model_data_pickle.Utilisation.where(model_data_pickle['quantity']=='FIFO').where(model_data_pickle['schedulingType']==1),color='blue')
# plt.title('Utilisation')
# plt.xlabel('FIFO')
# plt.subplot(3,2,2)
# plt.scatter(model_data_pickle.splitSize,model_data_pickle.Utilisation.where(model_data_pickle['quantity']=='Moores').where(model_data_pickle['schedulingType']==1),color='red')
# plt.xlabel('Moores')
# plt.subplot(3,2,3)
# plt.scatter(model_data_pickle.splitSize,model_data_pickle.Utilisation.where(model_data_pickle['quantity']=='SPT').where(model_data_pickle['schedulingType']==1),color='green')
# plt.xlabel('SPT')
# plt.subplot(3,2,4)
# plt.scatter(model_data_pickle.splitSize,model_data_pickle.Utilisation.where(model_data_pickle['quantity']=='MDD').where(model_data_pickle['schedulingType']==1),color='black')
# plt.xlabel('MDD')
# plt.subplot(3,2,5)
# plt.scatter(model_data_pickle.splitSize,model_data_pickle.Utilisation.where(model_data_pickle['quantity']=='EDD').where(model_data_pickle['schedulingType']==1),color='orange')
# plt.xlabel('EDD')
# plt.tight_layout()
# plt.show()


# plt.scatter(model_data_pickle.distributed,model_data_pickle.Utilisation.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Utilisation.where(model_data_pickle['distributed']==0),label='CM')
# plt.title('Utilisation')
# plt.legend()
# plt.show()
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Complete_Orders.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Complete_Orders.where(model_data_pickle['distributed']==0),label='CM')

# plt.title('Total Successful Orders')
# plt.legend()
# plt.show()

# plt.scatter(model_data_pickle.distributed,model_data_pickle.Successful_Orders.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Successful_Orders.where(model_data_pickle['distributed']==0),label='CM')
# plt.title('% Successful Orders')
# plt.legend()
# plt.show()

# plt.scatter(model_data_pickle.distributed,model_data_pickle.Average_Order_Wait_Time.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Average_Order_Wait_Time.where(model_data_pickle['distributed']==0),label='CM')
# plt.title('Average_Order_Wait_Time')
# plt.legend()
# plt.show()

# plt.scatter(model_data_pickle.distributed,model_data_pickle.Messages_Sent.where(model_data_pickle['distributed']==1),label='DM')
# plt.scatter(model_data_pickle.distributed,model_data_pickle.Messages_Sent.where(model_data_pickle['distributed']==0),label='CM')
# plt.title('Messages_Sent')
# plt.legend()
# plt.show()
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