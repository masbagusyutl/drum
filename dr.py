import requests
import time
import json
import re
from datetime import datetime, timedelta

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip().splitlines()

def extract_dev_auth_data(auth_data):
    match = re.search(r'user=%7B%22id%22%3A(\d+)%2C', auth_data)
    if match:
        return match.group(1)
    return None

def post_request(auth_data, dev_auth_data):
    url = "https://drumapi.wigwam.app/api/claimTaps"
    payload = {
        "devAuthData": int(dev_auth_data),
        "authData": auth_data,
        "data": {
            "taps": 8,
            "amount": 8
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.status_code == 200

def countdown_timer(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"\rCountdown: {remaining_time}", end="")
        time.sleep(1)
    print()

def main():
    auth_data_list = read_file('data.txt')
    
    num_accounts = len(auth_data_list)
    print(f"Total accounts: {num_accounts}")
    
    for i, auth_data in enumerate(auth_data_list):
        dev_auth_data = extract_dev_auth_data(auth_data)
        if not dev_auth_data:
            print(f"Failed to extract devAuthData for account {i + 1}. Skipping this account.")
            continue
        
        print(f"Processing account {i + 1} of {num_accounts}")
        process_count = 0
        while True:
            process_count += 1
            success = post_request(auth_data, dev_auth_data)
            if success:
                print(f"Process {process_count} for account {i + 1} processed successfully.")
            else:
                print(f"Failed to process {process_count} for account {i + 1}. Switching to next account.")
                break
            time.sleep(2)
        time.sleep(5)
    
    print("All accounts processed. Starting 3-hour countdown.")
    countdown_timer(3 * 3600)
    print("Restarting the process.")
    main()

if __name__ == "__main__":
    main()
