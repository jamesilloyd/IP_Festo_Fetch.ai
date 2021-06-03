import pandas as pd
from matplotlib import pyplot as plt


# plt.scatter(model_data_pickle.schedulingType,model_data_pickle.Utilisation)
# plt.show()

# plt.scatter(model_data_pickle.schedulingType,model_data_pickle.Average_Order_Wait_Time)
# plt.show()
# writer = pd.ExcelWriter('Results12356.xlsx')

model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Block3/Test3/test_0/model_data.pkl')


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

plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Utilisation)
plt.title('Utilisation')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Average_Order_Wait_Time)
plt.title('Wait Time')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Successful_Orders)
plt.title('Successful Orders')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Late_Orders)
plt.title('Late Orders')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Outsourced_Orders)
plt.title('Outsourced Orders')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Successful_Order_Price_Average)
plt.title('Successful_Order_Price_Average')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Successful_Order_Price_ASAP_Agent)
plt.title('Successful_Order_Price_ASAP_Agent')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Successful_Order_Price_Cheap_Agent)
plt.title('Successful_Order_Price_Cheap_Agent')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Successful_Order_Makespan_Average)
plt.title('Successful_Order_Makespan_Average')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Successful_Order_Makespan_ASAP_Agent)
plt.title('Successful_Order_Makespan_ASAP_Agent')
plt.show()
plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.Successful_Order_Makespan_Cheap_Agent)
plt.title('Successful_Order_Makespan_Cheap_Agent')
plt.show()

plt.scatter(model_data_pickle.proportion_of_weights,model_data_pickle.WIP_Backlog)
plt.title('Backlog')
plt.show()