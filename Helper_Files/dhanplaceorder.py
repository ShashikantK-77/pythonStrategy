# from dhanhq import dhanhq
# from Helper_Files.strategy_combiner import update_strategy_status
# from Helper_Files.save_executed_order import save_executed_order
# from Helper_Files.Risk_management import place_stop_loss_order,place_book_profit_order
# from dhanhq import dhanhq
# from Helper_Files.strategy_combiner import update_strategy_status,increment_operation_count
# from Helper_Files.save_executed_order import save_executed_order
# from Helper_Files.Risk_management import place_stop_loss_order, place_book_profit_order
# from Helper_Files.send_error_log import send_error_log
# from constants import access_token,client_id
# import logging


# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')




# dhan = dhanhq(client_id, access_token)

# # Define the mapping for action_name to transaction_type
# TRANSACTION_TYPE_MAP = {
#     'buy': dhan.BUY,
#     'sell': dhan.SELL,
# }

# # Define the mapping for exchange to exchange_segment
# EXCHANGE_SEGMENT_MAP = {
#     'NSE': dhan.NSE,
#     'BSE': dhan.BSE,
#     # Add more exchanges as needed
# }
# from Helper_Files.get_latest_ltp import get_latest_ltp

# def dhan_place_order(action, strategy_id, strategy_data, security_id):
#     # logging.debug(f"Placing single order in dhan_place_order for strategy_data by Shashikant...: {strategy_data}")
#     # logging.debug(f"Placing single order action...: {action}")ssss
    
#     # logging.debug(f"Placing security_id order buy...: {security_id}")
#     latest_ltp = get_latest_ltp(security_id)
#     # logging.debug(f"The data type of latest_ltp is: {type(latest_ltp)}")

#     try:
#         for action in action:
#             # Now `action` is a dictionary, so you can access `action_name`
#             logging.debug(f"Performing action: {action['action_name']}")
          

#         # Use the provided security_id
#         quantity = action.get('quantity', 1)  # Default to 1 if not provided
#         product_type = dhan.INTRA  # Assuming INTRA; update if necessary
#         price = action.get('price', 0)  # Default to 0 if not provided
#         order_type = dhan.MARKET if action['action_type'] == 'market' else dhan.LIMIT
        
#         # Set transaction_type dynamically based on action_name
#         transaction_type = TRANSACTION_TYPE_MAP.get(action['action_name'].lower(), dhan.BUY)
        
#         # Set exchange_segment dynamically based on strategy data
#         exchange_segment = EXCHANGE_SEGMENT_MAP.get(strategy_data['strategy']['exchange'], dhan.NSE)
        
#         logging.debug(f"Placing order with the following details: "
#                       f"Security ID: {security_id}, "
#                       f"Quantity: {quantity}, "
#                       f"Product Type: {product_type}, "
#                       f"Price: {price}, "
#                       f"Order Type: {order_type}, "
#                       f"Transaction Type: {transaction_type}, "
#                       f"Exchange Segment: {exchange_segment}")
        
#         # Handle different action types
#         if action['action_type'] == 'Bracket':
#             logging.debug("Placing Bracket order...")
#             response = dhan.place_order(
#                 transaction_type=transaction_type,
#                 exchange_segment=exchange_segment,
#                 product_type=product_type,
#                 order_type=dhan.BO,
#                 validity='DAY',
#                 security_id=security_id,
#                 quantity=quantity,
#                 price=price,
#                 bo_profit_value=action.get('BracketTarget', 0),
#                 bo_stop_loss_Value=action.get('BracketStopLoss', 0)
#             )
#         elif action['action_type'] == 'limit':
#             logging.debug("Placing Limit order...")
#             response = dhan.place_order(
#                 transaction_type=transaction_type,
#                 exchange_segment=exchange_segment,
#                 product_type=product_type,
#                 order_type=dhan.LIMIT,
#                 validity='DAY',
#                 security_id=security_id,
#                 quantity=quantity,
#                 price=action.get('price', 0),
#             )
#         elif action['action_type'] == 'cover':
#             logging.debug("Placing Cover order...")
#             response = dhan.place_order(
#                 transaction_type=transaction_type,
#                 exchange_segment=exchange_segment,
#                 product_type=product_type,
#                 order_type=dhan.COVER,
#                 validity='DAY',
#                 security_id=security_id,
#                 quantity=quantity,
#                 price=price,
#                 bo_profit_value=action.get('BracketTarget', 0),
#                 bo_stop_loss_Value=action.get('BracketStopLoss', 0)
#             )
#         elif action['action_type'] == 'trigger':
#             logging.debug("Placing Trigger order...")
#             response = dhan.place_order(
#                 transaction_type=transaction_type,
#                 exchange_segment=exchange_segment,
#                 product_type=product_type,
#                 order_type=dhan.TRIGGER,
#                 validity='DAY',
#                 security_id=security_id,
#                 quantity=quantity,
#                 price=action.get('price', 0),
#             )
#         elif action['action_type'] == 'market':
#             logging.debug("Placing Market order...")
#             response = dhan.place_order(
#                 security_id=security_id,
#                 exchange_segment=exchange_segment,
#                 transaction_type=transaction_type,
#                 quantity=quantity,
#                 order_type=order_type,
#                 product_type=dhan.INTRA,
#                 price=price,
#             )

#     if response['status'] == 'success' and 'data' in response:
#         order_data = response['data']
#         order_status = order_data.get('orderStatus')

#     if order_status in ['TRADED', 'PENDING', 'TRANSIT']:  # Modify based on your success criteria
#         if 'orderId' in order_data:
#             order_id = order_data['orderId']
#             logging.debug(f"Order placed successfully. Order ID: {order_id}, Status: {order_status}")

#             try:
#                 order_details = dhan.get_order_by_id(order_id)
#                 logging.debug(f"Fetched Order Details: {order_details}")

#                 save_executed_order(order_details, strategy_id, latest_ltp, ordertype="Entry")
#                 logging.debug(f"Executed order saved for strategy {strategy_id} with LTP: {latest_ltp}")

#                 update_strategy_status(strategy_id)
#                 logging.debug(f"Updated strategy status for strategy {strategy_id}")

#                 increment_operation_count(strategy_id)
#                 logging.debug(f"Incremented operation count for strategy {strategy_id}")

#                 place_book_profit_order(order_details, strategy_id, latest_ltp, strategy_data, action)
#                 logging.debug("Placed book profit order")

#                 place_stop_loss_order(order_details, strategy_id, latest_ltp, strategy_data, action)
#                 logging.debug("Placed stop loss order")

#             except Exception as e:
#                 logging.error(f"Error fetching order details or placing additional orders: {e}")
#                 send_error_log(f"Error processing order {order_id}: {e}", 'place_order')

#         else:
#             logging.error("Order ID missing in successful response")
#             send_error_log("Missing order ID in successful response", 'place_order')
#     else:
#         logging.error(f"Unexpected order status: {order_status}")
#         send_error_log(f"Unexpected order status: {order_status}", 'place_order')
# else:
#     logging.error(f"Failed to place order for {action['action_name']}. Response: {response}")
#     send_error_log(f"Failed to place order for {action['action_name']}: {response}", 'place_order')

# ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

# from dhanhq import dhanhq
# from Helper_Files.strategy_combiner import update_strategy_status, increment_operation_count
# from Helper_Files.save_executed_order import save_executed_order
# from Helper_Files.Risk_management import place_stop_loss_order, place_book_profit_order
# from Helper_Files.send_error_log import send_error_log
# from constants import access_token, client_id
# import logging
# from Helper_Files.get_latest_ltp import get_latest_ltp

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# dhan = dhanhq(client_id, access_token)

# # Define the mapping for action_name to transaction_type
# TRANSACTION_TYPE_MAP = {
#     'buy': dhan.BUY,
#     'sell': dhan.SELL,
# }

# # Define the mapping for exchange to exchange_segment
# EXCHANGE_SEGMENT_MAP = {
#     'NSE': dhan.NSE,
#     'BSE': dhan.BSE,
#     # Add more exchanges as needed
# }

# def dhan_place_order(action, strategy_id, strategy_data, security_id):
#     # Get the latest LTP (Last Traded Price)
#     latest_ltp = get_latest_ltp(security_id)

#     try:
#         for act in action:
#             logging.debug(f"Performing action: {act['action_name']}")

#             # Use the provided security_id
#             quantity = act.get('quantity', 1)  # Default to 1 if not provided
#             product_type = dhan.INTRA  # Assuming INTRA; update if necessary
#             price = act.get('price', 0)  # Default to 0 if not provided
#             order_type = dhan.MARKET if act['action_type'] == 'market' else dhan.LIMIT

#             # Set transaction_type dynamically based on action_name
#             transaction_type = TRANSACTION_TYPE_MAP.get(act['action_name'].lower(), dhan.BUY)

#             # Set exchange_segment dynamically based on strategy data
#             exchange_segment = EXCHANGE_SEGMENT_MAP.get(strategy_data['strategy']['exchange'], dhan.NSE)

#             logging.debug(f"Placing order with the following details: "
#                           f"Security ID: {security_id}, "
#                           f"Quantity: {quantity}, "
#                           f"Product Type: {product_type}, "
#                           f"Price: {price}, "
#                           f"Order Type: {order_type}, "
#                           f"Transaction Type: {transaction_type}, "
#                           f"Exchange Segment: {exchange_segment}")

#             # Handle different action types
#             if act['action_type'] == 'Bracket':
#                 logging.debug("Placing Bracket order...")
#                 response = dhan.place_order(
#                     transaction_type=transaction_type,
#                     exchange_segment=exchange_segment,
#                     product_type=product_type,
#                     order_type=dhan.BO,
#                     validity='DAY',
#                     security_id=security_id,
#                     quantity=quantity,
#                     price=price,
#                     bo_profit_value=act.get('BracketTarget', 0),
#                     bo_stop_loss_Value=act.get('BracketStopLoss', 0)
#                 )
#             elif act['action_type'] == 'limit':
#                 logging.debug("Placing Limit order...")
#                 response = dhan.place_order(
#                     transaction_type=transaction_type,
#                     exchange_segment=exchange_segment,
#                     product_type=product_type,
#                     order_type=dhan.LIMIT,
#                     validity='DAY',
#                     security_id=security_id,
#                     quantity=quantity,
#                     price=act.get('price', 0),
#                 )
#             elif act['action_type'] == 'cover':
#                 logging.debug("Placing Cover order...")
#                 response = dhan.place_order(
#                     transaction_type=transaction_type,
#                     exchange_segment=exchange_segment,
#                     product_type=product_type,
#                     order_type=dhan.COVER,
#                     validity='DAY',
#                     security_id=security_id,
#                     quantity=quantity,
#                     price=price,
#                     bo_profit_value=act.get('BracketTarget', 0),
#                     bo_stop_loss_Value=act.get('BracketStopLoss', 0)
#                 )
#             elif act['action_type'] == 'trigger':
#                 logging.debug("Placing Trigger order...")
#                 response = dhan.place_order(
#                     transaction_type=transaction_type,
#                     exchange_segment=exchange_segment,
#                     product_type=product_type,
#                     order_type=dhan.TRIGGER,
#                     validity='DAY',
#                     security_id=security_id,
#                     quantity=quantity,
#                     price=act.get('price', 0),
#                 )
#             elif act['action_type'] == 'market':
#                 logging.debug("Placing Market order...")
#                 response = dhan.place_order(
#                     security_id=security_id,
#                     exchange_segment=exchange_segment,
#                     transaction_type=transaction_type,
#                     quantity=quantity,
#                     order_type=order_type,
#                     product_type=dhan.INTRA,
#                     price=price,
#                 )

#             if response['status'] == 'success' and 'data' in response:
#                 order_data = response['data']
#                 order_status = order_data.get('orderStatus')
#                 # logging.debug(f"Order placed successfully. Order ID: {order_id}, Status very first time is: {order_status}")
#                 if order_status in ['TRADED', 'PENDING', 'TRANSIT']:  # Modify based on your success criteria
#                     if 'orderId' in order_data:
#                         order_id = order_data['orderId']
#                         logging.debug(f"Order placed successfully. Order ID: {order_id}, Status: {order_status}")

#                         try:
#                             order_details = dhan.get_order_by_id(order_id)
#                             logging.debug(f"Fetched Order Details: {order_details}")

#                             save_executed_order(order_details, strategy_id, latest_ltp, ordertype="Entry")
#                             logging.debug(f"Executed order saved for strategy {strategy_id} with LTP: {latest_ltp}")

#                             update_strategy_status(strategy_id)
#                             logging.debug(f"Updated strategy status for strategy {strategy_id}")

#                             increment_operation_count(strategy_id)
#                             logging.debug(f"Incremented operation count for strategy {strategy_id}")

#                             place_book_profit_order(order_details, strategy_id, latest_ltp, strategy_data, act)
#                             logging.debug("Placed book profit order")

#                             place_stop_loss_order(order_details, strategy_id, latest_ltp, strategy_data, act)
#                             logging.debug("Placed stop loss order")

#                         except Exception as e:
#                             logging.error(f"Error fetching order details or placing additional orders: {e}")
#                             send_error_log(f"Error processing order {order_id}: {e}", 'place_order')

#                     else:
#                         logging.error("Order ID missing in successful response")
#                         send_error_log("Missing order ID in successful response", 'place_order')
#                 else:
#                     logging.error(f"Unexpected order status: {order_status}")
#                     send_error_log(f"Unexpected order status: {order_status}", 'place_order')
#             else:
#                 logging.error(f"Failed to place order for {act['action_name']}. Response: {response}")
#                 send_error_log(f"Failed to place order for {act['action_name']}: {response}", 'place_order')

#     except Exception as e:
#         logging.error(f"Error in placing order: {e}")
#         send_error_log(f"Error placing order: {e}", 'place_order')



# ```````````````````````````````````without handling recheck```````````````````````````````````````````````




# from dhanhq import dhanhq
# from Helper_Files.strategy_combiner import update_strategy_status, increment_operation_count
# from Helper_Files.save_executed_order import save_executed_order
# from Helper_Files.Risk_management import place_stop_loss_Dhan, place_Target_Dhan
# from Helper_Files.send_error_log import send_error_log
# from constants import access_token, client_id
# import logging
# from Helper_Files.get_latest_ltp import get_latest_ltp

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# dhan = dhanhq(client_id, access_token)

# # Define the mapping for action_name to transaction_type
# TRANSACTION_TYPE_MAP = {
#     'buy': dhan.BUY,
#     'sell': dhan.SELL,
# }

# # Define the mapping for exchange to exchange_segment
# EXCHANGE_SEGMENT_MAP = {
#     'NSE': dhan.NSE,
#     'BSE': dhan.BSE,
#     # Add more exchanges as needed
# }

# def dhan_place_order(action, strategy_id, strategy_data, security_id):
#     # Get the latest LTP (Last Traded Price)
#     latest_ltp = get_latest_ltp(security_id)

#     try:
#         for act in action:
#             logging.debug(f"Performing action: {act['action_name']}")

#             # Use the provided security_id
#             quantity = act.get('quantity', 1)  # Default to 1 if not provided
#             product_type = dhan.INTRA  # Assuming INTRA; update if necessary
#             price = act.get('price', 0)  # Default to 0 if not provided
#             order_type = dhan.MARKET if act['action_type'] == 'market' else dhan.LIMIT

#             # Set transaction_type dynamically based on action_name
#             transaction_type = TRANSACTION_TYPE_MAP.get(act['action_name'].lower(), dhan.BUY)

#             # Set exchange_segment dynamically based on strategy data
#             exchange_segment = EXCHANGE_SEGMENT_MAP.get(strategy_data['strategy']['exchange'], dhan.NSE)

#             logging.debug(f"Placing order with the following details: "
#                           f"Security ID: {security_id}, "
#                           f"Quantity: {quantity}, "
#                           f"Product Type: {product_type}, "
#                           f"Price: {price}, "
#                           f"Order Type: {order_type}, "
#                           f"Transaction Type: {transaction_type}, "
#                           f"Exchange Segment: {exchange_segment}")

#             response = None
#             if act['action_type'] == 'market':
#                 logging.debug("Placing Market order...")
#                 response = dhan.place_order(
#                     security_id=security_id,
#                     exchange_segment=exchange_segment,
#                     transaction_type=transaction_type,
#                     quantity=quantity,
#                     order_type=order_type,
#                     product_type=dhan.INTRA,
#                     price=price,
#                 )
#             elif act['action_type'] == 'limit':
#                 logging.debug("Placing Limit order...")
#                 response = dhan.place_order(
#                     transaction_type=transaction_type,
#                     exchange_segment=exchange_segment,
#                     product_type=product_type,
#                     order_type=dhan.LIMIT,
#                     validity='DAY',
#                     security_id=security_id,
#                     quantity=quantity,
#                     price=act.get('price', 0),
#                 )
#             elif act['action_type'] == 'cover':
#                 logging.debug("Placing Cover order...")
#                 response = dhan.place_order(
#                     transaction_type=transaction_type,
#                     exchange_segment=exchange_segment,
#                     product_type=product_type,
#                     order_type=dhan.COVER,
#                     validity='DAY',
#                     security_id=security_id,
#                     quantity=quantity,
#                     price=price,
#                     bo_profit_value=act.get('BracketTarget', 0),
#                     bo_stop_loss_Value=act.get('BracketStopLoss', 0)
#                 )
#             elif act['action_type'] == 'trigger':
#                 logging.debug("Placing Trigger order...")
#                 response = dhan.place_order(
#                     transaction_type=transaction_type,
#                     exchange_segment=exchange_segment,
#                     product_type=product_type,
#                     order_type=dhan.TRIGGER,
#                     validity='DAY',
#                     security_id=security_id,
#                     quantity=quantity,
#                     price=act.get('price', 0),
#                 )

#             if response and response['status'] == 'success' and 'data' in response:
#                 order_data = response['data']
#                 order_status = order_data.get('orderStatus', 'UNKNOWN')
#                 logging.debug(f"Initial Order Status: {order_status}")
#                 increment_operation_count(strategy_id)

#                 if order_status == 'TRANSIT':
#                     # Fetch the updated order status
#                     try:
#                         order_id = order_data['orderId']
#                         order_details = dhan.get_order_by_id(order_id)
#                         logging.debug(f"Updated Order Details: {order_details}")
#                         order_status = order_details['data'].get('orderStatus', 'UNKNOWN')

#                         if order_status == 'REJECTED':
#                             logging.error(f"Order ID {order_id} was REJECTED: {order_details}")
#                             send_error_log(f"Order {order_id} rejected: {order_details}", 'place_order')
#                             return  # Exit the function early for REJECTED orders

#                     except Exception as e:
#                         logging.error(f"Error fetching updated order status for Order ID {order_id}: {e}")
#                         send_error_log(f"Error fetching updated order status for Order ID {order_id}: {e}", 'place_order')
#                         return

#                 if order_status in ['TRADED', 'PENDING']:
#                     logging.debug(f"Order ID {order_id} status is {order_status}. Proceeding...")
#                     try:
#                         save_executed_order(order_details, strategy_id, latest_ltp, ordertype="Entry")
#                         update_strategy_status(strategy_id)
                        
#                         place_Target_Dhan(order_details, strategy_id, latest_ltp, strategy_data, act)
#                         place_stop_loss_Dhan(order_details, strategy_id, latest_ltp, strategy_data, act)

                        
#                     except Exception as e:
#                         logging.error(f"Error processing successful order {order_id}: {e}")
#                         send_error_log(f"Error processing successful order {order_id}: {e}", 'place_order')
#                 else:
#                     logging.error(f"Unexpected final order status: {order_status}")
#                     send_error_log(f"Unexpected final order status: {order_status}", 'place_order')
#             else:
#                 logging.error(f"Failed to place order for {act['action_name']}. Response: {response}")
#                 send_error_log(f"Failed to place order for {act['action_name']}: {response}", 'place_order')

#     except Exception as e:
#         logging.error(f"Error in placing order: {e}")
#         send_error_log(f"Error placing order: {e}", 'place_order')


# ``````````````````````using while loop``````````````````

# from dhanhq import dhanhq
# from Helper_Files.strategy_combiner import update_strategy_status, increment_operation_count
# from Helper_Files.save_executed_order import save_executed_order
# from Helper_Files.Risk_management import place_stop_loss_Dhan, place_Target_Dhan
# from Helper_Files.send_error_log import send_error_log
# from constants import access_token, client_id
# import logging
# from Helper_Files.get_latest_ltp import get_latest_ltp

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# dhan = dhanhq(client_id, access_token)

# # Define the mapping for action_name to transaction_type
# TRANSACTION_TYPE_MAP = {
#     'buy': dhan.BUY,
#     'sell': dhan.SELL,
# }

# # Define the mapping for exchange to exchange_segment
# EXCHANGE_SEGMENT_MAP = {
#     'NSE': dhan.NSE,
#     'BSE': dhan.BSE,
#     # Add more exchanges as needed
# }

# import time

# def dhan_place_order(action, strategy_id, strategy_data, security_id):
#     # Get the latest LTP (Last Traded Price)
#     latest_ltp = get_latest_ltp(security_id)

#     try:
#         for act in action:
#             logging.debug(f"Performing action: {act['action_name']}")

#             # Extract order parameters
#             quantity = act.get('quantity', 1)
#             product_type = dhan.INTRA
#             price = act.get('price', 0)
#             order_type = dhan.MARKET if act['action_type'] == 'market' else dhan.LIMIT
#             transaction_type = TRANSACTION_TYPE_MAP.get(act['action_name'].lower(), dhan.BUY)
#             exchange_segment = EXCHANGE_SEGMENT_MAP.get(strategy_data['strategy']['exchange'], dhan.NSE)

#             logging.debug(f"Placing order with: Security ID: {security_id}, Quantity: {quantity}, Price: {price}, Order Type: {order_type}")

#             # Place order
#             response = dhan.place_order(
#                 security_id=security_id,
#                 exchange_segment=exchange_segment,
#                 transaction_type=transaction_type,
#                 quantity=quantity,
#                 order_type=order_type,
#                 product_type=product_type,
#                 price=price,
#             )

#             if response and response['status'] == 'success' and 'data' in response:
#                 order_data = response['data']
#                 order_id = order_data.get('orderId')
#                 order_status = order_data.get('orderStatus', 'UNKNOWN')
#                 logging.debug(f"Initial Order Status: {order_status}")
                
#                 increment_operation_count(strategy_id)

#                 # Wait and recheck for TRANSIT status
#                 while order_status == 'TRANSIT':
#                     time.sleep(5)  # Wait for 5 seconds before checking again
#                     try:
#                         order_details = dhan.get_order_by_id(order_id)
#                         order_status = order_details['data'].get('orderStatus', 'UNKNOWN')
#                         logging.debug(f"Updated Order Status: {order_status}")
#                     except Exception as e:
#                         logging.error(f"Error fetching updated status for Order ID {order_id}: {e}")
#                         send_error_log(f"Error fetching updated status for Order ID {order_id}: {e}", 'place_order')
#                         return

#                 # Process based on updated status
#                 if order_status in ['TRADED', 'PENDING']:
#                     logging.debug(f"Order ID {order_id} status is {order_status}. Proceeding with risk orders...")
#                     try:
#                         save_executed_order(order_details, strategy_id, latest_ltp, ordertype="Entry")
#                         update_strategy_status(strategy_id)

#                         # Place target and stop-loss orders
#                         place_Target_Dhan(order_details, strategy_id, latest_ltp, strategy_data, act)
#                         place_stop_loss_Dhan(order_details, strategy_id, latest_ltp, strategy_data, act)

#                     except Exception as e:
#                         logging.error(f"Error processing risk orders for Order ID {order_id}: {e}")
#                         send_error_log(f"Error processing risk orders for Order ID {order_id}: {e}", 'place_order')
#                 elif order_status == 'REJECTED':
#                     logging.error(f"Order ID {order_id} was rejected. Exiting...")
#                     send_error_log(f"Order {order_id} rejected: {order_data}", 'place_order')
#                     return
#                 else:
#                     logging.error(f"Unexpected order status: {order_status}")
#                     send_error_log(f"Unexpected order status: {order_status}", 'place_order')
#             else:
#                 logging.error(f"Failed to place order for {act['action_name']}. Response: {response}")
#                 send_error_log(f"Failed to place order for {act['action_name']}: {response}", 'place_order')

#     except Exception as e:
#         logging.error(f"Error in placing order: {e}")
#         send_error_log(f"Error placing order: {e}", 'place_order')




# ``````````````````````withot using while loop``````````````````


from dhanhq import dhanhq
from Helper_Files.strategy_combiner import update_strategy_status, increment_operation_count
from Helper_Files.save_executed_order import save_executed_order
from Helper_Files.Risk_management import place_stop_loss_Dhan, place_Target_Dhan
from Helper_Files.send_error_log import send_error_log
from constants import access_token, client_id
import logging
from Helper_Files.get_latest_ltp import get_latest_ltp

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

dhan = dhanhq(client_id, access_token)

# Define the mapping for action_name to transaction_type
TRANSACTION_TYPE_MAP = {
    'buy': dhan.BUY,
    'sell': dhan.SELL,
}

# Define the mapping for exchange to exchange_segment
EXCHANGE_SEGMENT_MAP = {
    'NSE': dhan.NSE,
    'BSE': dhan.BSE,
    # Add more exchanges as needed
}

import time

def dhan_place_order(action, strategy_id, strategy_data, security_id):
    # Get the latest LTP (Last Traded Price)
    latest_ltp = get_latest_ltp(security_id)

    try:
        for act in action:
            logging.debug(f"Performing action: {act['action_name']}")

            # Extract order parameters
            quantity = act.get('quantity', 1)
            product_type = dhan.INTRA
            price = act.get('price', 0)
            order_type = dhan.MARKET if act['action_type'] == 'market' else dhan.LIMIT
            transaction_type = TRANSACTION_TYPE_MAP.get(act['action_name'].lower(), dhan.BUY)
            exchange_segment = EXCHANGE_SEGMENT_MAP.get(strategy_data['strategy']['exchange'], dhan.NSE)

            logging.debug(f"Placing order with: Security ID: {security_id}, Quantity: {quantity}, Price: {price}, Order Type: {order_type}")

            # Place order
            response = dhan.place_order(
                security_id=security_id,
                exchange_segment=exchange_segment,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=order_type,
                product_type=product_type,
                price=price,
            )

            if response and response['status'] == 'success' and 'data' in response:
                order_data = response['data']
                order_id = order_data.get('orderId')
                order_status = order_data.get('orderStatus', 'UNKNOWN')
                logging.debug(f"Initial Order Status: {order_status}")
                
                increment_operation_count(strategy_id)

                # Retry mechanism for checking status
                max_retries = 10
                retry_interval = 5  # seconds

                for retry in range(max_retries):
                    if order_status not in ['TRANSIT']:
                        break
                    time.sleep(retry_interval)
                    try:
                        order_details = dhan.get_order_by_id(order_id)
                        order_status = order_details['data'].get('orderStatus', 'UNKNOWN')
                        logging.debug(f"Retry {retry + 1}: Updated Order Status: {order_status}")
                    except Exception as e:
                        logging.error(f"Error fetching updated status for Order ID {order_id}: {e}")
                        send_error_log(f"Error fetching updated status for Order ID {order_id}: {e}", 'place_order')
                        return

                # Process based on updated status
                if order_status in ['TRADED', 'PENDING']:
                    logging.debug(f"Order ID {order_id} status is {order_status}. Proceeding with risk orders...")
                    try:
                        # Extracting the price
                        order_details = dhan.get_order_by_id(order_id)
                        price = order_details['data']['price']

                        save_executed_order(order_details, strategy_id, price, ordertype="Entry")
                        update_strategy_status(strategy_id)

                        # Place target and stop-loss orders
                        place_Target_Dhan(order_details, strategy_id, price, strategy_data, act)
                        place_stop_loss_Dhan(order_details, strategy_id, price, strategy_data, act)

                    except Exception as e:
                        logging.error(f"Error processing risk orders for Order ID {order_id}: {e}")
                        send_error_log(f"Error processing risk orders for Order ID {order_id}: {e}", 'place_order')
                elif order_status == 'REJECTED':
                    logging.error(f"Order ID {order_id} was rejected. Exiting...")
                    send_error_log(f"Order {order_id} rejected: {order_data}", 'place_order')
                    return
                else:
                    logging.error(f"Unexpected order status: {order_status}")
                    send_error_log(f"Unexpected order status: {order_status}", 'place_order')
            else:
                logging.error(f"Failed to place order for {act['action_name']}. Response: {response}")
                send_error_log(f"Failed to place order for {act['action_name']}: {response}", 'place_order')

    except Exception as e:
        logging.error(f"Error in placing order: {e}")
        send_error_log(f"Error placing order: {e}", 'place_order')
