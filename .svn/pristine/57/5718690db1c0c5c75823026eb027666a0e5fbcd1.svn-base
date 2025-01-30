import requests
import os
import time
import schedule

def download_csv():
    print("Downloading CSV file...")
    # URL of the CSV file
    url = "https://images.dhan.co/api-data/api-scrip-master.csv"
    
    # Path to save the CSV file
    save_path = "./"
    
    # Name of the CSV file
    file_name = "dhan_securities.csv"
    
    # Complete path to save the file
    file_path = os.path.join(save_path, file_name)
    
    # Send request to download the file
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the CSV file
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("CSV file downloaded successfully.")
    else:
        print("Failed to download CSV file.")

# Download the CSV file immediately
# download_csv()

# Schedule the job to run every day at 9:00 AM
schedule.every().day.at("09:00").do(download_csv)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
