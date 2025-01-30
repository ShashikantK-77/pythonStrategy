import requests

# def get_latest_ltp(security_id):
#     print("security_id in get_latest_ltp-------------------------------------------------------", security_id)

#     # Construct the URL with the security_id parameter
#     url = f"http://localhost:5000/python/getltp/{security_id}"

#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         matched_row = data.get("matchedRow")
#         if matched_row and matched_row.get("Type") == "Ticker Data":
#             ltp = matched_row.get("LTP")
#             if ltp:
#                 return float(ltp)
#     print("Error: Unable to fetch latest LTP")


import requests

def get_latest_ltp(security_id):
    """
    Fetch the latest LTP for a given security ID using the updated file structure.
    
    Parameters:
        security_id (int): The ID of the security for which the LTP is required.
    
    Returns:
        float: The latest LTP if found, or None otherwise.
    """
    print("security_id in get_latest_ltp-------------------------------------------------------", security_id)

    # Construct the URL with the security_id parameter
    url = f"http://localhost:5000/python/getltp/{security_id}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            matched_row = data.get("matchedRow")
            
            # Ensure the matched_row contains the updated structure
            if matched_row:
                exchange_segment = matched_row.get("Exchange Segment")
                ltp = matched_row.get("LTP")
                ltt = matched_row.get("LTT")  # Optional: Log or use as needed

                print(f"Matched Row Details: Exchange Segment={exchange_segment}, LTP={ltp}, LTT={ltt}")

                if ltp:
                    return float(ltp)
        
        print("Error: No matching data found for the given security_id.")
    except Exception as e:
        print(f"Error fetching LTP: {e}")

    return None
