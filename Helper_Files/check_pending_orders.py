





import time
import requests
from dhanhq import dhanhq
from Helper_Files.send_error_log import send_error_log
from Helper_Files.save_executed_order import map_tradedupe_status
from constants import access_token,client_id


# import time
# import requests
# from dhanhq import dhanhq
# from send_error_log import send_error_log
# from save_executed_order import map_tradedupe_status

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# client_id = "1101343871"
# access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI4ODAxODg5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTM0Mzg3MSJ9.Rcr4VMpNakJvYB0ThB84v0DOaxiMRIZZoeqol8QAGEEgvPJJ3SpBsZVIyAcJvscOO3HPkx1fI0r6uZwV99V08g'

dhan = dhanhq(client_id, access_token)

BASE_URL = "http://localhost:5000/python"

def get_orders_from_api(endpoint):
    """
    Fetches orders from the API endpoint provided.
    
    Args:
        endpoint (str): The API endpoint to fetch orders from.
    
    Returns:
        list: A list of orders in JSON format.
    """
    try:
        logging.debug(f"Fetching orders from API endpoint: {BASE_URL}{endpoint}")
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        orders = response.json().get('orders', [])
        # logging.debug(f"Orders fetched successfully: {orders}")
        return orders
    except requests.RequestException as e:
        error_message = f"Failed to get orders from API: {str(e)}"
        send_error_log(error_message, 'get_orders_from_api')
        logging.error(error_message)
        return []

def update_order_in_api(order_id, updated_data):
    """
    Updates the specified order in the API with the provided data.
    
    Args:
        order_id (str): The ID of the order to update.
        updated_data (dict): The data to update the order with.
    
    Returns:
        dict: The response from the API.
    """
    try:
        logging.debug(f"Updating order before {order_id} with data: {updated_data}")
        
        # Map the status before sending it to the API
        mapped_status = map_tradedupe_status('Dhan', updated_data.get('order_status', ''))
        logging.debug(f"Mapped status: {mapped_status}")
        
        updated_data['order_status'] = mapped_status
        logging.debug(f"Updating order after map_tradedupe_status {order_id} with data: {updated_data}")
        
        response = requests.put(f"{BASE_URL}/orders/{order_id}", json=updated_data)
        response.raise_for_status()
        
        result = response.json()
        logging.debug(f"Order {order_id} updated successfully: {result}")
        return result
    except requests.RequestException as e:
        error_message = f"Failed to update order {order_id} in API: {str(e)}"
        send_error_log(error_message, 'update_order_in_api')
        logging.error(error_message)



def close_strategy(strategy_id):
    url = 'http://localhost:5000/order/close-strategy'
    payload = {
        'strategy_id': strategy_id
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            logging.debug("Status updated successfully:", response.json())
        else:
            logging.debug("Failed to update status. Error:", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)





def check_pending_orders():
    """
    Continuously checks all orders from your system, compares them with the latest orders from the broker,
    updates order statuses and quantities as needed, and synchronizes them with the broker's data.
    Cancels child orders if one of them is successful.
    """
    while True:
        # Fetch all orders from your system
        orders_from_db = get_orders_from_api('/get-all-orders')

        if not orders_from_db:
            logging.debug("No orders found in the system.")
            time.sleep(10)
            continue

        # Fetch all orders from the broker
        response = dhan.get_order_list()

        if response['status'] == 'success' and response['data']:
            broker_orders = response['data']
            broker_order_lookup = {order['orderId']: order for order in broker_orders}

            parent_orders = {}

            for order in orders_from_db:
                broker_order_id = order.get('broker_order_id')

                if broker_order_id and broker_order_id in broker_order_lookup:
                    broker_order = broker_order_lookup[broker_order_id]
                    broker_order_status = broker_order.get('orderStatus')

                    logging.debug(f"Comparing system order {order['order_id']} with broker order {broker_order_id}.")

                    if broker_order_status == 'TRADED' and order['order_status'] != 'success':
                        logging.debug(f"Updating system order {order['order_id']} status to 'success'.")
                        update_order_in_api(order['order_id'], {'order_status': 'success'})
                        order['order_status'] = 'success'
                    elif broker_order_status == 'PENDING' and order['order_status'] != 'pending':
                        logging.debug(f"Updating system order {order['order_id']} status to 'pending'.")
                        update_order_in_api(order['order_id'], {'order_status': 'pending'})
                        order['order_status'] = 'pending'

                    # Group orders by entry order (parent)
                    parent_orders[order['main_order_id']] = parent_orders.get(order['main_order_id'], []) + [order]

            # Process the parent orders and their child orders
            for parent_order_id, child_orders in parent_orders.items():
                successful_order = None

                for child_order in child_orders:
                    if child_order['order_status'] == 'success':
                        successful_order = child_order
                        logging.debug(f"Found successful order: {successful_order['order_id']}, category: {successful_order['order_category']}.")
                        break

                # If one child order is successful, cancel the others
                if successful_order:
                    for child_order in child_orders:
                        if child_order['order_id'] != successful_order['order_id']:
                            if (successful_order['order_category'].lower() == 'target' and child_order['order_category'].lower() == 'stop_loss') or \
                               (successful_order['order_category'].lower() == 'stop_loss' and child_order['order_category'].lower() == 'target'):

                                logging.debug(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Attempting to cancel order {child_order['broker_order_id']}.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``")
                                try:
                                    cancel_response = dhan.cancel_order(child_order['broker_order_id'])
                                    logging.debug(f"Cancel response for {child_order['broker_order_id']}: {cancel_response}")
                                    # if cancel_response['status'] == 'success':
                                    if cancel_response['remarks']['message'] == 'Order Is Cancelled.kindly Refresh Your Orderbook':
                                        logging.debug(f"Successfully cancelled {child_order['order_id']}.")
                                        update_order_in_api(child_order['order_id'], {'order_status': 'CANCELLED'})
                                        close_strategy(child_order['strategy_id'])
                                    else:
                                        logging.error(f"Failed to cancel order {child_order['order_id']} with broker.")
                                except Exception as e:
                                    logging.error(f"Exception while cancelling order {child_order['order_id']}: {str(e)}")

        else:
            logging.error("Failed to fetch orders from broker. Response may be invalid or None.")

        time.sleep(2)



# update_order_in_api(9124092422966, {'order_status': 'cancelled'})
# close_strategy(65)