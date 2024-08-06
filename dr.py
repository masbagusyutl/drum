import requests
import time
import json
import re
import random
from datetime import datetime, timedelta

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip().splitlines()

def extract_dev_auth_data(auth_data):
    match = re.search(r'user=%7B%22id%22%3A(\d+)%2C', auth_data)
    if match:
        return match.group(1)
    return None

def parse_user_info(response_content):
    # Parsing balance
    balance_start = response_content.find('"balance":') + len('"balance":')
    balance_end = response_content.find(',', balance_start)
    balance = response_content[balance_start:balance_end].strip().strip('"')
    balance = int(float(balance))  # Convert to float first, then to int
    
    # Parsing username
    username_start = response_content.find('"username":"') + len('"username":"')
    username_end = response_content.find('"', username_start)
    username = response_content[username_start:username_end]
    
    # Parsing availableTaps
    available_taps_start = response_content.find('"availableTaps":') + len('"availableTaps":')
    available_taps_end = response_content.find(',', available_taps_start)
    available_taps = int(response_content[available_taps_start:available_taps_end].strip())
    
    return balance, username, available_taps

def get_user_info(auth_data, dev_auth_data):
    url = "https://drumapi.wigwam.app/api/getUserInfo"
    payload = {
        "authData": auth_data,
        "devAuthData": int(dev_auth_data),
        "platform": "tdesktop"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        return parse_user_info(response.content.decode('utf-8'))
    else:
        print(f"Failed to get user info. Status code: {response.status_code}")
        return None, None, None

def post_taps_request(auth_data, dev_auth_data, taps):
    payload = {
        "devAuthData": int(dev_auth_data),
        "authData": auth_data,
        "data": {
            "taps": taps,
            "amount": taps
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    url = "https://drumapi.wigwam.app/api/claimTaps"
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
        
        # Get user info
        balance, username, available_taps = get_user_info(auth_data, dev_auth_data)
        if balance is not None:
            print(f"Account {i + 1} info: Balance={balance}, Username={username}, Available Taps={available_taps}")
            
            # Process taps
            if available_taps > 0:
                remaining_taps = available_taps
                while remaining_taps > 0:
                    # Determine a random number of taps between 1 and 10, ensuring we don't exceed remaining_taps
                    taps = random.randint(1, min(10, remaining_taps))
                    success = post_taps_request(auth_data, dev_auth_data, taps)
                    if success:
                        print(f"Taps processed successfully for account {i + 1}: Taps={taps}")
                        remaining_taps -= taps
                    else:
                        print(f"Failed to process taps for account {i + 1}.")
                    time.sleep(2)
            else:
                print(f"No available taps for account {i + 1}.")
        else:
            print(f"Failed to retrieve user info for account {i + 1}.")
        
        time.sleep(5)
    
    print("All accounts processed. Starting 3-hour countdown.")
    countdown_timer(3 * 3600)
    print("Restarting the process.")
    main()

if __name__ == "__main__":
    main()
