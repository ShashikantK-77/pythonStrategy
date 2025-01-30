
from dhanhq import dhanhq

from Helper_Files.save_executed_order import save_executed_order
from Helper_Files.send_error_log import send_error_log
from Helper_Files.get_latest_ltp import get_latest_ltp
from constants import access_token,client_id

import logging
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

dhan = dhanhq(client_id, access_token)


# def place_stop_loss_order(order_details, strategy_id, latest_ltp, strategy_data, actions):
#     logging.debug(f"in place_stop_loss_order", order_details)
#     security_id = order_details['data']['securityId']
#     logging.debug(f"security_id in Risk_management.py: {security_id}")
#     latest_ltp = get_latest_ltp(security_id)
#     tick_size = 0.01
#     tick_size = float(tick_size)  # Ensure tick_size is a float

#     transaction_type = dhan.SELL if order_details['data']['transactionType'] == dhan.BUY else dhan.BUY
    
#     try:
#         stoploss_percent = float(actions.get('stoploss_percent', 1))  # Ensure stoploss_percent is a float

#     except ValueError as ve:
#         logging.error(f"Error converting stoploss_percent to float: {ve}")
#         return
    
#     MainOrderid = order_details['data']['orderId']
#     logging.debug(f"MainOrderid in Risk_management.py: {MainOrderid}")
#     logging.debug(f"order_details in Risk_management.py: {order_details}")
 

#     logging.debug(f"latest_ltp in place_stop_loss_order::{latest_ltp}")

#     try:
#         latest_ltp = float(latest_ltp)  # Ensure latest_ltp is a float
#     except ValueError as ve:
#         logging.error(f"Error converting latest_ltp to float: {ve}")
#         return

#     # Calculate stop_loss_price
#     stop_loss_price = latest_ltp - (latest_ltp * stoploss_percent / 100)
#     stop_loss_price = round(stop_loss_price / tick_size) * tick_size

#     # Fallback to a default value if stop_loss_price is zero or negative
#     if stop_loss_price <= 0:
#         stop_loss_price = 24.00

#     logging.debug(f"stop_loss_price in Risk_management.py: {stop_loss_price}")
#     send_error_log(f"stop_loss_price for strategy {strategy_id}: {stop_loss_price}", "Risk_management.py")
    
#     try:
#         response = dhan.place_order(
#             transaction_type=transaction_type,
#             exchange_segment=order_details['data']['exchangeSegment'],
#             product_type=order_details['data']['productType'],
#             order_type=dhan.LIMIT,
#             validity='DAY',
#             security_id=order_details['data']['securityId'],
#             quantity=order_details['data']['quantity'],
#             price=stop_loss_price
#         )
#         logging.debug(f"stop_loss order placed successfully for strategy {strategy_id}. Response: {response}")
        
#         if response['status'] == 'success' and 'data' in response:
#             order_data = response['data']
#             if order_data.get('orderStatus') == 'TRANSIT' and 'orderId' in order_data:
#                 order_id = order_data['orderId']
#                 order_details = dhan.get_order_by_id(order_id)
              
#                 save_executed_order(order_details, strategy_id, latest_ltp, MainOrderid=MainOrderid, stop_loss_price=stop_loss_price, ordertype="stop_loss")

#     except Exception as e:
#         logging.debug(f"Failed to place stop_loss order for strategy {strategy_id}: {e}")
#         send_error_log(f"Failed to place stop_loss order for strategy {strategy_id}: {e}", "Risk_management.py")

def place_stop_loss_Dhan(order_details, strategy_id, price, strategy_data, actions):
    logging.debug(f"Entering place_stop_loss_order with order_details: {order_details}")
    
    security_id = order_details['data']['securityId']
    logging.debug(f"Extracted security_id: {security_id}")
    
    # Fetch the latest LTP
    # latest_ltp = get_latest_ltp(security_id)
    # logging.debug(f"Fetched price for security_id {security_id}: {price}")
    
    # Tick size initialization
    tick_size = 0.01  # Ideally, get this dynamically
    logging.debug(f"Using tick_size: {tick_size}")
    
    # Determine transaction type
    transaction_type = dhan.SELL if order_details['data']['transactionType'] == dhan.BUY else dhan.BUY
    logging.debug(f"Determined transaction_type based on order_details: {transaction_type}")
    
    # Extract stoploss_percent with error handling
    try:
        stoploss_percent = float(actions.get('stoploss_percent', 1))
        logging.debug(f"Extracted stoploss_percent: {stoploss_percent}")
    except ValueError as ve:
        logging.error(f"Error converting stoploss_percent to float: {ve}")
        return
    
    # Extract MainOrderid for reference
    MainOrderid = order_details['data']['orderId']
    logging.debug(f"MainOrderid extracted: {MainOrderid}")
    
    # Ensure latest_ltp is a float
    try:
        MainOrder_Price = float(price)
        logging.debug(f"Converted MainOrder_Price to float: {MainOrder_Price}")
    except ValueError as ve:
        logging.error(f"Error converting MainOrder_Price to float: {ve}")
        return
    
    # Calculate stop_loss_price
    stop_loss_price = MainOrder_Price - (MainOrder_Price * stoploss_percent / 100)
    logging.debug(f"Calculated stop_loss_price before rounding: {stop_loss_price}")
    
    # Round to nearest tick size
    stop_loss_price = round(stop_loss_price / tick_size) * tick_size
    logging.debug(f"Rounded stop_loss_price to nearest tick size: {stop_loss_price}")
    
    # Default fallback for invalid stop_loss_price
    if stop_loss_price <= 0:
        logging.warning(f"stop_loss_price is invalid (<= 0). Defaulting to 24.00")
        stop_loss_price = 24.00
    
    logging.debug(f"Final stop_loss_price to be used: {stop_loss_price}")
    
    # Log stop_loss_price
    send_error_log(f"stop_loss_price for strategy {strategy_id}: {stop_loss_price}", "Risk_management.py")
    
    # Place the stop-loss order
    try:
        response = dhan.place_order(
            transaction_type=transaction_type,
            exchange_segment=order_details['data']['exchangeSegment'],
            product_type=order_details['data']['productType'],
            order_type=dhan.LIMIT,
            validity='DAY',
            security_id=order_details['data']['securityId'],
            quantity=order_details['data']['quantity'],
            price=stop_loss_price
        )
        logging.debug(f"Stop-loss order placed successfully. Response: {response}")
        
        # Handle the response for a successful order placement
        if response['status'] == 'success' and 'data' in response:
            order_data = response['data']
            if order_data.get('orderStatus') == 'TRANSIT' and 'orderId' in order_data:
                order_id = order_data['orderId']
                logging.debug(f"Order in TRANSIT state. order_id: {order_id}")
                
                order_details = dhan.get_order_by_id(order_id)
                save_executed_order(order_details, strategy_id, MainOrder_Price, 
                                    MainOrderid, 
                                    stop_loss_price=stop_loss_price, 
                                    ordertype="Stop_loss")
            else:
                logging.debug(f"Order not in TRANSIT state or missing orderId: {order_data}")
    
    except Exception as e:
        logging.error(f"Failed to place stop-loss order for strategy {strategy_id}: {e}")
        send_error_log(f"Failed to place stop-loss order for strategy {strategy_id}: {e}", "Risk_management.py")







def place_Target_Dhan(order_details, strategy_id, price, strategy_data, actions):
    logging.debug("Entering function: place_book_profit_order")
    
    logging.debug(f"Extracted actions: {actions}")

    # Extracting the security ID
    security_id = order_details['data']['securityId']
    logging.debug(f"Extracted security_id: {security_id}")
    
    # Fetching the latest LTP for the security
    # latest_ltp = get_latest_ltp(security_id)
    # logging.debug(f"Fetched latest_ltp for security_id {security_id}: {latest_ltp}")
    
    # Debug the incoming order details
    logging.debug(f"Received order_details: {order_details}")
    
    # Retrieve the target percent or use the default value
    target_percent = actions.get('target_percent', 1)  # Default is 1%
    logging.debug(f"Target percent for book profit: {target_percent}")
    
    # Tick size for rounding
    tick_size = 0.01
    logging.debug(f"Tick size set to: {tick_size}")
    
    # Extract the main order ID
    MainOrderid = order_details['data']['orderId']
    logging.debug(f"Extracted MainOrderid: {MainOrderid}")
        
    # Convert the latest LTP to float if necessary
    MainOrder_Price = float(price)
    logging.debug(f"Converted MainOrder_Price to float: {MainOrder_Price}")
    
    # Calculate the book profit price
    book_profit_price = MainOrder_Price * (1 + float(target_percent) / 100)
    logging.debug(f"Calculated pre-rounded book_profit_price: {book_profit_price}")
    
    # Round the book profit price to the nearest tick size
    book_profit_price = round(book_profit_price / tick_size) * tick_size or 27
    logging.debug(f"Rounded book_profit_price to tick size: {book_profit_price}")
    
    # Log the calculated book profit price
    send_error_log(f"Book profit price for strategy {strategy_id}: {book_profit_price}", "Risk_management.py")
    
    try:
        # Attempt to place the book profit order
        logging.debug("Placing book profit order with the following parameters:")
        logging.debug(f"Transaction Type: SELL, Exchange Segment: {order_details['data']['exchangeSegment']}, "
                      f"Product Type: {order_details['data']['productType']}, Order Type: LIMIT, Validity: DAY, "
                      f"Security ID: {order_details['data']['securityId']}, Quantity: {order_details['data']['quantity']}, "
                      f"Price: {book_profit_price}")
        
        response = dhan.place_order(
            transaction_type=dhan.SELL,
            exchange_segment=order_details['data']['exchangeSegment'],
            product_type=order_details['data']['productType'],
            order_type=dhan.LIMIT,
            validity='DAY',
            security_id=order_details['data']['securityId'],
            quantity=order_details['data']['quantity'],
            price=book_profit_price
        )
        
        # Log the response from the order placement
        logging.debug(f"Response from dhan.place_order: {response}")

        # Handle the response for a successful order placement
        if response['status'] == 'success' and 'data' in response:
            order_data = response['data']
            if order_data.get('orderStatus') == 'TRANSIT' and 'orderId' in order_data:
                order_id = order_data['orderId']
                logging.debug(f"Order in TRANSIT state. order_id: {order_id}")
                
                order_details = dhan.get_order_by_id(order_id)
                save_executed_order(order_details, strategy_id, MainOrder_Price, MainOrderid,
                                book_profit_price=book_profit_price,ordertype="Target")
            else:
                logging.debug(f"Order not in TRANSIT state or missing orderId: {order_data}")


        
        # # Handle successful order placement
        # if response['status'] == 'success' and 'data' in response:
        #     order_data = response['data']
        #     logging.debug(f"Order data from response: {order_data}")
            
        #     # Save the executed order
        #     save_executed_order(order_details, strategy_id, MainOrder_Price, MainOrderid,
        #                         book_profit_price=book_profit_price,ordertype="Target")
                
            

        else:
            logging.error(f"Failed to place book profit order. Response: {response}")
            send_error_log(f"Failed to place book profit order: {response}", 'place_book_profit_order')

    except Exception as e:
        logging.error(f"Error in placing book profit order: {e}")
        send_error_log(f"Error placing book profit order: {e}", 'place_book_profit_order')



# def place_book_profit_order(order_details, strategy_id, latest_ltp, strategy_data, actions):
#     logging.debug("Entering function: place_book_profit_order")
    
#     logging.debug(f"Extracted actions: {actions}")

#     # Extracting the security ID
#     security_id = order_details['data']['securityId']
#     logging.debug(f"Extracted security_id: {security_id}")
    
#     # Fetching the latest LTP for the security
#     latest_ltp = get_latest_ltp(security_id)
#     logging.debug(f"Fetched latest_ltp for security_id {security_id}: {latest_ltp}")
    
#     # Debug the incoming order details
#     logging.debug(f"Received order_details: {order_details}")
    
#     # Retrieve the target percent or use the default value
#     target_percent = actions.get('target_percent', 1)  # Default is 1%
#     logging.debug(f"Target percent for book profit: {target_percent}")
    
#     # Tick size for rounding
#     tick_size = 0.01
#     logging.debug(f"Tick size set to: {tick_size}")
    
#     # Extract the main order ID
#     MainOrderid = order_details['data']['orderId']
#     logging.debug(f"Extracted MainOrderid: {MainOrderid}")
    
#     # Log the order details for debugging
#     send_error_log(order_details, "Risk_management.py-place_book_profit_order")
    
#     # Convert the latest LTP to float if necessary
#     latest_ltp = float(latest_ltp)
#     logging.debug(f"Converted latest_ltp to float: {latest_ltp}")
    
#     # Calculate the book profit price
#     book_profit_price = latest_ltp * (1 + float(target_percent) / 100)
#     logging.debug(f"Calculated pre-rounded book_profit_price: {book_profit_price}")
    
#     # Round the book profit price to the nearest tick size
#     book_profit_price = round(book_profit_price / tick_size) * tick_size or 27
#     logging.debug(f"Rounded book_profit_price to tick size: {book_profit_price}")
    
#     # Log the calculated book profit price
#     send_error_log(f"Book profit price for strategy {strategy_id}: {book_profit_price}", "Risk_management.py")
    
#     try:
#         # Attempt to place the book profit order
#         logging.debug("Placing book profit order with the following parameters:")
#         logging.debug(f"Transaction Type: SELL, Exchange Segment: {order_details['data']['exchangeSegment']}, "
#                       f"Product Type: {order_details['data']['productType']}, Order Type: LIMIT, Validity: DAY, "
#                       f"Security ID: {order_details['data']['securityId']}, Quantity: {order_details['data']['quantity']}, "
#                       f"Price: {book_profit_price}")
        
#         response = dhan.place_order(
#             transaction_type=dhan.SELL,
#             exchange_segment=order_details['data']['exchangeSegment'],
#             product_type=order_details['data']['productType'],
#             order_type=dhan.LIMIT,
#             validity='DAY',
#             security_id=order_details['data']['securityId'],
#             quantity=order_details['data']['quantity'],
#             price=book_profit_price
#         )
        
#         # Log the response from the order placement
#         logging.debug(f"Response from dhan.place_order: {response}")
        
#         # Handle successful order placement
#         if response['status'] == 'success' and 'data' in response:
#             order_data = response['data']
#             logging.debug(f"Order data from response: {order_data}")
            
#             if order_data.get('orderStatus') == 'TRANSIT' and 'orderId' in order_data:
#                 order_id = order_data['orderId']
#                 logging.debug(f"Order ID in transit: {order_id}")
                
#                 # Fetch the updated order details for this order
#                 order_details = dhan.get_order_by_id(order_id)
#                 logging.debug(f"Fetched order details for ID {order_id}: {order_details}")
                
#                 # Check the order status again
#                 order_status = order_details['data'].get('orderStatus', 'UNKNOWN')
                
#                 if order_status == 'REJECTED':
#                     logging.error(f"Order ID {order_id} was REJECTED: {order_details}")
#                     send_error_log(f"Order {order_id} rejected: {order_details}", 'place_book_profit_order')
#                     return  # Exit early if the order was rejected

#                 # Save the executed order
#                 save_executed_order(order_details, strategy_id, latest_ltp, MainOrderid=MainOrderid,
#                                     book_profit_price=book_profit_price)
                
#                 # Optionally, you can place additional risk management orders like stop loss, etc.
#                 place_stop_loss_order(order_details, strategy_id, latest_ltp, strategy_data, actions)

#         else:
#             logging.error(f"Failed to place book profit order. Response: {response}")
#             send_error_log(f"Failed to place book profit order: {response}", 'place_book_profit_order')

#     except Exception as e:
#         logging.error(f"Error in placing book profit order: {e}")
#         send_error_log(f"Error placing book profit order: {e}", 'place_book_profit_order')




def cancel_pending_orders(order_id):
    try:
        response = dhan.cancel_order(order_id)
        if response['status'] == 'success':
            print(f"Cancelled pending order with order ID {order_id}")
        else:
            print(f"Failed to cancel pending order with order ID {order_id}")
    except Exception as e:
        print(f"Failed to cancel pending order with order ID {order_id}: {e}")


def check_pending_orders():
    try:
        pending_orders = dhan.get_order_list()
        print("pending_orders:",pending_orders)
        # Get pending orders
        # pending_orders = dhan.get_pending_orders()
        if pending_orders['status'] == 'success':
            orders = pending_orders['data']
            if orders:
                print("Pending orders found:")
                for order in orders:
                    print(f"Order ID: {order['orderId']}, Status: {order['orderStatus']}")
                    # Cancel pending orders after 3 p.m.
                    if order['orderTime'] >= '15:00':
                        cancel_pending_orders(order['orderId'])
            else:
                print("No pending orders found.")
        else:
            print("Failed to retrieve pending orders.")
    except Exception as e:
        print(f"Failed to check pending orders: {e}")


# Example usage:

# Sample strategy ID
# strategy_id = 'S_41868'

# strategy_data = {4}

# Sample function call
# place_stop_loss_order(order_details, strategy_id, strategy_data )


# place_stop_loss_order(order_details, strategy_id, latest_ltp, strategy_data, actions)


# Static input values from debug logs
# order_details = {
#     'status': 'success',
#     'remarks': '',
#     'data': {
#         'dhanClientId': '1101343871',
#         'orderId': '6125011057766',
#         'exchangeOrderId': '0',
#         'correlationId': '1101343871-1736491974434',
#         'orderStatus': 'REJECTED',
#         'transactionType': 'BUY',
#         'exchangeSegment': 'NSE_EQ',
#         'productType': 'INTRADAY',
#         'orderType': 'MARKET',
#         'validity': 'DAY',
#         'tradingSymbol': 'LASA',
#         'securityId': '21713',
#         'quantity': 1,
#         'disclosedQuantity': 0,
#         'price': 0.0,
#         'triggerPrice': 0.0,
#         'afterMarketOrder': False,
#         'boProfitValue': 0.0,
#         'boStopLossValue': 0.0,
#         'legName': 'NA',
#         'createTime': '2025-01-10 12:22:54',
#         'updateTime': '2025-01-10 12:22:54',
#         'exchangeTime': '0001-01-01 00:00:00',
#         'drvExpiryDate': '0001-01-01',
#         'drvOptionType': 'NA',
#         'drvStrikePrice': 0.0,
#         'omsErrorCode': '0',
#         'omsErrorDescription': 'RMS:6125011057766:Insufficient Funds, required margin is 27.23 and available margin 0. Add Funds to Trade',
#         'filled_qty': 0,
#         'algoId': '0'
#     }
# }

# strategy_id = 1
# latest_ltp = 27.23
# strategy_data = {"key": "value"}  # Placeholder for strategy data
# actions = {"target_percent": 1}  # Example action

# Call the function
# place_book_profit_order(order_details, strategy_id, latest_ltp, strategy_data, actions)
# place_stop_loss_order(order_details, strategy_id, latest_ltp, strategy_data, actions)