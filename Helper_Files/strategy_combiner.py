import csv
from datetime import datetime
from dhanhq import dhanhq
import copy
from Helper_Files.fetch_data import fetch_data
from Helper_Files.send_error_log import send_error_log
from constants import access_token,client_id

import requests

# client_id = "1101343871"
# access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzIxMjg0NDUzLCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTM0Mzg3MSJ9.u6fKzbiql1wAPrfRJkbSU2IDgEblAvBD8TxvTHLdofz9e_QDP21D81pj9nL1A1tjlaUwG5nHKI9icIEDYZZ5eA'

dhan = dhanhq(client_id, access_token)

def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)



def combine_data():
    # Fetch data from the API endpoint
    api_url = "http://localhost:5000/python/activestrategy"
    api_data = fetch_data(api_url)
    
    # Define a mapping for indicator IDs to names
    # indicator_mapping = {
    #     1: "Simple Moving Average",
    #     2: "Relative Strength Index",
    #     3: "Parabolic SAR",
    #     4: "Moving Average Convergence Divergence",
    #     5: "Exponential Moving Average"
    # }

    indicator_mapping = {
        1: "SMA",
        2: "RSI",
        3: "PSAR",
        4: "MACD",
        5: "EMA"
    }
    
    # Create a list to store combined data for each strategy
    combined_data_list = []
    
    # Process the API data
    for entry in api_data:
        strategy = entry.get('strategy', {})
        indicators = entry.get('indicators', [])
        actions = entry.get('actions', [])
        
        # Update indicator names based on indicator_id
        for indicator in indicators:
            indicator_id = indicator.get('indicator_id')
            indicator['indicator_name'] = indicator_mapping.get(int(indicator_id), 'Unknown Indicator')
        
        combined_data = {
            'strategy': strategy,
            'indicators': indicators,
            'actions': actions
        }
        
        # Append the combined data for the current strategy to the list
        combined_data_list.append(combined_data)
    
    return combined_data_list

def print_combined_data(combined_data_list):
    for idx, combined_data in enumerate(combined_data_list, start=1):
        strategy_id = combined_data['strategy']['strategy_id']
        print(f"Strategy {idx}:")
        print("Strategy:", combined_data['strategy'])
        print("Indicators:", combined_data['indicators'])
        print("Actions:", combined_data['actions'])
        print()




def update_strategy_status(strategy_id):
    # Define the API endpoint URL
    api_url = 'http://localhost:5000/python/update-execution-status'
    
    # Define the payload with strategy_id
    payload = {
        'strategy_id': strategy_id
    }
    
    try:
        # Send a POST request to the API to update the execution status
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Check the response from the API
        data = response.json()
        if data.get('success'):
            print('Execution status updated to executed.')
        else:
            send_error_log(data.get('message'), 'update_strategy_status')
          

    
    except requests.RequestException as e:
        print('Error updating execution status:', e)
        send_error_log(e, 'update_strategy_status')


def increment_operation_count(strategy_id):
    # Define the API endpoint
    url = f'http://localhost:5000/python/increment-operation-count/{strategy_id}'

    try:
        # Make the PUT request to the API
        response = requests.put(url)

        # Check if the request was successful
        if response.status_code == 200:
            print(f'Success: {response.json()["message"]}')
            print(f'Updated operation count: {response.json()["operationcount"]}')
        else:
            print(f'Failed to increment operation count. Status code: {response.status_code}, Message: {response.json().get("message")}')
    
    except Exception as e:
        print(f'An error occurred: {e}')





# def check_pending_orders():
#     file_path = 'orders.csv'
#     updated_orders = []

#     try:
#         # Read the current orders from the CSV file
#         with open(file_path, mode='r') as file:
#             csv_reader = csv.DictReader(file)
#             fieldnames = csv_reader.fieldnames
#             orders = list(csv_reader)

#         # Get the list of all orders from dhan
#         response = dhan.get_order_list()
#         order_list = response['data']
#         print("response in check_pending_orders:", response)

#         # Create a dictionary for quick lookup of order details by orderId
#         order_lookup = {order['orderId']: order for order in order_list}

#         # Process orders
#         for row in orders:
#             order_id = row['BrokerOrderID']
#             if row['orderStatus'] == 'PENDING' and order_id in order_lookup:
#                 print(f"Order ID {order_id} for strategy {row['strategy_id']} is pending.")
#                 new_order_status = order_lookup[order_id]['orderStatus']

#                 if row['orderStatus'] != new_order_status:
#                     print(f"Updating order status for order ID {order_id} from {row['orderStatus']} to {new_order_status}")
#                     updated_row = copy.deepcopy(row)
#                     updated_row['orderStatus'] = new_order_status
#                     updated_orders.append(updated_row)
#                 else:
#                     updated_orders.append(row)
#             else:
#                 updated_orders.append(row)

#         # Write the updated orders back to the CSV file
#         with open(file_path, mode='w', newline='') as file:
#             csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
#             csv_writer.writeheader()
#             csv_writer.writerows(updated_orders)

#     except FileNotFoundError:
#         print(f"The file {file_path} does not exist.")
#     except csv.Error as e:
#         print(f"Error processing the CSV file: {e}")

#     file_path = 'orders.csv'
#     updated_orders = []

#     try:
#         # Read the current orders from the CSV file
#         with open(file_path, mode='r') as file:
#             csv_reader = csv.DictReader(file)
#             fieldnames = csv_reader.fieldnames
#             orders = list(csv_reader)

#         # Get the list of all orders from dhan
#         response = dhan.get_order_list()
#         order_list = response['data']
#         print("response in check_pending_orders:", response)

#         # Create a dictionary for quick lookup of order details by orderId
#         order_lookup = {order['orderId']: order for order in order_list}

#         # Process orders
#         for row in orders:
#             order_id = row['BrokerOrderID']
#             if row['orderStatus'] == 'PENDING' and order_id in order_lookup:
#                 print(f"Order ID {order_id} for strategy {row['strategy_id']} is pending.")

#                 # Compare and update only the changed fields
#                 updated_row = copy.deepcopy(row)
#                 for key, value in order_lookup[order_id].items():
#                     if key in row and row[key] != str(value):
#                         updated_row[key] = str(value)
                
#                 updated_orders.append(updated_row)
#             else:
#                 updated_orders.append(row)

#         # Write the updated orders back to the CSV file
#         with open(file_path, mode='w', newline='') as file:
#             csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
#             csv_writer.writeheader()
#             csv_writer.writerows(updated_orders)

#     except FileNotFoundError:
#         print(f"The file {file_path} does not exist.")
#     except csv.Error as e:
#         print(f"Error processing the CSV file: {e}")





        

def check_pending_orders():
    # Define the API endpoints
    get_orders_api = 'http://localhost:5000/python/get-all-orders'
    update_order_api = 'http://your-api-server/update-order-status'

    try:
        # Fetch orders from your database via API
        db_response = requests.get(get_orders_api)
        db_orders = db_response.json()

        # Fetch orders from Dhan
        dhan_response = dhan.get_order_list()
        dhan_orders = dhan_response['data']
        print("response in check_pending_orders:", dhan_response)

        # Create a dictionary for quick lookup of Dhan orders by orderId
        dhan_order_lookup = {order['orderId']: order for order in dhan_orders}

        # Process orders
        for order in db_orders:
            order_id = order['BrokerOrderID']
            if order['orderStatus'] == 'PENDING' and order_id in dhan_order_lookup:
                print(f"Order ID {order_id} for strategy {order['strategy_id']} is pending.")
                new_order_status = dhan_order_lookup[order_id]['orderStatus']

                # Update the order status if it has changed
                if order['orderStatus'] != new_order_status:
                    print(f"Updating order status for order ID {order_id} from {order['orderStatus']} to {new_order_status}")
                    updated_order = copy.deepcopy(order)
                    updated_order['orderStatus'] = new_order_status

                    # Send the updated order status back to the database
                    update_response = requests.post(update_order_api, json=updated_order)
                    if update_response.status_code != 200:
                        print(f"Failed to update order ID {order_id}: {update_response.text}")
                        send_error_log("Failed to update order ID {order_id}: {update_response.text}", 'strategy_combiner.py')

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with the API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")