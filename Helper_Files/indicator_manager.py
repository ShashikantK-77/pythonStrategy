import logging

from datetime import datetime, timedelta
from Helper_Files.calculate_sma import calculate_sma
from Helper_Files.rsi import calculate_rsi
from Helper_Files.fetch_historical_data import fetch_historical_data
from Helper_Files.send_error_log import send_error_log

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to handle SMA indicator logic
def sma_indicator(strategy_data, symbol,exchange,security_id):
                    # (strategy_data,symbol, exchange,security_id)
    logging.debug(f"in sma_indicator strategy_data.",strategy_data)
    try:
        # Extract SMA parameters
        parameters = {}
        actions = strategy_data.get('actions', [])
        for param in strategy_data.get('indicators', []):
            param_value = param['param_value']
            try:
                # Attempt to convert the value to an integer, otherwise leave it as a string
                param_value = int(param_value)
            except ValueError:
                # Non-numeric values will remain as they are
                pass
            parameters[param['param_name']] = param_value
        
        short_term_period = parameters.get('short_term_period')
        long_term_period = parameters.get('long_term_period')

        logging.debug(f"SMA ({parameters}). in Simple Moving Average.")
        
        # Fetch historical data
        hdata = fetch_historical_data(symbol, exchange,security_id)
        # logging.debug(f"SMA hdata ({hdata}). in Simple Moving Average.")

        # If both short-term and long-term periods are provided, calculate SMA
        if short_term_period and long_term_period:
            short_term_sma = calculate_sma(hdata, short_term_period)
            long_term_sma = calculate_sma(hdata, long_term_period)
            
            logging.debug(f"Short-term SMA: {short_term_sma}, Long-term SMA: {long_term_sma}")
            # logging.debug(f"actions: {actions}")
            # Compare short-term and long-term SMA, and check for 'buy' action
            if short_term_sma > long_term_sma and any(action['action_name'] == 'buy' for action in actions):
            # if any(action['action_name'] == 'buy' for action in actions):
                logging.debug("Short-term SMA is greater than Long-term SMA. 'buy' action found.")
                return True

        logging.debug("SMA conditions not met or no 'buy' action found.")
        return False
    except Exception as e:
        error_message = f"Error processing Simple Moving Average for symbol {symbol}: {str(e)}"
        send_error_log(error_message, 'strategy_engine')
        return False
    

def rsi_indicator(strategy_data,symbol, exchange,security_id,indicators, actions):

    logging.debug(f"in rsi_indicator")
    try:
        # Extract and parse RSI parameters
        logging.debug(f"in rsi_indicator")
        rsi_params = {param['param_name']: float(param['param_value']) for param in indicators if param['param_name'] in ['overbought', 'oversold', 'period']}
        
        # Set default values if parameters are missing
        overbought = rsi_params.get('overbought', 70)
        oversold = rsi_params.get('oversold', 30)
        period = int(rsi_params.get('period', 14))
        
        logging.debug(f"RSI Params: {rsi_params}")
        logging.debug(f"RSI Parameters - Overbought: {overbought}, Oversold: {oversold}, Period: {period}")

        # Fetch historical data for RSI calculation
        hdata = fetch_historical_data(symbol, exchange,security_id)
        # logging.debug(f"hdata: {hdata}")
        # logging.debug(f"RSI hdata: {hdata}")
        # Calculate RSI

        rsi = calculate_rsi(hdata)
        current_rsi = rsi.iloc[-1]  # Latest RSI value
        logging.debug(f"Current RSI: {current_rsi}")

        # Check for overbought/oversold conditions once and take actions
        if current_rsi > overbought:
            logging.debug(f"RSI is overbought: {current_rsi} > {overbought}")
            return execute_action(actions, 'buy', current_rsi, 'overbought', overbought)
        elif current_rsi < oversold:
            logging.debug(f"RSI is oversold: {current_rsi} < {oversold}")
            return execute_action(actions, 'sell', current_rsi, 'oversold', oversold)

        logging.debug(f"RSI does not meet buy/sell conditions.")
        return False

    except Exception as e:
        error_message = f"Error processing RSI for symbol {symbol}: {str(e)}"
        send_error_log(error_message, 'strategy_engine')
        logging.debug(f"Exception occurred: {str(e)}")
        return False


def execute_action(actions, action_name, current_rsi, condition, threshold):
    """
    Helper function to execute an action based on the RSI condition.
    """
    # logging.debug(f"actions in execute_action: {actions}")
    for action in actions:
        if action['action_name'] == action_name:
            logging.debug(f"RSI is {condition} ({current_rsi} {('>' if condition == 'overbought' else '<')} {threshold}) and '{action_name}' action found.")
            return True  # Perform the action
    return False
