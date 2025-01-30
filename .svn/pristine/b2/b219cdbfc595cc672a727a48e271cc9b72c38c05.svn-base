import csv
from collections import OrderedDict

from Helper_Files.strategy_combiner import update_strategy_status
# from save_order_to_csv import save_order_to_csv
from Helper_Files.save_executed_order import save_executed_order

from Helper_Files.Risk_management import place_stop_loss_order,place_book_profit_order,cancel_pending_orders,check_pending_orders


def save_paper_order(order_details, strategy_id, MainOrderid=None, ordertype="mainorder"):
    print("save_paper_order MainOrderid:", MainOrderid)
    file_path = 'paper_orders.csv'
    
    # Define the headers for the CSV file
    headers = ['strategy_id', 'MainOrderid', 'RiskOrder', 'orderStatus', 'orderId', 'transaction_type', 'exchange_segment',
               'product_type', 'order_type', 'validity', 'security_id', 'quantity', 'price', 'bo_profit_value', 'bo_stop_loss_value','symbol','date']

    # Check if the file exists and has content
    file_exists = False
    header_exists = False
    try:
        with open(file_path, 'r', newline='') as f:
            # Check if the file is empty
            file_exists = True
            first_line = f.readline()
            if first_line:
                # Check if the first line matches the headers
                header_exists = (first_line.strip().split(',') == headers)
    except FileNotFoundError:
        pass
    
    # Save the order details to the CSV file
    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        
        # Write the header only if the file did not exist or if the header was missing
        if not file_exists or not header_exists:
            writer.writeheader()
        
        # Create an OrderedDict to ensure the order of keys matches the headers
        order_details_with_strategy_id = OrderedDict()
        order_details_with_strategy_id['strategy_id'] = strategy_id
        order_details_with_strategy_id['MainOrderid'] = MainOrderid if MainOrderid else 'N/A'
        order_details_with_strategy_id['RiskOrder'] = ordertype
        
        # Flatten the order details to match the headers
        for header in headers[3:]:  # Skip 'strategy_id', 'MainOrderid', and 'RiskOrder' as they have been added
            order_details_with_strategy_id[header] = order_details.get(header, 'N/A')

        writer.writerow(order_details_with_strategy_id)
