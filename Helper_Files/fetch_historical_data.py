# import requests
# from Helper_Files.send_error_log import send_error_log
# import logging
# from datetime import datetime, timedelta
# from constants import access_token,client_id

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# exchange_segment_map = {
#     'NSE': 'NSE_EQ',
#     'BSE': 'BSE_EQ'
#     }
# def fetch_historical_data(symbol,exchange, fromDate, toDate,period):
#     logging.debug("Fetching historical data with the following inputs:")
#     logging.debug(f"Symbol: {symbol}")
#     logging.debug(f"Exchange: {exchange}")
#     logging.debug(f"From Date: {fromDate}")
#     logging.debug(f"To Date: {toDate}")
#     logging.debug(f"Period: {period}")
#     # Define a mapping for exchanges to their respective exchangeSegment
    
#     # Get the correct exchangeSegment using the mapping, defaulting to 'NSE_EQ' if not found
#     exchange_segment = exchange_segment_map.get(exchange, 'NSE_EQ')

#     # If period is provided, calculate fromDate and toDate
#     if period is not None:
#         # Set toDate as today's date
#         period = int(period)
#         toDate = datetime.today().strftime('%Y-%m-%d')
        
#         # Calculate fromDate as toDate - period days
#         fromDate = (datetime.today() - timedelta(days=period)).strftime('%Y-%m-%d')
    
#     logging.debug(f"fromDate: {fromDate}, toDate: {toDate}")

#     logging.debug(f"fetch_historical_data in exchange_segment...: {exchange_segment}")
#     url = "https://api.dhan.co/charts/historical"
#     #url = "https://api.dhan.co/v2/charts/intraday"
#     headers = {
#         "Content-Type": "application/json",
#         "access-token": access_token
#     }
#     payload = {
#         "symbol": symbol,
#         "exchangeSegment": exchange_segment,
#         "instrument": "EQUITY",
#         "expiryCode": 0,
#         "fromDate": fromDate,
#         "toDate": toDate
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     data = response.json()

#     if "error" in data:
#         print("Error:", data["error"])
#         send_error_log(data["error"],"fetch_historical_data")
#         return None
#     else:
#         print("data in the fetch_historical_data return",data)  # Print the data to understand its structure
#         return data






# import requests
# from Helper_Files.send_error_log import send_error_log
# import logging
# from datetime import datetime, timedelta
# from constants import access_token,client_id

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# exchange_segment_map = {
#     'NSE': 'NSE_EQ',
#     'BSE': 'BSE_EQ'
#     }
# def fetch_historical_data(symbol,exchange, fromDate, toDate,period):
#     logging.debug("Fetching historical data with the following inputs:")
#     logging.debug(f"Symbol: {symbol}")
#     logging.debug(f"Exchange: {exchange}")
#     logging.debug(f"From Date: {fromDate}")
#     logging.debug(f"To Date: {toDate}")
#     logging.debug(f"Period: {period}")
    
#     # Your existing logic for fetching historical data goes here

#     # Define a mapping for exchanges to their respective exchangeSegment
    
#     # Get the correct exchangeSegment using the mapping, defaulting to 'NSE_EQ' if not found
#     exchange_segment = exchange_segment_map.get(exchange, 'NSE_EQ')

#     # If period is provided, calculate fromDate and toDate
#     # if period is not None:
#         # Set toDate as today's date
#     period = int(period)
#     toDate = datetime.today().strftime('%Y-%m-%d')
        
#         # Calculate fromDate as toDate - period days
#     fromDate = (datetime.today() - timedelta(days=period)).strftime('%Y-%m-%d')
    
#     logging.debug(f"fromDate: {fromDate}, toDate: {toDate}")

#     logging.debug(f"fetch_historical_data in exchange_segment...: {exchange_segment}")
#     # url = "https://api.dhan.co/charts/historical"
#     url = "https://api.dhan.co/v2/charts/intraday"
#     headers = {
#         "Content-Type": "application/json",
#         "access-token": access_token
#     }
#     payload = {
#         "symbol": symbol,
#         "exchangeSegment": exchange_segment,
#         "instrument": "EQUITY",
#         "expiryCode": 0,
#         "fromDate": "string",
#         "toDate": "string"
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     data = response.json()
#     logging.debug("data in the fetch_historical_data return",data)  # Print the data to understand its structure
#     if "error" in data:
#         print("Error:", data["error"])
#         send_error_log(data["error"],"fetch_historical_data")
#         return None
#     else:
#         logging.debug("data in the fetch_historical_data return",data)  # Print the data to understand its structure
#         return data


import requests
from datetime import datetime, timedelta
import logging
from Helper_Files.send_error_log import send_error_log
from constants import access_token

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Map exchange names to segments
exchange_segment_map = {
    'NSE': 'NSE_EQ',
    'BSE': 'BSE_EQ'
}

# def fetch_historical_data(symbol, security_id, exchange, fromDate=None, toDate=None, period=None, interval="1",security_id):
def fetch_historical_data(symbol, exchange,security_id):
    # logging.debug("Fetching historical data with the following inputs:")
    """
    Fetch intraday historical data from the API.

    :param symbol: Symbol of the stock
    :param security_id: Security ID of the stock
    :param exchange: Exchange name (e.g., 'NSE', 'BSE')
    :param fromDate: Start date (YYYY-MM-DD format)
    :param toDate: End date (YYYY-MM-DD format)
    :param period: Number of days back for historical data (optional)
    :param interval: Time interval for intraday data (e.g., '1' for 1-minute)
    :return: JSON response from the API or None in case of an error
    """
    try:
        # Log inputs
        # logging.debug("Fetching historical data with the following inputs:")
        logging.debug(f"Symbol: {symbol}, Security ID: {security_id}, Exchange: {exchange}")
        # logging.debug(f"From Date: {fromDate}, To Date: {toDate}, Period: {period}")

        # Determine the exchange segment
        exchange_segment = exchange_segment_map.get(exchange.upper(), 'NSE_EQ')

        # Calculate fromDate and toDate if period is provided
        # if period:
        #     period = int(period)
        #     toDate = datetime.today().strftime('%Y-%m-%d')
        #     fromDate = (datetime.today() - timedelta(days=period)).strftime('%Y-%m-%d')

        # Ensure fromDate and toDate are set
        # if not fromDate or not toDate:
        #     raise ValueError("Either both fromDate and toDate or a valid period must be provided.")

        # logging.debug(f"Calculated Dates - From Date: {fromDate}, To Date: {toDate}")

        # Determine instrument type based on the symbol
        instrument = "INDEX" if "INDEX" in symbol.upper() else "EQUITY"

        # API details
        url = "https://api.dhan.co/v2/charts/intraday"
        headers = {
            "Content-Type": "application/json",
            "access-token": access_token
        }
        payload = {
            "securityId": security_id,
            "exchangeSegment": exchange_segment,
            "instrument": instrument,
        }

        # Log the payload
        logging.debug(f"Payload: {payload}")

        # Make the API request
        response = requests.post(url, json=payload, headers=headers)

        # Log the response
        # logging.debug(f"HTTP Status Code: {response.status_code}")
        # logging.debug(f"Response Text: {response.text}")

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Parse and return the JSON response
        data = response.json()
        # logging.debug("API Response Data: %s", data)
        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP Request failed: {e}")
        send_error_log(str(e), "fetch_historical_data")
        return None
    except ValueError as ve:
        logging.error(f"Value Error: {ve}")
        send_error_log(str(ve), "fetch_historical_data")
        return None
    except Exception as e:
        logging.error(f"Error in fetch_historical_data: {e}")
        send_error_log(str(e), "fetch_historical_data")
        return None
