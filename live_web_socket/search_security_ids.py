




# import csv
# import json
# import logging
# import requests
# from Helper_Files.send_error_log import send_error_log

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# def search_security_ids(symbols):
#     logging.debug("Starting search_security_ids")
#     logging.debug(f"Symbols in search_security_ids: {symbols}")
    
#     api_url = 'http://localhost:5000/python/processSymbols'  # URL of your Node.js API
#     headers = {'Content-Type': 'application/json'}
    
#     # Convert symbols list to JSON format
#     payload = {'symbols': symbols}
    
#     try:
#         # Send POST request to Node.js API
#         response = requests.post(api_url, headers=headers, data=json.dumps(payload))
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         # logging.debug(f"API response: {response.json()}")
        
#         if response.status_code == 200:
#             result = response.json()
#             security_ids = result.get('securityIds', [])  # Get securityIds from response
            
#             if not security_ids:
#                 logging.warning("No security IDs received from the API.")
#                 return []  # Return empty list if no data received
            
#             logging.debug(f"Received security IDs: {security_ids}")
            
#             # Write the results to a CSV file
#             output_file_path = "D:/shashikant kamthe/Main code/python/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/Input_Files/unique_symbols_security_ids.csv"
            
#             try:
#                 with open(output_file_path, mode='w', newline='') as csvfile:
#                     writer = csv.writer(csvfile)
#                     writer.writerow(['Symbol', 'Exchange ID', 'Security ID'])
#                     for item in security_ids:
#                         writer.writerow([item['symbol'], item['exchange'], item['securityId']])
#                 logging.info(f"Data successfully written to {output_file_path}")
#             except Exception as e:
#                 logging.error(f"Error occurred while writing to CSV file: {e}")
#                 send_error_log(str(e), 'search_security_ids')
#         else:
#             logging.error(f"Failed to get data from API: {response.status_code}")
#             logging.error(f"Response: {response.text}")
#             send_error_log(response.text, 'search_security_ids')
#     except requests.RequestException as e:
#         logging.error(f"Error during API request: {e}")
#         send_error_log(str(e), 'search_security_ids')
    
#     return security_ids  # Return the list of security IDs


import csv
import json
import logging
import requests
from Helper_Files.send_error_log import send_error_log
import os
from pathlib import Path
from constants import BASE_URL  # Import the global base URL

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def search_security_ids(symbols):
    logging.debug("Starting search_security_ids")
    logging.debug(f"Symbols in search_security_ids: {symbols}")
    
    # api_url = 'http://localhost:5000/python/processSymbols'  # URL of your Node.js API
    api_url = f"{BASE_URL}python/processSymbols"  # Use the global base URL
    headers = {'Content-Type': 'application/json'}
    
    # Convert symbols list to JSON format
    payload = {'symbols': symbols}
    
    try:
        # Send POST request to Node.js API
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        if response.status_code == 200:
            result = response.json()
            security_ids = result.get('securityIds', [])  # Get securityIds from response
            
            if not security_ids:
                logging.warning("No security IDs received from the API.")
                return []  # Return empty list if no data received
            
            # logging.debug(f"Received security IDs: {security_ids}")
            
            base_dir = Path("D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/Input_Files")
            output_file_path = base_dir / "unique_symbols_security_ids.csv"
            # Log the security IDs before writing to CSV
            logging.debug(f"Security IDs to be written: {security_ids}")
            
            try:
                with open(output_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Symbol', 'Exchange ID', 'Security ID'])
                    for item in security_ids:
                        writer.writerow([item['symbol'], item['exchange'], item['securityId']])
                logging.info(f"Data successfully written to {output_file_path}")
                
                # Check the file size after writing
                if os.path.exists(output_file_path):
                    file_size = os.path.getsize(output_file_path)
                    logging.debug(f"File size after writing: {file_size} bytes")
                    
            except Exception as e:
                logging.error(f"Error occurred while writing to CSV file: {e}")
                send_error_log(str(e), 'search_security_ids')
        else:
            logging.error(f"Failed to get data from API: {response.status_code}")
            logging.error(f"Response: {response.text}")
            send_error_log(response.text, 'search_security_ids')
    except requests.RequestException as e:
        logging.error(f"Error during API request: {e}")
        send_error_log(str(e), 'search_security_ids')
    
    return security_ids  # Return the list of security IDs
