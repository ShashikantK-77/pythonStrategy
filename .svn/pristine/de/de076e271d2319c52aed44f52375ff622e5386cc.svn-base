# import pandas as pd

# # Load the data
# file_path = "orders.csv"  # Use a relative path if the file is in the same directory

# # Function to calculate PnL and net PnL percentage difference
# def calculate_pnl(df):
#     # Filter relevant columns
#     df_filtered = df[['strategy_id', 'OrderCategory', 'orderStatus', 'transactionType', 'ExecutionPrice']]
    
#     # Find all unique strategies
#     strategies = df['strategy_id'].unique()
    
#     # Initialize dictionary to store pnl results for each strategy
#     strategy_pnl = {}
    
#     for strategy in strategies:
#         print(f"Calculating PnL for strategy: {strategy}")
        
#         # Filter orders for the current strategy
#         df_strategy = df[df['strategy_id'] == strategy]
        
#         # Find the main order (buy order)
#         main_order = df_strategy[(df_strategy['OrderCategory'] == 'Entry') & (df_strategy['transactionType'] == 'BUY')]
        
#         # If no main order found, continue to next strategy
#         if main_order.empty:
#             print(f"No main order found for strategy: {strategy}. Skipping...")
#             continue
        
#         # Get the buy price from the main order
#         buy_price = main_order['ExecutionPrice'].values[0]
        
#         # Initialize netpnl for the first row where mainorder is found
#         df.loc[df_strategy.index[0], 'netpnl'] = 0.0
        
#         # Find bookprofit or stoploss orders that are successful and sell orders
#         sell_orders = df_strategy[(df_strategy['OrderCategory'].isin(['Target', 'stop_loss'])) & 
#                                   (df_strategy['orderStatus'] == 'SUCCESS') & 
#                                   (df_strategy['transactionType'] == 'SELL')]
        
#         # Calculate PnL for each sell order and update dictionary
#         for index, sell_order in sell_orders.iterrows():
#             sell_price = sell_order['price']
#             print("sell_price, buy_price:",sell_price, buy_price)
#             pnl = sell_price - buy_price
#             pnl_percentage = (pnl / buy_price) * 100  # Calculate PnL percentage
#             if strategy in strategy_pnl:
#                 strategy_pnl[strategy] += pnl
#             else:
#                 strategy_pnl[strategy] = pnl
                
            
#             # Calculate net PnL percentage difference (percentage change)
#             df.loc[index, 'netpnl'] = pnl_percentage
        
#         print(f"Strategy {strategy} PnL: {strategy_pnl[strategy]}")
    
#     # Calculate total PnL and total net PnL percentage difference
#     total_pnl = df['pnl'].sum()
#     initial_investment = df.loc[df['OrderCategory'] == 'Entry', 'ExecutionPrice'].sum()  # Total initial investment (sum of all main order prices)
#     total_netpnl_percentage = (total_pnl / initial_investment) * 100
    
#     print(f"\nTotal PnL: {total_pnl}")
#     print(f"Total Net PnL Percentage: {total_netpnl_percentage}%")
    
#     # Update original DataFrame with calculated pnl for each strategy
#     for strategy, pnl in strategy_pnl.items():
#         df.loc[df['strategy_id'] == strategy, 'pnl'] = pnl
#         df.loc[df['strategy_id'] == strategy, 'netpnl'] = df.loc[df['strategy_id'] == strategy, 'netpnl']  # Update netpnl as calculated
    
#     return df

# # Load the data
# df = pd.read_csv(file_path)

# # Calculate PnL and update DataFrame
# df = calculate_pnl(df)

# # Save the updated DataFrame back to the CSV file (overwrite existing data)
# df.to_csv(file_path, index=False)

# print("PnL and net PnL percentage difference updated in orders.csv successfully.")




import pandas as pd

# Load the data
file_path = "orders.csv"  # Use a relative path if the file is in the same directory

# Function to calculate PnL and net PnL percentage difference
def calculate_pnl(df):
    # Filter relevant columns
    df_filtered = df[['strategy_id', 'OrderCategory', 'orderStatus', 'transactionType', 'ExecutionPrice']]
    
    # Find all unique strategies
    strategies = df['strategy_id'].unique()
    
    # Initialize dictionary to store pnl results for each strategy
    strategy_pnl = {}
    
    for strategy in strategies:
        print(f"Calculating PnL for strategy: {strategy}")
        
        # Filter orders for the current strategy
        df_strategy = df[df['strategy_id'] == strategy]
        
        # Find the main order (buy order)
        main_order = df_strategy[(df_strategy['OrderCategory'] == 'Entry') & (df_strategy['transactionType'] == 'BUY')]
        
        # If no main order found, continue to next strategy
        if main_order.empty:
            print(f"No main order found for strategy: {strategy}. Skipping...")
            continue
        
        # Get the buy price from the main order
        buy_price = main_order['ExecutionPrice'].values[0]
        
        # Initialize netpnl for the first row where mainorder is found
        df.loc[df_strategy.index[0], 'netpnl'] = 0.0
        
        # Find bookprofit or stoploss orders that are successful and sell orders
        sell_orders = df_strategy[(df_strategy['OrderCategory'].isin(['Target', 'stop_loss'])) & 
                                  (df_strategy['orderStatus'] == 'TRADED') & 
                                  (df_strategy['transactionType'] == 'SELL')]
        
        # Calculate PnL for each sell order and update dictionary
        for index, sell_order in sell_orders.iterrows():
            sell_price = sell_order['ExecutionPrice']
            print("sell_price, buy_price:", sell_price, buy_price)
            pnl = sell_price - buy_price
            pnl_percentage = (pnl / buy_price) * 100  # Calculate PnL percentage
            if strategy in strategy_pnl:
                strategy_pnl[strategy] += pnl
            else:
                strategy_pnl[strategy] = pnl
                
            # Calculate net PnL percentage difference (percentage change)
            df.loc[index, 'netpnl'] = pnl_percentage
        
        if strategy in strategy_pnl:
            print(f"Strategy {strategy} PnL: {strategy_pnl[strategy]}")
        else:
            print(f"No PnL calculated for strategy: {strategy}")
    
    # Calculate total PnL and total net PnL percentage difference
    total_pnl = df['pnl'].sum() if 'pnl' in df.columns else 0
    initial_investment = df.loc[df['OrderCategory'] == 'Entry', 'ExecutionPrice'].sum()  # Total initial investment (sum of all main order prices)
    total_netpnl_percentage = (total_pnl / initial_investment) * 100 if initial_investment != 0 else 0
    
    print(f"\nTotal PnL: {total_pnl}")
    print(f"Total Net PnL Percentage: {total_netpnl_percentage}%")
    
    # Update original DataFrame with calculated pnl for each strategy
    for strategy, pnl in strategy_pnl.items():
        df.loc[df['strategy_id'] == strategy, 'pnl'] = pnl
        df.loc[df['strategy_id'] == strategy, 'netpnl'] = df.loc[df['strategy_id'] == strategy, 'netpnl']  # Update netpnl as calculated
    
    return df

# Load the data
df = pd.read_csv(file_path)

# Calculate PnL and update DataFrame
df = calculate_pnl(df)

# Save the updated DataFrame back to the CSV file (overwrite existing data)
df.to_csv(file_path, index=False)

print("PnL and net PnL percentage difference updated in orders.csv successfully.")
