import time
import threading
import logging
import asyncio
import csv
from datetime import datetime, timedelta

from Helper_Files.strategy_combiner import combine_data
from Helper_Files.check_pending_orders import check_pending_orders

from live_web_socket.live_websocket import live_websocket
from live_web_socket.search_security_ids import search_security_ids
from Helper_Files.get_latest_ltp import get_latest_ltp
from Helper_Files.place_order import place_order_by_broker
from Helper_Files.unique_symbol import get_unique_symbols
# from Helper_Files.read_security_ids import read_security_ids
from Helper_Files.send_error_log import send_error_log
from Helper_Files.indicator_calculations import indicator_validations
from live_web_socket.live_websocket import run_websocket_thread


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# def read_security_ids(file_path):
#     security_ids_map = {}
#     try:
#         logging.debug(f"returning security_ids_map file_path: {file_path}")
#         with open(file_path, newline='') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 symbol = row['Symbol']
#                 exchange_id = int(row['Exchange ID'])
#                 security_id = int(row['Security ID'])
#                 security_ids_map[symbol] = (exchange_id, security_id)
#                 logging.debug(f"returning security_ids_map: {security_ids_map}")
#     except Exception as e:
#         error_message = f"Error reading security IDs: {str(e)}"
#         send_error_log(error_message, 'read_security_ids')
        
#     return security_ids_map

def read_security_ids(file_path):
    security_ids_map = {}
    try:
        logging.debug(f"Reading security IDs from file: {file_path}")
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                symbol = row['Symbol']
                exchange_id = row['Exchange ID'].strip().upper()  # Use the string directly
                security_id = int(row['Security ID'])  # Convert Security ID to integer
                security_ids_map[symbol] = (exchange_id, security_id)
        logging.debug(f"Successfully read security IDs: {security_ids_map}")
    except Exception as e:
        error_message = f"Error reading security IDs: {str(e)}"
        logging.error(error_message)
        send_error_log(error_message, 'read_security_ids')
        
    return security_ids_map




async def process_symbols(symbols):
    """Fetch and process symbols with live WebSocket in a separate thread."""
    logging.debug("Starting to process symbols.")
    security_ids_list = search_security_ids(symbols)
    # logging.debug(f"Security IDs List: {security_ids_list}")
    run_websocket_thread(security_ids_list)  # Updated function call

    # Start a new thread for WebSocket
    # thread = threading.Thread(target=run_websocket_thread, args=(security_ids_list,))
    # thread.start()  # Start the thread
    # thread.join()   # Wait for the thread to finish
    # Run the WebSocket in a new thread to fetch real-time data
    # live_websocket_thread = threading.Thread(target=run_live_websocket_in_thread, args=(security_ids_list,))
    # live_websocket_thread.start()
    # live_websocket_thread.join()  # Wait for the WebSocket thread to finish


# def run_live_websocket_in_thread(security_ids_list):
#     """Runs the live_websocket coroutine in a separate thread with its own event loop."""
#     loop = asyncio.new_event_loop()  # Create a new event loop for this thread
#     asyncio.set_event_loop(loop)  # Set the new event loop for this thread
    
#     try:
#         loop.run_until_complete(live_websocket(security_ids_list))
#     except Exception as e:
#         logging.error(f"Error in live_websocket thread: {e}")
#     finally:
#         loop.close()  # Ensure the event loop is closed properly after the task



async def websocket_engine(csv_symbols_event):
    logging.debug(f"Starting websocket engine")
    # while not csv_symbols_event.is_set():
    #     await asyncio.sleep(1)  # Check every second if the event is set
    # csv_symbols_event.wait()
   
    symbols = get_unique_symbols()
    # logging.debug(f"symbols websocket_engine: '{symbols}'")  
    
    # logging.debug(f"symbols from get_unique_symbols:",symbols)
    await process_symbols(symbols)
    # logging.debug(f"symbols after process_symbolsss: '{symbols}'")  

def strategy_engine(strategy_file, csv_symbols_event, strategy_done_event):
   
    security_ids_map = read_security_ids('D:/shashikant kamthe/Main code/svn/repo_Trading/Strategy_Builder/Python_StrategyBuilder_v1/Input_Files/unique_symbols_security_ids.csv')

    strategy_executed = True
    while not strategy_done_event.is_set():
        logging.debug("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Starting strategy engine~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # logging.debug(f"security_ids_map: {security_ids_map}")
        strategy_data_list = combine_data()
        # logging.debug(f"strategy_data_list combine_data response:", strategy_data_list)
        symbols = get_unique_symbols()
        csv_symbols_event.set()

        if not symbols:
            logging.error("No symbols found in strategy file.")
            return

        

        if strategy_data_list:
            waiting_strategy_exists = any(strategy_data['strategy']['status'] == 'waiting' for strategy_data in strategy_data_list)
            logging.debug(f"waiting_strategy_exists: {waiting_strategy_exists}")


            if not waiting_strategy_exists:
                logging.debug("No waiting strategies found")
                send_error_log("No waiting strategies found", 'strategy_engine')
                time.sleep(1)
                continue

            for strategy_data in strategy_data_list:
                if strategy_data['strategy']['status'] == 'executed':
                    logging.debug("Skipping strategy '%s' because it's already executed", strategy_data['strategy']['strategy_name'])
                    continue
                
                symbol = strategy_data['strategy']['symbol']

                # logging.debug("strategy_data:", {strategy_data})
                logging.debug(f"security_ids_map: {security_ids_map}")
                security_id = security_ids_map.get(symbol, (None, None))[1]
                # security_id =539300
                logging.debug(f"Security ID for symbol {symbol}: {security_id}")

                if security_id is None:
                    error_message = f"No security ID found for symbol: {symbol}"
                    send_error_log(error_message, 'strategy_engine')
                    continue

                # data = fetch_historical_data(symbol, strategy_data['strategy']['exchange'], fromDate, toDate, period=None)
                # latest_ltp = get_latest_ltp(security_id)
                # logging.debug(f"calling combined_order_flag indicator_validations") 
            
                # Process indicators using the new function
                combined_order_flag = indicator_validations(strategy_data,  symbol, security_id)
                logging.debug(f"combined_order_flag on strategy '{combined_order_flag}'")  
                # Determine whether to place an order based on the processed indicators
                # combined_order_flag = True
                if combined_order_flag:
                    logging.debug(f"Placing order based on strategy '{strategy_data['strategy']['strategy_name']}'") 
                    # place_order(strategy_data['actions'], strategy_data['strategy']['strategy_id'], strategy_data, security_id)
                    place_order_by_broker(strategy_data['actions'], strategy_data['strategy']['strategy_id'], strategy_data, security_id)
                    strategy_executed = True
                else:
                    logging.debug(f"No order placed for strategy '{strategy_data['strategy']['strategy_name']}'")
                    continue

                if not strategy_executed:
                    time.sleep(1)

def status_update_engine(strategy_done_event):
    logging.debug(f"status_update_engine")
    while not strategy_done_event.is_set():
        try:
            # Place the logic to update strategy status here
            check_pending_orders()  # Define this function as per your logic
            time.sleep(2)  # Adjust the sleep time as per your requirements
        except Exception as e:
            error_message = f"Error in status update engine: {e}"
            send_error_log(error_message, 'status_update_engine')
    logging.debug(f"Status update engine stopped")


if __name__ == "__main__":
    logging.debug(f"Main program started")
    csv_symbols_event = threading.Event()
    strategy_done_event = threading.Event()
    strategy_thread = threading.Thread(target=strategy_engine, args=('Input_Files/strategy.csv', csv_symbols_event, strategy_done_event))
    LTPSecurityFetchThread = threading.Thread(target=lambda: asyncio.new_event_loop().run_until_complete(websocket_engine(csv_symbols_event)))
    status_update_thread = threading.Thread(target=status_update_engine, args=(strategy_done_event,))
    live_websocket_thread = threading.Thread(target=run_websocket_thread, args=([]))
    


    try:
        strategy_thread.start()
        LTPSecurityFetchThread.start()
        status_update_thread.start()
      
        strategy_thread.join()
        strategy_done_event.set()
        LTPSecurityFetchThread.join()
        live_websocket_thread.start()
        live_websocket_thread.join()  # Wait for the WebSocket thread to finish
        status_update_thread.join()
    except KeyboardInterrupt:
        logging.debug(f"KeyboardInterrupt received. Shutting down.")
        strategy_done_event.set()
        strategy_thread.join()
        LTPSecurityFetchThread.join()
        status_update_thread.join()
    finally:
        logging.debug(f"Main program finished")
