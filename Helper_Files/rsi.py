# import pandas as pd
# import logging
# from Helper_Files.send_error_log import send_error_log
# # Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# def calculate_rsi(data, period=14):
#     """
#     Calculate the Relative Strength Index (RSI) for a given dataset.
    
#     Parameters:
#     - data: A dictionary containing lists of price data (open, high, low, close, volume, start_Time).
#     - period: The period over which to calculate the RSI (default is 14).
    
#     Returns:
#     - A pandas Series containing the RSI values.
#     """

#     logging.debug(f"------------in rsi functionnn---------------")
#     # Create a pandas DataFrame from the provided dictionary
#     df = pd.DataFrame(data)
    
#     # Extract the 'close' prices into a pandas Series
#     close_prices = df['close']
#     logging.debug(f"close_prices:",close_prices)

#     # Calculate price changes
#     delta = close_prices.diff()
    
#     # Separate gains and losses
#     gains = delta.where(delta > 0, 0)
#     losses = -delta.where(delta < 0, 0)
    
#     # Calculate the average gains and losses
#     avg_gain = gains.rolling(window=period, min_periods=1).mean()
#     avg_loss = losses.rolling(window=period, min_periods=1).mean()
    
#     # Calculate the Relative Strength (RS)
#     rs = avg_gain / avg_loss
    
#     # Calculate the RSI
#     rsi = 100 - (100 / (1 + rs))
#     print("---------------- rsi returning by function:",rsi)
#     send_error_log("rsi returning by function:",rsi)
#     return rsi


import pandas as pd
import logging
from Helper_Files.send_error_log import send_error_log

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_rsi(data, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given dataset.
    """
    logging.debug("------------in rsi function---------------")
    # logging.debug(f"data: {data}")
    # Check if data is None
    if data is None:
        logging.error("Input data is None.")
        return None

    # Convert input data to DataFrame if it's a dictionary
    if isinstance(data, dict):
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        logging.error("Input data must be a dictionary or a pandas DataFrame.")
        return None

    # Check if 'close' column exists
    if 'close' not in df.columns:
        logging.error("Data does not contain 'close' column.")
        return None

    close_prices = df['close']
    # logging.debug(f"close_prices: {close_prices}")

    # Calculate price changes
    delta = close_prices.diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate the average gains and losses
    avg_gain = gains.rolling(window=period, min_periods=1).mean()
    avg_loss = losses.rolling(window=period, min_periods=1).mean()

    # logging.debug(f"avg_gain: {avg_gain}, avg_loss: {avg_loss}")
    
    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # Replace NaN values resulting from division by zero
    rsi = rsi.fillna(50)  # Set RSI to 50 if there's no variation

    # logging.debug(f"RSI calculated: {rsi}")
    send_error_log("RSI calculated:", rsi)
    return rsi