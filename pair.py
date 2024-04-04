# pair.py
# File to pair phone via wireless debugging

# Function to pair and connect to the device
import os
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()

ADB_PATH = os.getenv("ADB_PATH")

def pair_and_connect():

    #for pairing
    ip = input("Please enter phone ip: ")
    print(f"Pairing with device: {ip}")
    
    # Check if already connected
    result = subprocess.run([ADB_PATH, "devices"], stdout=subprocess.PIPE, text=True)
    already_connected = ip in result.stdout

    if not already_connected:
        port = input("Please enter port for pairing: ")
        code = input("Please enter the pairing code: ")

        # Pair to the device
        subprocess.run([ADB_PATH, "pair", f"{ip}:{port}"], input=code, text=True)

        connection_port = input("Please enter the connection port: ")

        # Connect to the device
        subprocess.run([ADB_PATH, "connect", f"{ip}:{connection_port}"])

    else:
        print(f"Already connected to {ip}.")

    print("Waiting for 10 seconds after pairing and connecting. Take this time to open up the chat.")
    time.sleep(3)