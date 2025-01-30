

# # Download the CSV file
# # download_csv.download_csv()

# # Example usage
# symbols = ["NIFTY", "BANKNIFTY"]   #
# result = search_security_ids.search_security_ids(symbols)
# print(result)
# #result = [('0', '1022653'), ('0', '1022656')]

# live_websocket(result)
import threading
import search_security_ids
from live_websocket import live_websocket
# import download_csv

print("in main started")
# Create an event to wait for the CSV file to be downloaded
# csv_downloaded_event = threading.Event()

# def download_csv_thread():
#     print("Downloading CSV file...")
#     download_csv.download_csv()
#     # Set the event to notify that the CSV file has been downloaded
#     csv_downloaded_event.set()
#     print("CSV file download completed.")

# # Download the CSV file in a separate thread
# download_thread = threading.Thread(target=download_csv_thread)
# download_thread.start()

print("Waiting for the CSV file to be downloaded...")

# Wait for the download thread to complete
# download_thread.join()

# Example usage
symbols = ["TCS"]
result = search_security_ids.search_security_ids(symbols)
print("Security IDs:", result)

live_websocket(result)
