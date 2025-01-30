import csv
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def read_security_ids(file_path):
    security_ids_map = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbol = row['Symbol']
            exchange_id = int(row['Exchange ID'])
            security_id = int(row['Security ID'])
            security_ids_map[symbol] = (exchange_id, security_id)
            logging.debug(f"returning Symbols in read_security_ids: {security_ids_map}")
    return security_ids_map
