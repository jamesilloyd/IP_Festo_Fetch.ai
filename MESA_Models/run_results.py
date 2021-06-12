import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools

# page = 7
page = 4


# plt.scatter(model_data_pickle.schedulingType,model_data_pickle.Utilisation)
# plt.show()

# plt.scatter(model_data_pickle.schedulingType,model_data_pickle.Average_Order_Wait_Time)
# plt.show()
# writer = pd.ExcelWriter('Results12356.xlsx')

model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Block3/Test3/test_9/model_data.pkl'.format(page))


print(model_data_pickle)


# model_data_pickle.to_excel(writer,sheet_name = '{}_model'.format(i))



if(page == 4):

    '''TEST 4'''
    quantities = [10,20,50,100,150]
    newOrderProbability = [8,16,40,60,80]
    dueDateFactor = [1,1.5,2]

    plots = {
        'Utilisation':model_data_pickle.Utilisation,
        'Successful Orders':model_data_pickle.SuccessfulOrders,
        'Average Messages Sent':model_data_pickle.AverageMessagesSent,
    }

    # First show them all on their own, then show the the tradeoff
    fig = plt.figure()
    i = 1
    colors = ['r','g','b']
    index = 0
    element = 1

    for plot in plots.keys():
        ax = fig.add_subplot(1,3,i,projection='3d')
        i += 1
        # ax.scatter(model_data_pickle.newOrderProbability.where(model_data_pickle['dueDateFactor']==element),model_data_pickle.quantity.where(model_data_pickle['dueDateFactor']==element),plots[plot].where(model_data_pickle['dueDateFactor']==element),label=str(element),color=colors[index])
        ax.scatter(model_data_pickle.newOrderProbability,model_data_pickle.quantity,plots[plot],color=colors[index])
        index += 1
        ax.set(xlabel = 'New Order Prob',ylabel = 'Quantity', zlabel = plot)

    # plt.legend()

    plt.show()

    plots = {
        'Utilisation':model_data_pickle.Utilisation,
        'Successful Orders':model_data_pickle.SuccessfulOrders,
    }

    fig = plt.figure()
    colors = ['r','g']
    index = 0
    element = 1

    ax = fig.add_subplot(111,projection='3d')

    for plot in plots.keys():
        # ax.scatter(model_data_pickle.newOrderProbability.where(model_data_pickle['dueDateFactor']==element),model_data_pickle.quantity.where(model_data_pickle['dueDateFactor']==element),plots[plot].where(model_data_pickle['dueDateFactor']==element),label=plot,color=colors[index])
        ax.scatter(model_data_pickle.newOrderProbability,model_data_pickle.quantity,plots[plot],label=plot,color=colors[index])
        index += 1
        ax.set(xlabel = 'Quantity',ylabel = 'New Order Probability')

    plt.legend()
    plt.show()

if(page == 7):

    quantity = [10,20,50,100,150] 
    newOrderProbability = [40,80]
    plots1 = {
        'AverageSuccessfulOrderPriceCheap':model_data_pickle.AverageSuccessfulOrderPriceCheap,
        'AverageSuccessfulOrderPriceNeutral':model_data_pickle.AverageSuccessfulOrderPriceNeutral,
        'AverageSuccessfulOrderPriceAsap':model_data_pickle.AverageSuccessfulOrderPriceAsap,
    }
    plots2 = {
        'AverageSuccessfulOrderMakespanCheap':model_data_pickle.AverageSuccessfulOrderMakespanCheap,
        'AverageSuccessfulOrderMakespanNeutral':model_data_pickle.AverageSuccessfulOrderMakespanNeutral,
        'AverageSuccessfulOrderMakespanAsap':model_data_pickle.AverageSuccessfulOrderMakespanAsap,
    }

    
    colors = ['r','g','b']
    legend = ['cheap','neutral','asap']
    index = 0

    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    
    for plot in plots1.keys():
        
        ax.scatter(model_data_pickle.newOrderProbability,model_data_pickle.quantity,plots1[plot],label=legend[index],color=colors[index])
        index += 1
        ax.set(xlabel = 'New Order Probability',ylabel = 'Quantity',zlabel = 'Price')

    
    plt.legend()
    plt.show()
    
    colors = ['r','g','b']
    legend = ['cheap','neutral','asap']
    index = 0

    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    
    for plot in plots2.keys():
        
        ax.scatter(model_data_pickle.newOrderProbability,model_data_pickle.quantity,plots2[plot],label=legend[index],color=colors[index])
        index += 1
        ax.set(xlabel = 'New Order Probability',ylabel = 'Quantity',zlabel = 'Makespan')

    
    plt.legend()
    plt.show()



'''TEST 5'''
# TEST 5
requirementWeights = [1,0.8,0.5,0.2,0]
# plots = {
#     'Utilisation':model_data_pickle.Utilisation,
#     'Successful Orders':model_data_pickle.SuccessfulOrders,
#     'Average Satisfaction Score':model_data_pickle.AverageSatisfactionScore,
#     'Average Successful Price':model_data_pickle.AverageSuccessfulPrice,
#     'Average Successful Makespan':model_data_pickle.AverageSuccessfulMakespan,
    
#     'Messages Sent':model_data_pickle.MessagesSent,
#     'Late Orders':model_data_pickle.LateOrders,
#     'WIP Backlog':model_data_pickle.WIPBacklog,
#     'Average Order Wait time':model_data_pickle.AverageOrderWaitTime,
    
# }


# # TEST 6
# for plot in plots.keys():
#     plt.scatter(model_data_pickle.requirementWeights,plots[plot])
#     plt.title(plot)
#     plt.show()




# # writer.save()
# # writer.close()

# # DF TO CSV
# # yourdf.to_csv('PythonExport.csv', sep=',')

# # resultsFile16 = open('resultsFile16',"w")
# # resultsFile16.write('tray - part - type - description\n')

# # resultsFile16.write('{0} - {1} - {2} - {3}\n'.format(tray,part,ty,fault))
# # resultsFile16.close()

# # scheduling = quantity
# # quantity = scheduling
# # plt.scatter(model_data_pickle.splitSize,model_data_pickle.Utilisation)
# # plt.show()