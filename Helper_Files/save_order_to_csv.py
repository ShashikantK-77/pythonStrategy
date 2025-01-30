# import csv
# import os

# def save_order_to_csv(response, file_path='Order.csv'):
#     file_exists = os.path.isfile(file_path)
#     with open(file_path, mode='a', newline='') as file:
#         writer = csv.writer(file)
        
#         # # Write the header only if the file does not exist
#         # if not file_exists:
#         #     writer.writerow(['order_id', 'security_id', 'exchange_segment', 'transaction_type', 'quantity', 'order_type', 'product_type', 'price', 'status', 'message'])
        
#         # # Extract data from the response and write it to the CSV file
#         # order_data = [
#         #     response.get('order_id', ''),
#         #     response.get('security_id', ''),
#         #     response.get('exchange_segment', ''),
#         #     response.get('transaction_type', ''),
#         #     response.get('quantity', ''),
#         #     response.get('order_type', ''),
#         #     response.get('product_type', ''),
#         #     response.get('price', ''),
#         #     response.get('status', ''),
#         #     response.get('message', '')
#         # ]
#         writer.writerow(response)



import csv
import os

def save_order_to_csv(response, file_path='Order.csv'):
    print("in save_order_to_csv")
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header only if the file does not exist
        if not file_exists:
            writer.writerow(response.keys())
        
        # Write the response values to the CSV file
        writer.writerow(response.values())