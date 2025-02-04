import csv
import time
import copy
from collections import OrderedDict
from dhanhq import dhanhq
from Helper_Files.send_error_log import send_error_log
from constants import access_token,client_id

# client_id = "1101343871"
# access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzIxMjg0NDUzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTM0Mzg3MSJ9.u6fKzbiql1wAPrfRJkbSU2IDgEblAvBD8TxvTHLdofz9e_QDP21D81pj9nL1A1tjlaUwG5nHKI9icIEDYZZ5eA'

dhan = dhanhq(client_id, access_token)

def read_orders(file_path):
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            orders = list(csv_reader)
        return orders, csv_reader.fieldnames
    except FileNotFoundError:
        error_message = f"The file {file_path} does not exist."
        send_error_log(error_message, 'read_orders')
        return [], []

def get_pending_orders(orders):
    return [order for order in orders if order['orderStatus'].lower() == 'pending']

def get_Entry_orders(orders):
    # print("orders in get_Entry_orders:",orders)
    return [order for order in orders if order['OrderCategory'].lower() == 'entry']






def compare_and_update_orders(orders, all_orders):
    updated_orders = []
    # Create a lookup dictionary only if 'BrokerOrderID' is present in all_orders
    if all_orders and all(isinstance(order, dict) and 'orderId' in order for order in all_orders):
        order_lookup = {order['orderId']: order for order in all_orders}
      
    else:
        print("ERROR: Invalid data format in all_orders or missing 'orderId' key.")
        return updated_orders

    for order in orders:
  
        broker_order_id = order.get('BrokerOrderID')  # Use .get() to safely get the value or None
        if broker_order_id and broker_order_id in order_lookup:
            all_order = order_lookup[broker_order_id]
            new_order_status = all_order.get('orderStatus')
            if new_order_status and order['orderStatus'] != new_order_status:
                order['orderStatus'] = new_order_status

            # Check for quantity changes in Entry orders
            if order['OrderCategory'].lower() == 'entry':
                print("in ordersflow")
                new_quantity = all_order.get('quantity')
                print("new_quantity:",new_quantity)
                if new_quantity and order['quantity'] != str(new_quantity):
                    print(f"Quantity changed for order {order['order_id']}: old quantity = {order['quantity']}, new quantity = {new_quantity}")
        
        updated_orders.append(order)

    return updated_orders

def write_orders(file_path, orders, fieldnames):
    try:
        with open(file_path, mode='w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()
            csv_writer.writerows(orders)
    except csv.Error as e:
        error_message = f"Error writing to the CSV file: {e}"
        send_error_log(error_message, 'write_orders')

def cancelorder(MainOrderid):
    orders, _ = read_orders('orders.csv')
    pending_orders = [order for order in orders if order['MainOrderid'] == MainOrderid and order['orderStatus'].lower() == 'pending']
    
    for order in pending_orders:
        broker_order_id = order['BrokerOrderID']
        print("in cancelorder id:",broker_order_id )
        response = dhan.cancel_order(broker_order_id)
        if response.get('status') == 'success':
            order['orderStatus'] = 'cancelled'
    
    write_orders('orders.csv', orders, orders[0].keys())

def WaitingStatus(strategy_id):
    strategies, fieldnames = read_orders('strategy.csv')
    for strategy in strategies:
        if strategy['strategy_id'] == strategy_id:
            strategy['status'] = 'waiting'
    
    write_orders('../Input_Files/strategy.csv', strategies, fieldnames)


def check_and_update_entry_orders(entry_orders, all_orders):

    # print("in check_and_update_entry_orders all_orders:",all_orders)
    changed_orders = []  # Initialize changed_orders list
    for entry_order in entry_orders:
        print("entry_order.get('BrokerOrderID'):", entry_order.get('BrokerOrderID'))
        for all_order in all_orders:
            print("all_order.get('orderId'):", all_order.get('orderId'))
            if all_order.get('orderId') == entry_order.get('BrokerOrderID'):
                new_quantity = all_order.get('quantity')
                if new_quantity and entry_order['quantity'] != str(new_quantity):
                    # Read orders from CSV
                    orders, fieldnames = read_orders('orders.csv')
                    order_id = next((order['order_id'] for order in orders if order['order_id'] == entry_order['order_id']), None)
                    if order_id:
                        print(f"Quantity changed for Entry order {order_id}: old quantity = {entry_order['quantity']}, new quantity = {new_quantity}")
                        # Collect all rows in orders.csv where MainOrderid matches order_id
                        matching_orders = [order for order in orders if order.get('MainOrderid') == order_id]
                        changed_orders.extend(matching_orders)
                        # print("changed_orders:", changed_orders)
    if changed_orders:
        modify_orders(changed_orders, new_quantity)                    


def updatenewqty(order_id, new_quantity):
    orders, fieldnames = read_orders('orders.csv')
    order_found = False
    for order in orders:
        if order['order_id'] == order_id:
            order['quantity'] = str(new_quantity)
            order_found = True
            break
    
    if order_found:
        write_orders('orders.csv', orders, fieldnames)
        print(f"Updated quantity for order {order_id} to {new_quantity}.")
    else:
        print(f"Order ID {order_id} not found in the orders file.")

def modify_orders(changed_orders, new_quantity):
    modified_orders = []
    modified_fieldnames = ['orderid', 'scripname', 'origional qty', 'modiefied qty', 'modiefiedtiming']

    for order in changed_orders:
        print("in modify_orders order['BrokerOrderID'],new_quantity:",order['BrokerOrderID'],new_quantity)
        try:
            response = dhan.modify_order(
                 order_id=order['BrokerOrderID'],
                 order_type=dhan.LIMIT,
                 leg_name=0,
                 quantity=new_quantity,
                 price=order['ExecutionPrice'],
                 disclosed_quantity='',
                 trigger_price=0,
                 validity=dhan.DAY
            )
            if response['status'] == 'TRANSIT':
                print(f"Order {order['order_id']} modified successfully to new quantity {new_quantity}")
                updatenewqty(order['order_id'],new_quantity)
                modified_orders.append({
                    'orderid': order['order_id'],
                    'scripname': order['tradingSymbol'],
                    'origional qty': order['quantity'],
                    'modiefied qty': new_quantity,
                    'modiefiedtiming': time.strftime('%Y-%m-%d %H:%M:%S')
                })
                # modified_orders.append(order)  # Add modified order to list
            else:
                print(f"Failed to modify order {order['order_id']}: {response}")
        except Exception as e:
            print(f"Exception occurred while modifying order {order['order_id']}: {str(e)}")
         # Save modified orders to orders_modified.csv
    if modified_orders:
        write_orders('orders_modified.csv', modified_orders, modified_fieldnames)               

def check_pending_orders():
    while True:
        orders, fieldnames = read_orders('orders.csv')
        if not orders:
            print("DEBUG: No orders found in orders.csv")
       
        pending_orders = get_pending_orders(orders)
        entry_orders = get_Entry_orders(orders)

        # print("entry_orders:",entry_orders)
        # print("pending_orders:",pending_orders)
        
        if pending_orders:
            response = dhan.get_order_list()

            if response['status'] == 'success':
                all_orders = response['data']
            else:
                print("DEBUG: No orders found from dhan.get_order_list()")
                all_orders = []
#             all_orders = [
#     {
#         "dhanClientId": "1000000003",
#         "orderId": "67756890",
#         "correlationId":"123abc678",
#         "orderStatus": "success",
#         "transactionType": "BUY",
#         "exchangeSegment": "NSE_EQ",
#         "productType": "INTRADAY",
#         "orderType": "MARKET",
#         "validity": "DAY",
#         "tradingSymbol": "",
#         "securityId": "11536",
#         "quantity": 5,
#         "disclosedQuantity": 0,
#         "price": 0.0,
#         "triggerPrice": 0.0,
#         "afterMarketOrder": False,
#         "boProfitValue": 0.0,
#         "boStopLossValue": 0.0,
#         "legName":0,
#         "createTime": "2021-11-24 13:33:03",
#         "updateTime": "2021-11-24 13:33:03",
#         "exchangeTime": "2021-11-24 13:33:03",
#         "drvExpiryDate": "null",
#         "drvOptionType": "null",
#         "drvStrikePrice": 0.0,
#         "omsErrorCode": "null",
#         "omsErrorDescription": "null",
#         "filled_qty": 0,
#         "algoId": "string"
#     }
# ]

            if not all_orders:
                print("DEBUG: No orders found from dhan.get_order_list()")
            
            updated_orders = compare_and_update_orders(orders, all_orders)
            check_and_update_entry_orders(entry_orders, all_orders)
            write_orders('orders.csv', updated_orders, fieldnames)
            
            for order in pending_orders:
                if order['orderStatus'].lower() != 'pending':
                    WaitingStatus(order['strategy_id'])
        else:
            print("DEBUG: No pending orders found")
        
        time.sleep(10)

# Call the function to start checking for pending orders
# check_pending_orders()

