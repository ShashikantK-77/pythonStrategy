# import requests

# def send_error_log(error_message, fileName):

#     """ Send error log to Node.js server """
#     url = 'http://localhost:5000/python/saveError'
#     data = {
#         'error': error_message,
#         'fileName': fileName
#     }
#     try:
#         response = requests.post(url, json=data)
#         response.raise_for_status()
#         print("Error logged successfully to server:", error_message)
#     except Exception as e:
#         print("Error logging to server:", str(e))



import requests
from constants import BASE_URL

def send_error_log(error_message, file_name):
    """ Send error log to Node.js server """
    # url = 'http://localhost:5000/python/saveError'
    url = f"{BASE_URL}python/saveError"  # Use the global base URL
    data = {
        'error_message': error_message,  # updated to match server expectations
        'file_name': file_name  # updated to match server expectations
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Error logged successfully to server:", error_message)
    except Exception as e:
        print("Error logging to server:", str(e))
