# from dhanhq import marketfeed
# import csv
# import os
# import asyncio
# import logging
# from constants import access_token,client_id

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# async def on_connect(instance):
#     logging.debug("Connected to websocket")

# async def on_message(instance, message):
#     logging.debug(f"ENTERED IN THE on_message live_websocket ")
#     try:
#         if 'type' in message:
#             if message['type'] == 'Ticker Data':
#                 # Check if the file exists, if not, write the header row
#                 if not os.path.exists('D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/live_web_socket/dhan_LTP.csv'):
#                     with open('D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/live_web_socket/dhan_LTP.csv', 'w', newline='') as csvfile:
#                         writer = csv.writer(csvfile)
#                         writer.writerow(['Type', 'Exchange Segment', 'Security ID', 'LTP', 'LTT'])
                
#                 # Read the existing data
#                 existing_data = {}
#                 if os.path.exists('D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/live_web_socket/dhan_LTP.csv'):
#                     with open('D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/live_web_socket/dhan_LTP.csv', 'r', newline='') as csvfile:
#                         reader = csv.DictReader(csvfile)
#                         for row in reader:
#                             existing_data[row['Security ID']] = row

#                 # Update the data for the current security ID
#                 existing_data[message.get('security_id', '')] = {
#                     'Type': message.get('type', ''),
#                     'Exchange Segment': message.get('exchange_segment', ''),
#                     'Security ID': message.get('security_id', ''),
#                     'LTP': message.get('LTP', ''),
#                     'LTT': message.get('LTT', '')
#                 }

#                 # Write the data back to the CSV file
#                 with open('D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/live_web_socket/dhan_LTP.csv', 'w', newline='') as csvfile:
#                     fieldnames = ['Type', 'Exchange Segment', 'Security ID', 'LTP', 'LTT']
#                     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                     writer.writeheader()
#                     for row in existing_data.values():
#                         writer.writerow(row)

#     except Exception as e:
#         logging.debug("Error processing message:", e)
#         logging.debug("Message causing the issue:", message)





# async def live_websocket(instruments):
#     connected = False
#     # logging.debug("Formatted instruments:", formatted_instruments)
#     while not connected:
#         try:
#             # Convert instruments to the desired format
#             formatted_instruments = [(item['exchangeId'], item['securityId']) for item in instruments]
#             logging.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~in live_websocket")
            
#             # client_id = "1101343871"
#             # access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzI4ODAxODg5LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMTM0Mzg3MSJ9.Rcr4VMpNakJvYB0ThB84v0DOaxiMRIZZoeqol8QAGEEgvPJJ3SpBsZVIyAcJvscOO3HPkx1fI0r6uZwV99V08g'  # Replace with your actual access token
            
#             # logging.debug(f'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', )
#             # logging.debug(f'Processing instruments for ltp:::::::::::::::::::: %s', formatted_instruments)
#             # logging.debug(f'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', )

#             # Type of data subscription
#             subscription_code = marketfeed.Ticker

#             print("Subscription code :", subscription_code)

#             feed = marketfeed.DhanFeed(
#                 client_id,
#                 access_token,
#                 formatted_instruments,
#                 subscription_code,
#                 on_connect=on_connect,
#                 on_message=on_message
#             )

#             await feed.connect()  # Await the connect coroutine
#             await feed.run_forever()  # Await the run_forever coroutine

#             connected = True  # Set connected to True if connection successful
#         except Exception as e:
#             logging.debug("Error connecting to websocket:", e)
#             await asyncio.sleep(2)  # Retry after 2 seconds if connection failsss
# import asyncio
# import logging
# from dhanhq import marketfeed
# from constants import access_token, client_id
# logging.basicConfig(level=logging.DEBUG)
# from constants import access_token,client_id

# def map_exchange(exchange_name):
#     exchange_mapping = {
#         'MCX': marketfeed.MCX,
#         'NSE': marketfeed.NSE,
#         'BSE': marketfeed.BSE
#     }
#     return exchange_mapping.get(exchange_name.upper())

# # Function to process symbols and fetch market data
# def live_websocket(symbols):
#     try:
#         # Transform the symbols into the desired instruments list
#         instruments = []
#         for item in symbols:
#             exchange = map_exchange(item['exchange'])
#             if exchange:
#                 instruments.append((exchange, item['securityId'], marketfeed.Ticker))  # Ticker - Ticker Data
        
#         # Initialize the DhanFeed instance with the instruments
#         data = marketfeed.DhanFeed(client_id, access_token, instruments)

#         # Start the WebSocket connections
#         data.run_forever()

#         # Fetch and print data
#         while True:
#             response = data.get_data()
#             print(response)

#     except Exception as e:
#         print(f"Error: {e}")

#     # Ensure disconnection
#     finally:
#         if 'data' in locals():
#             data.disconnect()


# import logging
# import asyncio
# from dhanhq import marketfeed
# from constants import access_token, client_id

# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# def map_exchange(exchange_name):
#     """Map the exchange name to marketfeed exchange class."""
#     exchange_mapping = {
#         'MCX': marketfeed.MCX,
#         'NSE': marketfeed.NSE,
#         'BSE': marketfeed.BSE
#     }
#     return exchange_mapping.get(exchange_name.upper())

# async def live_websocket(symbols):
#     """Fetch market data for the provided symbols using WebSocket."""
#     logging.debug(f"Initializing DhanFeed with {symbols} instruments.")
#     instruments = []
    
#     # Prepare instruments based on symbols
#     for item in symbols:
#         exchange = map_exchange(item['exchange'])
#         if exchange:
#             instruments.append((exchange, item['securityId'], marketfeed.Ticker))  # Ticker - Ticker Data
#         else:
#             logging.warning(f"Invalid exchange for symbol: {item['symbol']}")

#     try:
#         # Initialize the DhanFeed instance with the instruments
#         logging.debug(f"Initializing DhanFeed with {len(instruments)} instruments.")
#         data = marketfeed.DhanFeed(client_id, access_token, instruments)

#         # Start the WebSocket connection
#         logging.debug("Starting WebSocket connection...")
#         await data.connect()  # Ensure that we await the coroutine

#         # Fetch and print data in real-time
#         while True:
#             try:
#                 response = await data.get_data()  # Await the coroutine properly
#                 if response:
#                     logging.debug(f"Received data: {response}")
#                 else:
#                     logging.debug("Received empty data response.")
#             except Exception as e:
#                 logging.error(f"Error fetching data: {e}")
#                 break  # Break out of the loop in case of errors

#     except Exception as e:
#         logging.error(f"Error during WebSocket connection: {e}")
#         send_error_log(f"WebSocket connection error: {e}", 'live_websocket')

#     finally:
#         # Ensure disconnection from the WebSocket
#         if 'data' in locals():
#             await data.disconnect()  # Await the disconnect coroutine
#             logging.debug("Disconnected from WebSocket.")

# def send_error_log(message, function_name):
#     """Send error logs to a logging system or external service."""
#     logging.error(f"Error in {function_name}: {message}")

# async def run_websocket_thread(symbols):
#     logging.debug("Starting WebSocket.")
#     try:
#         await live_websocket(symbols)  # Await the WebSocket directly
#         logging.debug("WebSocket finished.")
#     except Exception as e:
#         logging.error(f"Error in WebSocket: {e}")

import asyncio
import threading
import logging
import nest_asyncio
from dhanhq import marketfeed
from constants import access_token, client_id
# logging.basicConfig(level=logging.DEBUG)
import csv
import os


# Allow nest_asyncio to patch the current event loop
nest_asyncio.apply()

CSV_FILE_PATH = 'D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/live_web_socket/dhan_LTP.csv'

# Initialize the CSV file with header
def initialize_csv():
    if not os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['exchange_segment', 'security_id', 'LTP', 'LTT'])
            writer.writeheader()

def map_exchange(exchange_name):
    exchange_mapping = {
        'MCX': marketfeed.MCX,
        'NSE': marketfeed.NSE,
        'BSE': marketfeed.BSE
    }
    return exchange_mapping.get(exchange_name.upper())

# Function to process symbols and fetch market data using WebSocket
async def live_websocket(symbols):
    """Simulate the WebSocket task with live market data retrieval."""
    try:
        # Transform the symbols into the desired instruments list
        instruments = []
        for item in symbols:
            exchange = map_exchange(item['exchange'])
            if exchange:
                instruments.append((exchange, item['securityId'], marketfeed.Ticker))  # Ticker - Ticker Data
        
        # Initialize the DhanFeed instance with the instruments
        data = marketfeed.DhanFeed(client_id, 
                                   access_token, 
                                   instruments=instruments)
        
        # Attempt to connect (ensure this is awaited or handled properly)
        await data.connect()  # Assuming connect is async
        
        # Start the WebSocket connections (this will be handled by the WebSocket client)
        loop = asyncio.get_event_loop()
        task = loop.run_in_executor(None, data.run_forever)  # Run blocking WebSocket in the background
        
        # Fetch and process data
        while True:
            response = data.get_data()  # Fetch the data
            logging.debug(f"Received data: {response}")  # For example, logging it

            if response.get('type') == 'Ticker Data':
                store_to_csv(response)
            await asyncio.sleep(1)  # Simulate periodic data fetching, adjust as needed

    except Exception as e:
        logging.error(f"Error in live_websocket: {e}")
    
    # Ensure disconnection (await the disconnect coroutine)
    finally:
        if 'data' in locals():
            await data.disconnect()  # Properly await the disconnect
            logging.debug("Disconnected from WebSocket")

# Function to run WebSocket in a separate thread
def run_websocket_thread(symbols):
    """Run the WebSocket engine in an asyncio event loop in a separate thread."""
    logging.debug("Starting WebSocket thread.")
    
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If the event loop is already running, create and await the task
        task = loop.create_task(live_websocket(symbols))
        loop.run_until_complete(task)
    else:
        # If no event loop is running, create a new one and set it for the thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(live_websocket(symbols))
        loop.run_until_complete(task)

    logging.debug("WebSocket thread finished.")
    """Run the WebSocket engine in an asyncio event loop in a separate thread."""
    logging.debug("Starting WebSocket thread.")
    
    # Get the current event loop (it can be used in the current thread due to nest_asyncio)
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If the event loop is already running, create and await the task
        task = loop.create_task(live_websocket(symbols))
        loop.run_until_complete(task)
    else:
        # If no event loop is running, create a new one and set it for the thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(live_websocket(symbols))
        loop.run_until_complete(task)

    logging.debug("WebSocket thread finished.")


# Function to store data to CSV
def store_to_csv(data):
    """Update the CSV file with the latest data for the given Security ID."""
    try:
        updated = False
        csv_file_path = CSV_FILE_PATH
        updated_rows = []

        # Read the existing data
        with open(csv_file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Check if this row matches the Security ID
                if row['Security ID'] == str(data['security_id']):
                    # Update this row
                    row['Exchange Segment'] = str(data['exchange_segment'])
                    row['LTP'] = str(data['LTP'])
                    row['LTT'] = data['LTT']
                    updated = True
                updated_rows.append(row)

        # If no row was updated, append the new data
        if not updated:
            updated_rows.append({
                'Exchange Segment': str(data['exchange_segment']),
                'Security ID': str(data['security_id']),
                'LTP': str(data['LTP']),
                'LTT': data['LTT']
            })

        # Write the updated rows back to the file
        with open(csv_file_path, mode='w', newline='') as file:
            fieldnames = ['Exchange Segment', 'Security ID', 'LTP', 'LTT']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

        logging.debug(f"CSV updated successfully with data: {data}")

    except Exception as e:
        logging.error(f"Error updating CSV: {e}")
