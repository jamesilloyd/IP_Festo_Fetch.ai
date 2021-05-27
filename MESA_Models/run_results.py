import pandas as pd
from matplotlib import pyplot as plt


# TODO: have way of changing this path


# plt.scatter(model_data_pickle.schedulingType,model_data_pickle.Utilisation)
# plt.show()

# plt.scatter(model_data_pickle.schedulingType,model_data_pickle.Average_Order_Wait_Time)
# plt.show()
# writer = pd.ExcelWriter('Results12356.xlsx')

model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Block3/Test2/test_1/model_data.pkl')


print(model_data_pickle)

# model_data_pickle.to_excel(writer,sheet_name = '{}_model'.format(i))
    
# writer.save()
# writer.close()

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

# "Utilisation": utilisation.machine_utilisation, 
#                 "Complete_Orders": orders.ordersComplete,
#                 'Average_Order_Wait_Time': orders.averageOrderWaitTime, 
#                 "Successful_Orders":orders.successfulOrders,
#                 'Messages_Sent': messages.messagesSent, 
#                 'Late_Orders':orders.lateOrders,
#                 'WIP_Backlog':orders.totalWIPSize, 
#                 'Max_Messages_Sent': messages.maxMessagesSentFromNode, 
#                 'Max_Messages_Received': messages.maxMessagesReceivedByNode},

# plt.subplot(3,2,1)
plt.scatter(model_data_pickle.method,model_data_pickle.Utilisation)
plt.title('Utilisation')
plt.show()
plt.scatter(model_data_pickle.method,model_data_pickle.Average_Order_Wait_Time)
plt.title('Wait Time')
plt.show()
plt.scatter(model_data_pickle.method,model_data_pickle.Successful_Orders)
plt.title('Successful Orders')
plt.show()
plt.scatter(model_data_pickle.method,model_data_pickle.Late_Orders)
plt.title('Late Orders')
plt.show()
plt.scatter(model_data_pickle.method,model_data_pickle.WIP_Backlog)
plt.title('Backlog')
plt.show()