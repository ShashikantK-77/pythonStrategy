import requests
import logging
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_active_brokers():
    url = "http://localhost:5000/broker/active-brokers"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        brokers = response.json()
        # logging.debug(f"Retrieved active brokers: {brokers}")
        return brokers
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching active brokers: {e}")
        return []


