from mesa import model
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
# model_data_pickle.to_excel(writer,sheet_name = '{}_model'.format(i))
page = 7
# page = 4
page = 8
page = 9
page = 10
runningWeights = False


model_data_pickle = pd.read_pickle('/Users/heisenberg/IP/MESA_Models/results/Block3/Test3/test_{}/model_data.pkl'.format(page))



print(model_data_pickle)

if(page == 10):

    plots = {
            'Utilisation':model_data_pickle.Utilisation,
            'Successful Orders':model_data_pickle.SuccessfulOrders,
            'Average Messages Sent per Agent': model_data_pickle.AverageMessagesSent, 
            "noProposalOrders":model_data_pickle.noProposalOrders,
            'searchSize':model_data_pickle.searchSize,
            'LateOrders':model_data_pickle.LateOrders,}

    

    for plot in plots.keys():
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['quantity'] == 50),model_data_pickle.searchSize.where(model_data_pickle['quantity'] == 50),plots[plot].where(model_data_pickle['quantity'] == 50))
        ax.set(xlabel = 'Orders per week',ylabel = 'Search Size',zlabel = plot)
        plt.show()

    fig, (ax1,ax2) = plt.subplots(1,2)
    fig = plt.figure()
    ax1 = fig.add_subplot(1,2,1,projection ='3d')
    ax1.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['quantity'] == 50),model_data_pickle.searchSize.where(model_data_pickle['quantity'] == 50),model_data_pickle.Utilisation.where(model_data_pickle['quantity'] == 50))
    ax1.set_xlabel('Orders Per Week')
    ax1.set_ylabel('Search Size')
    ax1.set_zlabel('Utilisation')

    ax2 = fig.add_subplot(1,2,2,projection ='3d')
    ax2.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['quantity'] == 50),model_data_pickle.searchSize.where(model_data_pickle['quantity'] == 50),model_data_pickle.SuccessfulOrders.where(model_data_pickle['quantity'] == 50),color='g')
    ax2.set_xlabel('Orders Per Week')
    ax2.set_ylabel('Search Size')
    ax2.set_zlabel('Successful Orders')

    # ax3 = fig.add_subplot(1,2,3,projection ='3d')
    # ax3.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['quantity'] == 50),model_data_pickle.searchSize.where(model_data_pickle['quantity'] == 50),model_data_pickle.AverageMessagesSent.where(model_data_pickle['quantity'] == 50))
    # ax3.set_xlabel('Orders Per Week')
    # ax3.set_ylabel('Search Size')
    # ax3.set_zlabel('Average number of messages sent per agent')

    plt.show()





if(page == 9):
    if(not runningWeights):
        searchSize = [1,2]
        plots = {
            'Utilisation':model_data_pickle.Utilisation,
            'Successful Orders':model_data_pickle.SuccessfulOrders,
            'Average Messages Sent per Agent': model_data_pickle.AverageMessagesSent, 
            "noProposalOrders":model_data_pickle.noProposalOrders,
            'LateOrders':model_data_pickle.LateOrders,}

        for plot in plots.keys():
            fig = plt.figure()
            ax = fig.add_subplot(111,projection='3d')
            # ax.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['searchSize'] == 2),model_data_pickle.quantity.where(model_data_pickle['searchSize'] == 2),plots[plot].where(model_data_pickle['searchSize'] == 2),label = "50%")
            ax.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['searchSize'] == 1),model_data_pickle.quantity.where(model_data_pickle['searchSize'] == 1),plots[plot].where(model_data_pickle['searchSize'] == 1))
            ax.set(xlabel = 'Orders Per Week',ylabel = 'Quantity of Machines',zlabel = plot)
            # plt.legend()
            plt.show()
        
        fig, (ax1,ax2) = plt.subplots(1,2)

        fig = plt.figure()
        ax1 = fig.add_subplot(1,2,1,projection ='3d')

        ax1.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['searchSize'] == 1),model_data_pickle.quantity.where(model_data_pickle['searchSize'] == 1),model_data_pickle.Utilisation.where(model_data_pickle['searchSize'] == 1))
        ax1.set_xlabel('Orders Per Week')
        ax1.set_ylabel('Quantity of Machines')
        ax1.set_zlabel('Utilisation')
        ax2 = fig.add_subplot(1,2,2,projection ='3d')
        ax2.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['searchSize'] == 1),model_data_pickle.quantity.where(model_data_pickle['searchSize'] == 1),model_data_pickle.SuccessfulOrders.where(model_data_pickle['searchSize'] == 1),color='g')
        ax2.set_xlabel('Orders Per Week')
        ax2.set_ylabel('Quantity of Machines')
        ax2.set_zlabel('Successful Orders')
        plt.show()


        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        
        ax.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['searchSize'] == 1),model_data_pickle.quantity.where(model_data_pickle['searchSize'] == 1),model_data_pickle.Utilisation.where(model_data_pickle['searchSize'] == 1),label = 'Utilisation')
        ax.scatter(model_data_pickle.ordersPerWeek.where(model_data_pickle['searchSize'] == 1),model_data_pickle.quantity.where(model_data_pickle['searchSize'] == 1),model_data_pickle.SuccessfulOrders.where(model_data_pickle['searchSize'] == 1),label = "Successful Orders",color='g')
        ax.set(xlabel = 'Orders Per Week',ylabel = 'Quantity of Machines')
        plt.legend()
        plt.show()
        
        

        

    else:

        quantities = [10,20,50,80,100,120,150]
        newOrderProbability = [1,5,20,40,80,120]
        
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

        for x in newOrderProbability:
            index = 0
            
            # fig = plt.figure()
            fig, (ax1,ax2) = plt.subplots(1,2)

            for plot in plots1.keys():
                # Calculate averages and errors
                averages = []
                errors = []
                
                for quantity in quantities:
                    yaverage = 0
                    yn = 0
                    ysum = 0
                    sumdifferencesqured = 0

                    for value in plots1[plot].where(model_data_pickle['ordersPerWeek']==x).where(model_data_pickle['searchSize']==1).where(model_data_pickle['quantity']==quantity):
                        if value > 0:
                            yn += 1
                            ysum += value
                    
                    yaverage = ysum / yn

                    for value in plots1[plot].where(model_data_pickle['ordersPerWeek']==x).where(model_data_pickle['searchSize']==1).where(model_data_pickle['quantity']==quantity):
                        if value > 0:
                            sumdifferencesqured = (yaverage - value) **2
                    
                    ysd = (sumdifferencesqured / yn)**(0.5)
                    averages.append(yaverage)
                    errors.append(ysd)

                # plt.scatter(model_data_pickle.quantity.where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),plots1[plot].where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),label=legend[index],color=colors[index])
                # plt.errorbar(model_data_pickle.quantity.where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),plots1[plot].where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),label=legend[index],color=colors[index],linestyle='None')
                ax1.errorbar(quantities,averages,yerr=errors,label=legend[index],color=colors[index],fmt='o')
                ax1.set_xlabel('Quantity of machines')
                ax1.set_ylabel('Price')
                index += 1

            # plt.legend()
            # plt.show()
            
            index = 0

            # fig = plt.figure()

            for plot in plots2.keys():
                # Calculate averages and errors
                averages = []
                errors = []
                
                for quantity in quantities:
                    yaverage = 0
                    yn = 0
                    ysum = 0
                    sumdifferencesqured = 0

                    for value in plots2[plot].where(model_data_pickle['ordersPerWeek']==x).where(model_data_pickle['searchSize']==1).where(model_data_pickle['quantity']==quantity):
                        if value > 0:
                            yn += 1
                            ysum += value
                    
                    yaverage = ysum / yn

                    for value in plots2[plot].where(model_data_pickle['ordersPerWeek']==x).where(model_data_pickle['searchSize']==1).where(model_data_pickle['quantity']==quantity):
                        if value > 0:
                            sumdifferencesqured = (yaverage - value) **2
                    
                    ysd = (sumdifferencesqured / yn)**(0.5)
                    averages.append(yaverage)
                    errors.append(ysd)


                
                # plt.scatter(model_data_pickle.quantity.where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),plots1[plot].where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),label=legend[index],color=colors[index])
                # plt.errorbar(model_data_pickle.quantity.where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),plots1[plot].where(model_data_pickle['ordersPerWeek']==20).where(model_data_pickle['searchSize']==1),label=legend[index],color=colors[index],linestyle='None')
                ax2.errorbar(quantities,averages,yerr=errors,label=legend[index],color=colors[index],fmt='o')
                ax2.set_xlabel('Quantity of machines')
                ax2.set_ylabel('Makespan')
                index += 1

            plt.title("{} Orders Per Week".format(x))
            plt.legend()
            plt.show()

        


if(page == 8):

    plots = {
        'Utilisation':model_data_pickle.Utilisation,
        'Successful Orders':model_data_pickle.SuccessfulOrders,
        'AverageMessagesSent': model_data_pickle.AverageMessagesSent, 
        "noProposalOrders":model_data_pickle.noProposalOrders,
        'LateOrders':model_data_pickle.LateOrders,}

    for plot in plots.keys():
        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(model_data_pickle.newOrderProbability,model_data_pickle.quantity,plots[plot])
        
        ax.set(xlabel = 'Quantity',ylabel = 'New Order Probability',zlabel = plot)
        plt.show()

if(page == 4):

    '''TEST 4'''
    quantities = [10,20,50,100,150]
    newOrderProbability = [8,16,40,60,80]
    dueDateFactor = [1,1.5,2]

    plots = {
        'Utilisation':model_data_pickle.Utilisation,
        'Successful Orders':model_data_pickle.SuccessfulOrders,
        'Average Messages Sent':model_data_pickle.MessagesSent,
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

    # ax = fig.add_subplot(111,projection='3d')

    
    fig  = plt.figure()

    for plot in plots.keys():
        plt.scatter(model_data_pickle.newOrderProbability.where(model_data_pickle['quantity']==100),plots[plot].where(model_data_pickle['quantity']==100),label=plot,color=colors[index])
        plt.xlabel('New Order Probability')

        # ax.scatter(model_data_pickle.newOrderProbability.where(model_data_pickle['dueDateFactor']==element),model_data_pickle.quantity.where(model_data_pickle['dueDateFactor']==element),plots[plot].where(model_data_pickle['dueDateFactor']==element),label=plot,color=colors[index])
        index += 1
        # ax.set(xlabel = 'New Order Probability',ylabel = 'Quantity')

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

    
    # ax = fig.add_subplot(111,projection='3d')
    fig = plt.figure()
    
    for plot in plots1.keys():
        plt.scatter(model_data_pickle.quantity.where(model_data_pickle['newOrderProbability']==40),plots1[plot].where(model_data_pickle['newOrderProbability']==40),label=legend[index],color=colors[index])
        plt.xlabel('Quantity')
        plt.ylabel('Price')
        
        # ax.scatter(model_data_pickle.newOrderProbability,model_data_pickle.quantity,plots1[plot],label=legend[index],color=colors[index])
        index += 1
        # ax.set(xlabel = 'New Order Probability',ylabel = 'Quantity',zlabel = 'Price')

    
    plt.legend()
    plt.show()
    
    colors = ['r','g','b']
    legend = ['cheap','neutral','asap']
    index = 0

    fig = plt.figure()
    
    for plot in plots2.keys():
        plt.scatter(model_data_pickle.quantity.where(model_data_pickle['newOrderProbability']==40),plots2[plot].where(model_data_pickle['newOrderProbability']==40),label=legend[index],color=colors[index])
        plt.xlabel('Quantity')
        plt.ylabel('Makespan')
        
        index += 1

    
    plt.legend()
    plt.show()