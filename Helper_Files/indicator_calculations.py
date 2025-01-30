


import logging
from datetime import datetime, timedelta
from Helper_Files.calculate_sma import calculate_sma
from Helper_Files.rsi import calculate_rsi
from Helper_Files.fetch_historical_data import fetch_historical_data
from Helper_Files.send_error_log import send_error_log
from Helper_Files.indicator_manager import sma_indicator,rsi_indicator


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the date range for historical data
fromDate = '2023-05-01'
toDate = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')



def indicator_validations(strategy_data, symbol, security_id):
    logging.debug(f"in indicator_validations")
    # logging.debug(f"strategy_data:",strategy_data) 
    indicators = strategy_data.get('indicators', [])
    actions = strategy_data.get('actions', [])
    exchange = strategy_data['strategy']['exchange']
    # logging.debug(f"exchange in indicator_validations: {exchange}.")
    # logging.debug(f"indicators in indicator_validations: {indicators}.")
    combined_order_flag = False
    rsi_calculated = False  # Flag to track RSI calculation

    # global rsi_call_count  # To modify the global counter

    for indicator in indicators:
        try:
            if indicator['indicator_name'] == 'SMA':
                combined_order_flag = sma_indicator(strategy_data,symbol, exchange,security_id)
                logging.debug(f"SMA combined_order_flag: {combined_order_flag} in Simple Moving Average.")
                
                if not combined_order_flag:
                    logging.debug("SMA condition failed. Stopping further processing.")
                    return False  # Stop further processing

            elif indicator['indicator_name'] == 'RSI' and not rsi_calculated:
         
                logging.debug(f"RSI function called.")
                # Only calculate RSI if not already calculated
                # rsi_call_count += 1  # Increment the call counter
                # logging.debug(f"RSI function called {rsi_call_count} times.")

                # combined_order_flag = rsi_indicator(indicators, strategy_data, symbol, actions, fromDate, toDate)
                combined_order_flag = rsi_indicator(strategy_data,symbol, exchange,security_id,indicators, actions)
                rsi_calculated = True  # Set the flag after the first calculation

                logging.debug(f"RSI combined_order_flag: {combined_order_flag} in Relative Strength Index.")
                if not combined_order_flag:
                    logging.debug("RSI condition failed. Stopping further processing.")
                    return False  # Stop further processing

        except Exception as e:
            error_message = f"Error processing {indicator['indicator_name']} for symbol {symbol}: {str(e)}"
            send_error_log(error_message, 'strategy_engine')

    return combined_order_flag
