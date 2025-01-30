
import csv
from collections import OrderedDict
import random
import requests
from Helper_Files.send_error_log import send_error_log
from Helper_Files.get_latest_ltp import get_latest_ltp
import logging
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# from send_error_log import send_error_log


def map_tradedupe_status(broker_name, broker_status):
    """
    Map the broker's status to the application's status.
    
    :param broker_name: Name of the broker
    :param broker_status: Status from the broker
    :return: Mapped status for the application
    """
    # Define your status mappings here
    status_mapping = {
        'Dhan': {
            'TRADED': 'success', 
            'PENDING': 'pending',
            'REJECTED': 'failed',
            'CANCELLED': 'cancelled',
            'TRANSIT':'pending',
            'success':'success',
 
            # Add more mappings as needed
        },
        'BrokerB': {
            'done': 'Success',
            'in_progress': 'Pending',
            'error': 'Failed'
            # Add more mappings as needed
        }
        # Add more brokers as needed
    }





    # Get the status mapping for the given broker
    broker_status_mapping = status_mapping.get(broker_name, {})
    return broker_status_mapping.get(broker_status, 'Unknown')


def save_executed_order(order_details, strategy_id,price, MainOrderid=None, stop_loss_price=None,book_profit_price=None, ordertype="mainorder"):
    print("save_executed_order MainOrderid:", MainOrderid)

    execution_price = price  # Default to latest_ltp

    if ordertype == "Stop_loss" and stop_loss_price is not None:
        execution_price = stop_loss_price
    elif ordertype == "Target" and book_profit_price is not None:
        execution_price = book_profit_price
    
    api_url = 'http://localhost:5000/python/save-executed-order'
    
    # Create a new object with values from order_details
    new_order_details = OrderedDict()
    new_order_details['strategy_id'] = strategy_id
    new_order_details['MainOrderid'] = MainOrderid if MainOrderid else ''
    new_order_details['OrderCategory'] = ordertype
    
    # Generate a random 5-digit order ID
    random_order_id = str(random.randint(10000, 99999))
    
    new_order_details.update({
        'BrokerClientID': order_details['data'].get('dhanClientId', ''),
        'order_id': random_order_id, 
        'BrokerOrderID': order_details['data'].get('orderId', ''),
        'correlationId': order_details['data'].get('correlationId', ''),
        'orderStatus': map_tradedupe_status('Dhan', order_details['data'].get('orderStatus', '')),
        'transactionType': order_details['data'].get('transactionType', ''),
        'exchangeSegment': order_details['data'].get('exchangeSegment', ''),
        'productType': order_details['data'].get('productType', ''),
        'orderType': order_details['data'].get('orderType', ''),
        'validity': order_details['data'].get('validity', ''),
        'tradingSymbol': order_details['data'].get('tradingSymbol', ''),
        'securityId': order_details['data'].get('securityId', ''),
        'quantity': order_details['data'].get('quantity', ''),
        'disclosedQuantity': order_details['data'].get('disclosedQuantity', ''),
        # 'ExecutionPrice': order_details['data'].get('price', ''),
        'ExecutionPrice':execution_price,
        'triggerPrice': order_details['data'].get('triggerPrice', ''),
        'IsAMO': order_details['data'].get('afterMarketOrder', ''),
        'boProfitValue': order_details['data'].get('boProfitValue', ''),
        'boStopLossValue': order_details['data'].get('boStopLossValue', ''),
        'legName': order_details['data'].get('legName', ''),
        'createTime': order_details['data'].get('createTime', ''),
        'updateTime': order_details['data'].get('updateTime', ''),
        'exchangeTime': order_details['data'].get('exchangeTime', ''),
        'drvExpiryDate': order_details['data'].get('drvExpiryDate', ''),
        'drvOptionType': order_details['data'].get('drvOptionType', ''),
        'drvStrikePrice': order_details['data'].get('drvStrikePrice', ''),
        'omsErrorCode': order_details['data'].get('omsErrorCode', ''),
        'omsErrorDescription': order_details['data'].get('omsErrorDescription', ''),
        'filled_qty': order_details['data'].get('filled_qty', ''),
        'algoId': order_details['data'].get('algoId', ''),
    })

    response = requests.post(api_url, json={
        'order_details': new_order_details,
        'strategy_id': strategy_id,
        'MainOrderid': MainOrderid,
        'ordertype': ordertype
    })

    if response.status_code == 201:
        print('Order saved successfully')
    else:
        print('Failed to save order', response.text)
        send_error_log(response.text, 'save_executed_order')


#         # Sample order_details object
# order_details = {
#     'data': {
#     "dhanClientId": "1101343871",
#     "orderId": "1124090536396",
#     "exchangeOrderId": "1300000024948292",
#     "correlationId": "1101343871-1725518165987",
#     "orderStatus": "PENDING",
#     "transactionType": "SELL",
#     "exchangeSegment": "NSE_EQ",
#     "productType": "INTRADAY",
#     "orderType": "LIMIT",
#     "validity": "DAY",
#     "tradingSymbol": "SOUTHBANK",
#     "securityId": "5948",
#     "quantity": 1,
#     "disclosedQuantity": 0,
#     "price": 26.42,
#     "triggerPrice": 0.0,
#     "afterMarketOrder": False,
#     "boProfitValue": 0.0,
#     "boStopLossValue": 0.0,
#     "legName": "NA",
#     "createTime": "2024-09-05 12:06:06",
#     "updateTime": "2024-09-05 12:06:06",
#     "exchangeTime": "2024-09-05 12:06:06",
#     "drvExpiryDate": "0001-01-01",
#     "drvOptionType": "NA",
#     "drvStrikePrice": 0.0,
#     "omsErrorCode": "0",
#     "omsErrorDescription": "CONFIRMED",
#     "filled_qty": 0,
#     "algoId": "0"
# }
# }

# # Parameters for the function
# strategy_id = 65
# latest_ltp = 0
# MainOrderid = ''
# stop_loss_price = 0
# book_profit_price = 26.42
# ordertype = 'Target'  # Use 'mainorder', 'stop_loss', or 'Target'

# # Function call
# save_executed_order(order_details, strategy_id, latest_ltp, MainOrderid, stop_loss_price, book_profit_price, ordertype)