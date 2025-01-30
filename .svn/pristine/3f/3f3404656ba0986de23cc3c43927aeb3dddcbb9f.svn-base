import csv
from datetime import datetime

def check_risk_order_status(strategy_id, order_file):
    """
    Checks if any risk order (bookprofit or stop_loss) for a given strategy ID has status SUCCESS.
    
    Args:
    - strategy_id (str): The ID of the strategy to check.
    - order_file (str): The path to the order file.
    
    Returns:
    - bool: True if any risk order has status SUCCESS, False otherwise.
    """
    with open(order_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['strategy_id'] == strategy_id and row['OrderCategory'] in ['Target', 'Stop_loss'] and row['orderStatus'] == 'success':
                return True
    return False

def update_strategy_statusforexecutioncount(strategy_id):
    """
    Updates the status of the strategy in the strategy file to 'waiting' if any risk order is successful.
    
    Args:
    - strategy_id (str): The ID of the strategy to update.
    """
    strategy_file = 'Input_Files/strategy.csv'
    order_file = 'orders.csv'  # Assuming this is the order file
    updated_rows = []
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check risk order status
    if not check_risk_order_status(strategy_id, order_file):
        print(f"No successful risk orders found for strategy ID {strategy_id}.")
        return

    # Update strategy status
    with open(strategy_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['strategy_id'] == strategy_id:
                row['status'] = 'waiting'
                row['last_execution_date'] = current_datetime
            updated_rows.append(row)

    with open(strategy_file, 'w', newline='') as file:
        fieldnames = updated_rows[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"Strategy ID {strategy_id} status updated to 'waiting'.")

# Example usage
# update_strategy_status('S_82382')
