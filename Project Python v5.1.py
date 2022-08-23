# -*- coding: utf-8 -*-
"""
Group members :
    
    MOHAMAD DAKKOURI
    YOUSSEF EL BQAQ
    BASMA EL KHAMLICHI
    HOOMAN HALABICHIAN
    SHEHAB RASLAN
    SATNAM SINGH


##############################################################################
##############################################################################

ORDER BOOK PROJECT

STEP 1 : GENERATE A RANDOM ORDER BOOK 
STEP 2 : GENERATE RANDOM ORDER TO INTERACTE WITH THE ORDER BOOK 
BONUS PART : HANDLING THE ORDER i.e IF Limit or Market, if Buy or Sell 

##############################################################################
##############################################################################
"""
import numpy as np
import pandas as pd
import random
from datetime import datetime
import time 
startTime = time.time()

'''
##############################################################################
##############################################################################

STEP 1  :
    in this part we have set up some functions to produce a random order book

##############################################################################
##############################################################################
'''

#### We build different functions to build a random order book : 
def adapt_date(x) :
    import numpy as np
    import random
    x=x.replace("/","")
    x=x.replace(" ","")
    x=x.replace(":","")
    x= x + str(int(np.random.randint(1,100,[1,1])))
    return x

# We use a function to generate random ID for limit price in the orderbook

def Gen_Id(Side, Length_List) :
    if Side in ["S","s"] :
        x="S"
    elif Side in ["B","b"] :
        x="B"
    Data=[]
    for i in np.random.choice(1000000, replace=False, size=Length_List) :
        i=str(i)
        Data.append(x+i)
    return Data

# We use a function to generate random series for limit price in the orderbook
def Gen_Px(Index_Start, Index_End, Px_Start,Px_End, indicator ) :# Indicator is a boolean Argument(True if ascending sort)
    import random
    Gen_List=[]
    for i in range(Index_Start,Index_End) : 
        i=random.uniform(Px_Start,Px_End)
        i=round(i,3)
        Gen_List.append(i)
    Gen_List=sorted(Gen_List, reverse=indicator)
    return Gen_List

# We use a function to generate random order quantity for each order 
def Gen_Quantity(index_start, index_end) :
    Data=[]
    for i in range(index_start, index_end) :
        i=random.randrange(10,1000,5) #Here we assume that the qty in the order book can be settled from 10 to 1000 with a step of 5
        Data.append(i)
    return Data

# We use a function to generate random order date & time for each order 
def Gen_rdm(index_start, index_end):
    import random
    import numpy as np
    data = []
    for i in range(index_start,index_end):
        d = int(np.random.randint(1,28,[1,1]))
        m = int(np.random.randint(1,12,[1,1]))
        h = int(np.random.randint(1,24,[1,1]))
        mi =int(np.random.randint(0,60,[1,1]))
        s = int(np.random.randint(0,60,[1,1]))
        #Random day
        d = int(d)
        if d < 10:
            d = str(d)
            d = '0' + d + '/'
        else:
            d = str(d)
            d = d+'/'
        # Random month
        m = int(m)
        if m < 10:
            m = str(m)
            m = '0' + m + '/'
        else:
            m = str(m)
            m = m + '/'      
        # Random hour
        h = int(h)
        if h < 10 :
            h = str(h)
            h = '0' + h + ':'
        else:
            h = str(h)
            h = h + ':'
        # Random minute
        mi = int(mi)
        if mi < 10:
            mi = str(mi)
            mi = '0' + mi + ':'
        else:
            mi = str(mi)
            mi = mi + ':'
        # Random Second 
        s = int(s)
        if s < 10:
            s = str(s)
            s = '0' + s
        else:
            s = str(s)
            s = s
        data.append([d,m,"2021 ",h,mi,s]) # We assume that all order are dated from 2021 (not before)
    timeColumns=[]
    for i in data:
        i_Time = i[0] + i[1] + i[2] + i[3] + i[4] + i[5]
        timeColumns.append(i_Time)
    return timeColumns

##################################################################################################
# We start by building list for each  columns of our order book 
# We will then transform all these list in 2 data frame (one for all the buy orders / another for the sell orders) and merge them
# Our order book will contain the following columns : id for buy order / date & time of buy order / Qty of buy order / Price for buy order  (and the same columns for sell side)
##################################################################################################

#Parameters
#  x & y are parameters to generate 5000 random orders 
x = 1 
y = 5001
#RandomPrice_A = int(np.random.randint(1, 3500, [1, 1])) #Here we can assign a random price that will be used to build our order book // We assume that our stock price can here is not a penny stock and can reach a price of 3500 (like AMZN)
RandomPrice_A = 40

#Build Buy orders 
#### Lists for buy orders 
list_BuyOrdersIds = Gen_Id('B', y)
list_BuyOrdersPx = Gen_Px(x, y, RandomPrice_A, RandomPrice_A-3, True ) # All the buy orders will be generate in a price range of 37 - 40 hence the RandomPrice_A-3
list_BuyOrdersDateTime = Gen_rdm(x,y)
list_BuyOrdersQty = Gen_Quantity(x,y) 

# Buy Orders List convert into a DF 
list_BuyOrders = [] 
for i , j , k , l in zip(list_BuyOrdersIds, list_BuyOrdersDateTime, list_BuyOrdersQty, list_BuyOrdersPx): 
    list_BuyOrders.append([i, j, k, l]) 
df_BuyOrders_col = ["B_ID", "B_Time", "B_Qty", "B_Price"]
df_BuyOrders = pd.DataFrame(list_BuyOrders, columns = df_BuyOrders_col)
df_BuyOrders["B_Time"] = pd.to_datetime(df_BuyOrders["B_Time"])  # Convert the random date & time generated list in date format
df_BuyOrders.sort_values(["B_Price","B_Time"], ascending = (False,True), inplace = True, ignore_index = True)

#Build Sell orders 
#### Lists for sell orders 
list_SellOrdersIds = Gen_Id("S",y)
list_SellOrdersPx = Gen_Px(x,y, RandomPrice_A + (RandomPrice_A * 0.01), RandomPrice_A + 2, False ) # # All the sell orders will be generate in a price range of  40 * (1+0.01%) to 42 hence RandomPrice_A + 2  
# # 0.001 = our initial bid/ask spread correspond to 1% of the random price generated/choosen 
list_SellOrdersDateTime = Gen_rdm(x,y)
list_BuyOrdersQty = Gen_Quantity(x,y)

# Sell Orders List convert into a DF 
list_SellOrders = []
for e,f,g,h in zip(list_SellOrdersPx, list_BuyOrdersQty, list_SellOrdersDateTime, list_SellOrdersIds):
    list_SellOrders.append([e,f,g,h])
df_SellOrders_col = ["S_Price","S_Qty","S_Time","S_ID"]
df_SellOrders = pd.DataFrame(list_SellOrders, columns = df_SellOrders_col) # Convert the random date & time generated list in date format
df_SellOrders["S_Time"] = pd.to_datetime(df_SellOrders["S_Time"])
df_SellOrders.sort_values(["S_Price", "S_Time"], ascending = (True, True), inplace = True, ignore_index = True)

########################## Merging Data Frame Sell Orders & Buy Orders 
df_OrderBook = pd.concat([df_BuyOrders,df_SellOrders], axis = 1, ignore_index= True)
df_OrderBook_Columns = ["B_ID","B_Time","B_Qty","B_Price","S_Price","S_Qty","S_Time","S_ID"]
df_OrderBook.columns = df_OrderBook_Columns

df_OrderBook #Display all the df
df_OrderBook.head(10) # display the 10 first lines
    
'''
##############################################################################
##############################################################################

STEP 2 :
    in this part we generate 5000 random orders (Buy or Sell, Limit or Market)

##############################################################################
##############################################################################
'''    

for i in range(1,5000): #We generate 5000 random orders i.e. Limit buy or Market Buy or Limit Sell or Market Sell
    import random
    import numpy as np
    mu = 0.05
    n = 1
    M = 200
    T = 1
    dt = T/M
    x0 = 100
    nb_samples = 100
    sigma = 0.3

    z = np.exp((mu - sigma ** 2 / 2) * dt + sigma * np.random.normal(0, np.sqrt(dt), size=(1, n)).T)
    z = x0*z
    z.shape
    
    x = bool(random.getrandbits(1))
    if x == 1:
        orderType = 'L'
        #orderPxLimit = random.randrange(37, 42) # Above we have set a price range from 37 to 42 
        orderPxLimit =float(z)
    else:
        orderType = 'M'
    
    x = bool(random.getrandbits(1))        
    if x == 1:
        orderSide = 'B'
    else:
        orderSide = 'S'    
    
    orderTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    orderId = orderSide + orderType + adapt_date(orderTime)
    orderQty = random.randrange(10,1000,5)
    
    best_BuyOrderPx = df_BuyOrders.iloc[0,3]
    best_BuyOrderQty = df_BuyOrders.iloc[0,2] 
    best_SellOrderPx = df_SellOrders.iloc[0,0]
    best_SellOrderQty = df_SellOrders.iloc[0,1]
    orderExecutionPx = 0
    list_TradesParam = [] # List of parameters to add in the text file
    txtFile_Path = r"C:\Users\ssatn\Desktop\trades.txt"
    
    bid_ask_spread = best_SellOrderPx - best_BuyOrderPx 
    
    # Function to add the trade in a txt file
    def AddTxtFile(arg_list, filePath):
        obj_file = open(filePath, 'a')
        df_TradesParamAsString = pd.DataFrame([arg_list])
        df_TradesParamAsString = df_TradesParamAsString.to_string(header=False, index=False)
        obj_file.write(df_TradesParamAsString + "\n")
        obj_file.close()
    
    if orderSide in ["S","s"]: #if it's a sell order 
        
        if orderType in ["L","l"] and orderPxLimit > best_BuyOrderPx : 
            
            # Adding the new order in a list 
            L_S_New_Order = [orderPxLimit, orderQty, orderTime, orderId] 
            # Adding the limit order in the order book 
            df_SellOrders_col = ["S_Price","S_Qty","S_Time","S_ID"]
            df_SellOrders.loc[df_SellOrders.shape[0]+1,df_SellOrders.columns]=L_S_New_Order
            df_SellOrders["S_Time"] = pd.to_datetime(df_SellOrders["S_Time"])  # Convert the random date & time generated  in date format
            df_SellOrders.sort_values(["S_Price", "S_Time"], ascending = (True, True), inplace = True, ignore_index = True)
        
        else: #i.e if (orderType in ['M','m']) or (orderType in ['l,'L']) and orderPxLimit <= (best_BuyOrderPx) we execute the order as a market order
       
            orderResidualQty = orderQty
            orderExecutionPx = best_BuyOrderPx # For the execution price we assume that there is no "broker fees" 
            
            if orderQty < best_BuyOrderQty:
                #Add the trade in the text file
                tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                list_TradesParam = [df_BuyOrders.iloc[0,0], ';', df_BuyOrders.iloc[0,1], ';', orderQty, ';', orderExecutionPx,';', orderExecutionPx, ';',orderQty, ';', orderTime, ';', orderId,';', tradeExecutionTime,';', bid_ask_spread] 
                AddTxtFile(list_TradesParam, txtFile_Path)
                orderResidualQty = best_BuyOrderQty - orderQty    
                df_BuyOrders.iloc[0,2] = orderResidualQty
         
            elif orderQty == best_BuyOrderQty:
                #Add the trade in the text file
                tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                list_TradesParam = [df_BuyOrders.iloc[0,0], ';', df_BuyOrders.iloc[0,1], ';', orderQty, ';', orderExecutionPx,';', orderExecutionPx, ';',orderQty, ';', orderTime, ';', orderId,';', tradeExecutionTime,';', bid_ask_spread] 
                AddTxtFile(list_TradesParam, txtFile_Path)
                df_BuyOrders.drop(0, 0, inplace = True)
                df_BuyOrders.reset_index(drop = "True", inplace=True)
    
            else:
                while orderResidualQty >= best_BuyOrderQty:
                    orderExecutionPx = best_BuyOrderPx
                    orderResidualQty = orderResidualQty - best_BuyOrderQty
                    tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    list_TradesParam = [df_BuyOrders.iloc[0,0],';', df_BuyOrders.iloc[0,1],';', best_BuyOrderQty,';', orderExecutionPx,';', orderExecutionPx,';', best_BuyOrderQty,';', orderTime,';', orderId,';', tradeExecutionTime,';', bid_ask_spread] 
                    #Add the trade in the text file
                    AddTxtFile(list_TradesParam, txtFile_Path)
                    df_BuyOrders.drop(0, 0, inplace = True)
                    df_BuyOrders.reset_index(drop = "True", inplace=True)
                    best_BuyOrderPx = df_BuyOrders.iloc[0,3]
                    best_BuyOrderQty = df_BuyOrders.iloc[0,2]
                    bid_ask_spread = best_SellOrderPx - best_BuyOrderPx
                orderExecutionPx = best_BuyOrderPx
                tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                #Add the trade in the text file
                list_TradesParam = [df_BuyOrders.iloc[0,0],';', df_BuyOrders.iloc[0,1],';', orderResidualQty,';', orderExecutionPx,';', orderExecutionPx,';', orderResidualQty,';', orderTime,';', orderId,';', tradeExecutionTime,';', bid_ask_spread] 
                AddTxtFile(list_TradesParam, txtFile_Path)
                orderResidualQty = best_BuyOrderQty - orderResidualQty  
                df_BuyOrders.iloc[0,2] = orderResidualQty
                
    elif orderSide in ["B","b"] : #If it's  a  Buy order     
        
        if orderType in ["L","l"] and orderPxLimit < best_SellOrderPx :
            
            # Adding the new order in a list 
            L_B_New_Order = [orderId, orderTime, orderQty, orderPxLimit] 
            # Adding the limit order in the order book          
            df_BuyOrders_col = ["B_ID","B_Time","B_Qty","B_Price"]
            df_BuyOrders.loc[df_BuyOrders.shape[0]+1,df_BuyOrders.columns]=L_B_New_Order
            df_BuyOrders["B_Time"] = pd.to_datetime(df_BuyOrders["B_Time"]) # Convert the random date & time generated in date format
            df_BuyOrders.sort_values(["B_Price","B_Time"], ascending = (False,True), inplace = True, ignore_index = True)
            
        else: #i.e if (orderType in ['M','m'] or orderType in ['l,'L']) and orderPxLimit >= best_BuyOrderPx  we execute the order as a market order
            orderResidualQty = orderQty
            orderExecutionPx = best_SellOrderPx # For the execution price we assume that there is no "broker fees" 
            
            if orderQty < best_SellOrderQty:
                tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                list_TradesParam = [orderId,';', orderTime,';', orderQty,';', orderExecutionPx,';', orderExecutionPx,';', orderQty,';', df_SellOrders.iloc[0,2],';', df_SellOrders.iloc[0,3],';', tradeExecutionTime,';', bid_ask_spread] 
                AddTxtFile(list_TradesParam, txtFile_Path)
                orderResidualQty = best_SellOrderQty - orderQty    
                df_SellOrders.iloc[0,1] = orderResidualQty
                
            elif orderQty == best_SellOrderQty:
                tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                list_TradesParam = [orderId,';', orderTime,';', orderQty, ';', orderExecutionPx,';', orderExecutionPx,';', orderQty,';', df_SellOrders.iloc[0,2],';', df_SellOrders.iloc[0,3], ';',tradeExecutionTime,';', bid_ask_spread] 
                #Add the trade in the text file
                AddTxtFile(list_TradesParam, txtFile_Path)
                df_SellOrders.drop(0, 0, inplace = True)
                df_SellOrders.reset_index(drop = "True", inplace=True)
                
            else:
                while orderResidualQty >= best_SellOrderQty:
                    orderExecutionPx = best_SellOrderPx
                    orderResidualQty = orderResidualQty - best_SellOrderQty
                    tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    list_TradesParam = [orderId,';', orderTime,';', best_SellOrderQty, ';', orderExecutionPx, ';',orderExecutionPx, ';', best_SellOrderQty, ';',df_SellOrders.iloc[0,2], ';',df_SellOrders.iloc[0,3], ';',tradeExecutionTime,';', bid_ask_spread] 
                    #Add the trade in the text file
                    AddTxtFile(list_TradesParam, txtFile_Path)
                    df_SellOrders.drop(0, 0, inplace = True)
                    df_SellOrders.reset_index(drop = "True", inplace=True)
                    best_SellOrderPx = df_SellOrders.iloc[0,0]
                    best_SellOrderQty = df_SellOrders.iloc[0,1]
                    bid_ask_spread = best_SellOrderPx - best_BuyOrderPx
                orderExecutionPx = best_SellOrderPx
                tradeExecutionTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                #Add the trade in the text file
                list_TradesParam = [orderId,';', orderTime,';', orderResidualQty, ';',orderExecutionPx,';', orderExecutionPx,';', orderResidualQty,';', df_SellOrders.iloc[0,2], ';', df_SellOrders.iloc[0,3],';', tradeExecutionTime,';', bid_ask_spread] 
                AddTxtFile(list_TradesParam, txtFile_Path)
                orderResidualQty = best_SellOrderQty - orderResidualQty   
                df_SellOrders.iloc[0,1] = orderResidualQty

########################## Merge the DF of sell and buy orders

df_OrderBook = pd.concat([df_BuyOrders, df_SellOrders], axis = 1, ignore_index = True)
df_OrderBook_Columns=["B_ID","B_Time","B_Qty","B_Price","S_Price","S_Qty","S_Time","S_ID"]
df_OrderBook.columns = df_OrderBook_Columns       

df_OrderBook
df_OrderBook.head(10)

endTime = time.time()
print('Time elapsed to generate : ' + str(endTime-startTime))

'''
##############################################################################
##############################################################################

BONUS PART  :
    in this part we have set up some functions to handle all the input from 
    the user 

##############################################################################
##############################################################################
'''

best_BuyOrderPx = df_BuyOrders.iloc[0,3]
best_BuyOrderQty = df_BuyOrders.iloc[0,2] 
best_SellOrderPx = df_SellOrders.iloc[0,0]
best_SellOrderQty = df_SellOrders.iloc[0,1]
orderExecutionPx = 0
list_TradesParam = [] # List of parameters to add in the text file
txtFile_Path = r"C:\Users\ssatn\Desktop\trades.txt"

bid_ask_spread = best_SellOrderPx - best_BuyOrderPx 

# We ask the user to enter the order type with error handling (user can only input M or L):
test = True
while test:
    orderType = input('Please enter the order type (M for market order ; L for Limit Order) : ')
    if orderType == '' or orderType not in ['M','L','m','l']:
        print('Incorrect input ! Please only input M for market order or L for Limit Order).')
        test = True
    else:
        break
        
# We ask the user to enter the order side with error handling (user can only input S or B)
test = True
while test:
    orderSide = input('Please enter the order side (B for BUY ; S for SELL) : ')
    if orderSide == '' or orderSide not in ['S','B','s','b'] :
        print('Incorrect input ! Please only input B for BUY or S for SELL).')
        test = True
    else:
        break
        
# We ask the user to enter the quantity with error handling (only an integer)
test = True
while test:
    try:
        orderQty = int(input('Quantity : '))
        break
    except:
        print('Incorrect Quantity Input ! You have to put an integer value. Please try again.')
        test = True
        
# We ask the user to enter the limit price with error handling (if he select a Limit order)
if orderType in ['L','l'] :
    test = True
    while test:
        try:
            orderPxLimit = float(input('Price Limit : '))
            orderPxLimit = round(orderPxLimit, 3) #Here we assume that the tick size is 0.001
            break
        except:
            print('Incorrect price input ! Please try again.')
            test = True
            
# Once the user has finished to enter all the parameters, we state the order time
from datetime import datetime
orderTime = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

if orderSide in ["B","b"]:
    orderId = "B" + adapt_date(orderTime)
elif orderSide in ["S","s"]:
    orderId = "S"+ adapt_date(orderTime)



if orderSide in ["S","s"]: #if it's a sell order 
    
    if orderType in ["L","l"] and orderPxLimit > best_BuyOrderPx : 
        
        # Adding the new order in a list 
        L_S_New_Order = [orderPxLimit, orderQty, orderTime, orderId] 
        # Adding the limit order in the order book 
        df_SellOrders_col = ["S_Price","S_Qty","S_Time","S_ID"]
        df_SellOrders.loc[df_SellOrders.shape[0]+1,df_SellOrders.columns]=L_S_New_Order
        df_SellOrders["S_Time"] = pd.to_datetime(df_SellOrders["S_Time"])  # Convert the random date & time generated  in date format
        df_SellOrders.sort_values(["S_Price", "S_Time"], ascending = (True, True), inplace = True, ignore_index = True)
    
    else: #i.e if (orderType in ['M','m']) or (orderType in ['l,'L']) and orderPxLimit <= (best_BuyOrderPx) we execute the order as a market order
   
        orderResidualQty = orderQty
        orderExecutionPx = best_BuyOrderPx # For the execution price we assume that there is no "broker fees" 
        
        if orderQty < best_BuyOrderQty:
            #Add the trade in the text file
            tradeExecutionTime = datetime.now()
            list_TradesParam = [df_BuyOrders.iloc[0,0], df_BuyOrders.iloc[0,1], orderQty, orderExecutionPx, orderExecutionPx, orderQty, orderTime, orderId, tradeExecutionTime, bid_ask_spread] 
            AddTxtFile(list_TradesParam, txtFile_Path)
            orderResidualQty = best_BuyOrderQty - orderQty    
            df_BuyOrders.iloc[0,2] = orderResidualQty
     
        elif orderQty == best_BuyOrderQty:
            #Add the trade in the text file
            tradeExecutionTime = datetime.now()
            list_TradesParam = [df_BuyOrders.iloc[0,0], df_BuyOrders.iloc[0,1], orderQty, orderExecutionPx, orderExecutionPx, orderQty, orderTime, orderId, tradeExecutionTime, bid_ask_spread] 
            AddTxtFile(list_TradesParam, txtFile_Path)
            df_BuyOrders.drop(0, 0, inplace = True)
            df_BuyOrders.reset_index(drop = "True", inplace=True)

        else:
            while orderResidualQty >= best_BuyOrderQty:
                orderExecutionPx = best_BuyOrderPx
                orderResidualQty = orderResidualQty - best_BuyOrderQty
                tradeExecutionTime = datetime.now()
                list_TradesParam = [df_BuyOrders.iloc[0,0], df_BuyOrders.iloc[0,1], best_BuyOrderQty, orderExecutionPx, orderExecutionPx, orderQty, orderTime, orderId, tradeExecutionTime, bid_ask_spread] 
                #Add the trade in the text file
                AddTxtFile(list_TradesParam, txtFile_Path)
                df_BuyOrders.drop(0, 0, inplace = True)
                df_BuyOrders.reset_index(drop = "True", inplace=True)
                best_BuyOrderPx = df_BuyOrders.iloc[0,3]
                best_BuyOrderQty = df_BuyOrders.iloc[0,2]
                bid_ask_spread = best_SellOrderPx - best_BuyOrderPx
            orderExecutionPx = best_BuyOrderPx
            tradeExecutionTime = datetime.now()
            #Add the trade in the text file
            list_TradesParam = [df_BuyOrders.iloc[0,0], df_BuyOrders.iloc[0,1], best_BuyOrderQty, orderExecutionPx, orderExecutionPx, orderQty, orderTime, orderId, tradeExecutionTime, bid_ask_spread] 
            AddTxtFile(list_TradesParam, txtFile_Path)
            orderResidualQty = best_BuyOrderQty - orderResidualQty  
            df_BuyOrders.iloc[0,2] = orderResidualQty
            
elif orderSide in ["B","b"] : #If it's  a  Buy order     
    
    if orderType in ["L","l"] and orderPxLimit < best_SellOrderPx :
        
        # Adding the new order in a list 
        L_B_New_Order = [orderId, orderTime, orderQty, orderPxLimit] 
        # Adding the limit order in the order book          
        df_BuyOrders_col = ["B_ID","B_Time","B_Qty","B_Price"]
        df_BuyOrders.loc[df_BuyOrders.shape[0]+1,df_BuyOrders.columns]=L_B_New_Order
        df_BuyOrders["B_Time"] = pd.to_datetime(df_BuyOrders["B_Time"]) # Convert the random date & time generated in date format
        df_BuyOrders.sort_values(["B_Price","B_Time"], ascending = (False,True), inplace = True, ignore_index = True)
        
    else: #i.e if (orderType in ['M','m'] or orderType in ['l,'L']) and orderPxLimit >= best_BuyOrderPx  we execute the order as a market order
        orderResidualQty = orderQty
        orderExecutionPx = best_SellOrderPx # For the execution price we assume that there is no "broker fees" 
        
        if orderQty < best_SellOrderQty:
            tradeExecutionTime = datetime.now()
            list_TradesParam = [orderId, orderTime, orderQty, orderExecutionPx, orderExecutionPx, orderQty, df_SellOrders.iloc[0,2], df_SellOrders.iloc[0,3], tradeExecutionTime, bid_ask_spread] 
            AddTxtFile(list_TradesParam, txtFile_Path)
            orderResidualQty = best_SellOrderQty - orderQty    
            df_SellOrders.iloc[0,1] = orderResidualQty
            
        elif orderQty == best_SellOrderQty:
            tradeExecutionTime = datetime.now()
            list_TradesParam = [orderId, orderTime, orderQty, orderExecutionPx, orderExecutionPx, orderQty, df_SellOrders.iloc[0,2], df_SellOrders.iloc[0,3], tradeExecutionTime, bid_ask_spread] 
            #Add the trade in the text file
            AddTxtFile(list_TradesParam, txtFile_Path)
            df_SellOrders.drop(0, 0, inplace = True)
            df_SellOrders.reset_index(drop = "True", inplace=True)
            
        else:
            while orderResidualQty >= best_SellOrderQty:
                orderExecutionPx = best_SellOrderPx
                orderResidualQty = orderResidualQty - best_SellOrderQty
                tradeExecutionTime = datetime.now()
                list_TradesParam = [orderId, orderTime, orderQty, orderExecutionPx, orderExecutionPx, orderQty, df_SellOrders.iloc[0,2], df_SellOrders.iloc[0,3], tradeExecutionTime, bid_ask_spread] 
                #Add the trade in the text file
                AddTxtFile(list_TradesParam, txtFile_Path)
                df_SellOrders.drop(0, 0, inplace = True)
                df_SellOrders.reset_index(drop = "True", inplace=True)
                best_SellOrderPx = df_SellOrders.iloc[0,0]
                best_SellOrderQty = df_SellOrders.iloc[0,1]
                bid_ask_spread = best_SellOrderPx - best_BuyOrderPx
            orderExecutionPx = best_SellOrderPx
            tradeExecutionTime = datetime.now()
            #Add the trade in the text file
            list_TradesParam = [orderId, orderTime, orderQty, orderExecutionPx, orderExecutionPx, orderQty, df_SellOrders.iloc[0,2], df_SellOrders.iloc[0,3], tradeExecutionTime, bid_ask_spread] 
            AddTxtFile(list_TradesParam, txtFile_Path)
            orderResidualQty = best_SellOrderQty - orderResidualQty   
            df_SellOrders.iloc[0,1] = orderResidualQty

########################## Merge the DF of sell and buy orders

df_OrderBook = pd.concat([df_BuyOrders, df_SellOrders], axis = 1, ignore_index = True)
df_OrderBook_Columns=["B_ID","B_Time","B_Qty","B_Price","S_Price","S_Qty","S_Time","S_ID"]
df_OrderBook.columns = df_OrderBook_Columns       

df_OrderBook
df_OrderBook.head(10)