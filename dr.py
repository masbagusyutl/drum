import requests
import time
import json
from datetime import datetime, timedelta

def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip().splitlines()

def post_request(auth_data, dev_auth_data):
    url = "https://drumapi.wigwam.app/api/claimTaps"
    payload = {
        "devAuthData": int(dev_auth_data),
        "authData": auth_data,
        "data": {
            "taps": 97,
            "amount": 97
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
    dev_auth_data_list = read_file('idtele.txt')
    
    num_accounts = len(auth_data_list)
    print(f"Total accounts: {num_accounts}")
    
    for i, (auth_data, dev_auth_data) in enumerate(zip(auth_data_list, dev_auth_data_list)):
        print(f"Processing account {i + 1} of {num_accounts}")
        success = post_request(auth_data, dev_auth_data)
        if success:
            print(f"Account {i + 1} processed successfully.")
        else:
            print(f"Failed to process account {i + 1}.")
        time.sleep(5)
    
    print("All accounts processed. Starting 1-hour countdown.")
    countdown_timer(3600)
    print("Restarting the process.")
    main()

if __name__ == "__main__":
    main()
