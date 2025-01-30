

from Helper_Files.save_paper_order import save_paper_order
from Helper_Files.strategy_combiner import update_strategy_status
from datetime import datetime
def get_exchange_and_transaction(strategy_data):
    try:
        # Extract exchange_segment, transaction_type, and order_type from strategy_data
        exchange_segment = strategy_data['strategy']['exchange']
        transaction_type = strategy_data['actions'][0]['action_type']  # Assuming only one action for simplicity
        order_type = strategy_data['actions'][0]['action_name']  # Assuming only one action for simplicity

        return exchange_segment, transaction_type, order_type

    except KeyError as e:
        print(f"KeyError: {e}. Strategy data structure is not as expected.")
        return None, None, None
    except Exception as e:
        print(f"Error: {e}. Failed to retrieve exchange_segment, transaction_type, and order_type.")
        return None, None, None







def place_paper_trade_order(actions, strategy_id, strategy_data, security_id):
    print("Placing paper strategy_data,...:", strategy_data)




    
    # Retrieve exchange_segment, transaction_type, and order_type using the function
    exchange_segment, transaction_type, order_type = get_exchange_and_transaction(strategy_data)
    
    if exchange_segment is None or transaction_type is None or order_type is None:
        print("Failed to retrieve exchange_segment, transaction_type, or order_type. Aborting paper order placement.")
        return
    
    try:
        for action in actions:
            print("Simulating action:", action['action_name'])

            # Extract necessary parameters from the action
            security_id = security_id  # Use the provided security_id
            quantity = 1  # Default to 1 if not provided
            product_type = "INTRA"  # Assuming INTRA; update if necessary
            price = 0  # Default to 0 if not provided
            
            # Log the order details instead of placing a real order
            order_details = {
            "transaction_type": transaction_type,
            "exchange_segment": exchange_segment,
            "symbol":strategy_data['strategy']['symbol'],
           "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "product_type": product_type,
            "order_type": action['action_name'],
            "validity": 'DAY',
            "security_id": security_id,
            "quantity": quantity,
            "price": price,
            "bo_profit_value": action.get('BracketTarget', 0),
            "bo_stop_loss_Value": action.get('BracketStopLoss', 0),
            "MainOrderid": strategy_id,
            "orderStatus":"success",
        }
            
            print(f"Simulated order placed for {action['action_name']}. Details: {order_details}")
            
            # Simulate the successful order placement
            order_data = {
                'orderStatus': 'TRANSIT',
                'orderId': f"sim-{strategy_id}-{security_id}"
            }
            # place_book_profit_order(order_data, strategy_id, strategy_data)
            # place_stop_loss_order(order_data, strategy_id, strategy_data)
            save_paper_order(order_details, strategy_id, MainOrderid=None, ordertype="main_order")
    
    except Exception as e:
        print(f"Failed to simulate order for {action['action_name']}: {e}")
    
    # Update the strategy status after placing the simulated order
    # update_strategy_status(strategy_id)
