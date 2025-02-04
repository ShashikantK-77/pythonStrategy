# from dhanhq import dhanhq
# from Helper_Files.strategy_combiner import update_strategy_status
# from Helper_Files.save_executed_order import save_executed_order
# from Helper_Files.Risk_management import place_stop_loss_order,place_book_profit_order
# from dhanhq import dhanhq
# from Helper_Files.strategy_combiner import update_strategy_status,increment_operation_count
# from Helper_Files.save_executed_order import save_executed_order
# from Helper_Files.Risk_management import place_stop_loss_order, place_book_profit_order
# from Helper_Files.send_error_log import send_error_log
# import logging
# from Helper_Files.get_active_brokers import get_active_brokers

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# # Initialize DhanHQ client
# client_id = "1101343871"
# access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI4ODAxODg5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTM0Mzg3MSJ9.Rcr4VMpNakJvYB0ThB84v0DOaxiMRIZZoeqol8QAGEEgvPJJ3SpBsZVIyAcJvscOO3HPkx1fI0r6uZwV99V08g'

# #access_token = 'eyJ0eXAiOiJKV5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IRIZZoeqol8QAGEEgvPJJ3SpBsZVIyAcJvscOO3HPkx1fI0r6uZwV99V08g'



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

# def place_order(action, strategy_id, strategy_data, security_id):
#     logging.debug(f"Placing single order for strategy_data by Shashikant...: {strategy_data}")
#     logging.debug(f"Placing single order action...: {action}")
    
#     logging.debug(f"Placing security_id order buy...: {security_id}")
#     latest_ltp = get_latest_ltp(security_id)
#     latest_ltp = get_latest_ltp(security_id)
#     logging.debug(f"The data type of latest_ltp is: {type(latest_ltp)}")

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



#         # Handle response and save order
#         if response['status'] == 'success' and 'data' in response:
#             order_data = response['data']
#             if order_data.get('orderStatus') == 'TRANSIT' and 'orderId' in order_data:
#                 order_id = order_data['orderId']
#                 logging.debug(f"Order in transit. Order ID: {order_id}")

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

#                 # update_strategy_status(strategy_id)
#                 # logging.debug(f"Updated strategy status for strategy {strategy_id}")

#                 # increment_operation_count(strategy_id)
#                 # logging.debug(f"Incremented operation count for strategy {strategy_id}")
#             else:
#                 error_message = f"Failed to place order for {action['action_name']}. Response: {response}"
#                 logging.error(error_message)
#                 send_error_log(error_message, 'place_single_order')
#         else:
#             error_message = f"Failed to place order for {action['action_name']}. Response: {response}"
#             logging.error(error_message)
#             send_error_log(error_message, 'place_single_order')

#     except Exception as e:
#         error_message = f"Failed to place order for {action['action_name']}: {e}"
#         logging.error(error_message)
#         send_error_log(error_message, 'place_single_order')











import logging
from Helper_Files.get_active_brokers import get_active_brokers
from Helper_Files.dhanplaceorder import dhan_place_order  # Assuming you have this helper for Dhan

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def place_order_by_broker( action, strategy_id, strategy_data, security_id):
    logging.debug(f"in pace order by broker")
    brokers_info = get_active_brokers()  # Fetching active brokers
    for broker in brokers_info:
        current_broker_name = broker['broker_name']
        logging.debug(f"in pace order current_broker_name {current_broker_name}")
        if current_broker_name.lower() == 'alpaca':
            logging.debug(f"Placing order with Alpaca for action: {action}")
            # Uncomment and define place_alpaca_order if needed
            # place_alpaca_order(action, strategy_id, strategy_data, security_id)
        
        elif current_broker_name.lower() == 'dhan':
            # logging.debug(f"Placing order with Dhan for action: {action}")
            dhan_place_order(action, strategy_id, strategy_data, security_id)
        
        else:
            logging.error(f"Broker not supported: {current_broker_name}")
