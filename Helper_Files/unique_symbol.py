

import csv
from Helper_Files.fetch_data import fetch_data
import logging
from constants import BASE_URL  # Import the global base URL
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def get_unique_symbols():
    # logging.debug(f"in get_unique_symbols")
    # api_url = 'http://localhost:5000/python/get_unique_symbols'
    api_url = f"{BASE_URL}python/get_unique_symbols"  # Use the global base URL
    api_data = fetch_data(api_url)
    
    if not api_data or not api_data.get("is_success"):
        return []
    
    strategy_data = api_data.get("details", [])
    
    symbols_info = {}  # Dictionary to store symbols along with their exchange and categories
    
    for row in strategy_data:
        symbol = row['symbol']
        exchange = row['exchange']
        category = row['categories']
        
        # If symbol already exists, update the category
        if symbol in symbols_info:
            symbols_info[symbol]['categories'].update(category)
        else:
            # If symbol doesn't exist, create a new entry
            symbols_info[symbol] = {'exchange': exchange, 'categories': set(category)}
    
    # Convert the dictionary to a list of dictionaries
    unique_symbols_list = []
    for symbol, info in symbols_info.items():
        unique_symbols_list.append({
            'symbol': symbol,
            'exchange': info['exchange'],  # Only include the single exchange
            'categories': list(info['categories'])
        })
    
    return unique_symbols_list



def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)