# #chat_responder.py
# import os
# import subprocess
# import time
# import random
# from dotenv import load_dotenv

# load_dotenv()

# ADB_PATH = os.getenv("ADB_PATH")

# buttons = {
#     "text_box": (490, 2570),
#     "send": (1093, 1750),
# }

# def click_button(button_name):
#     if button_name in buttons:
#         x, y = buttons[button_name]
#         subprocess.Popen([ADB_PATH, "shell", "input", "tap", str(x), str(y)])
#         time.sleep(random.uniform(0.75, 1.5))  # Random wait between 0.75-1.5 seconds
#     else:
#         print(f"Error: Button '{button_name}' not found.")

# def send_response(response_text):
#     print("Sending response...")
#     # Click the text box
#     click_button("text_box")

#     # Escape or remove special characters and formatting from the response text
#     response_text = response_text.replace("\\", "\\\\")  # Escape backslashes
#     response_text = response_text.replace("'", "\\'")  # Escape single quotes
#     response_text = response_text.replace('"', '\\"')  # Escape double quotes
#     response_text = response_text.replace('\n', ' ')  # Replace newline characters with spaces

#     # Split the response into chunks of maximum 100 characters
#     chunk_size = 100
#     chunks = [response_text[i:i+chunk_size] for i in range(0, len(response_text), chunk_size)]

#     # Input each chunk of the response text
#     for i, chunk in enumerate(chunks):
#         print(f"Inputting response chunk {i+1}/{len(chunks)}...")
#         subprocess.run([ADB_PATH, "shell", "input", "text", chunk], check=True)
#         time.sleep(1)  # Wait for 1 second between chunks

#     # Click the send button
#     click_button("send")
#     print("Response sent in chat.")


################################


import os
import subprocess
import time
import random
from dotenv import load_dotenv

load_dotenv()

ADB_PATH = os.getenv("ADB_PATH")
permission_to_send = False # default value. ask me before sending
buttons = {
    "text_box": (490, 2570),
    "send": (1093, 2604),
    "outside": (111, 568)
}

def click_button(button_name):
    if button_name in buttons:
        x, y = buttons[button_name]
        subprocess.Popen([ADB_PATH, "shell", "input", "tap", str(x), str(y)])
        time.sleep(random.uniform(0.75, 1.5))  # Random wait between 0.75-1.5 seconds
    else:
        print(f"Error: Button '{button_name}' not found.")

def send_response(response_text):
    print("Sending response...")

    # Click the text box
    click_button("text_box")

    # # Escape or remove special characters and formatting from the response text
    response_text = response_text.replace("|", "\\|")
    response_text = response_text.replace("\"", "\\\"")
    response_text = response_text.replace("\'", "\\\'")
    response_text = response_text.replace("<", "\\<")
    response_text = response_text.replace(">", "\\>")
    response_text = response_text.replace(";", "\\;")
    response_text = response_text.replace("?", "\\?")
    response_text = response_text.replace("`", "\\`")
    response_text = response_text.replace("&", "\\&")
    response_text = response_text.replace("*", "\\*")
    response_text = response_text.replace("(", "\\(")
    response_text = response_text.replace(")", "\\)")
    response_text = response_text.replace("~", "\\~")
    response_text = response_text.replace(" ", "\\ ")
    response_text = response_text.replace(".", "\\ ")
    response_text = response_text.replace("\n", "\\ ")
    # Input the entire response text at once
    subprocess.run([ADB_PATH, "shell", "input", "text", response_text], check=True)
    time.sleep(1)  # Wait for 1 second after inputting the response

    # permission_to_send = ''

    # while permission_to_send.lower() not in ['y', 'n']:
    #     permission_to_send = input("Send response (y/n)? ")
        
    #     if permission_to_send.lower() == 'y':
    #         permission_to_send = 'y'
    #     elif permission_to_send.lower() == 'n':
    #         permission_to_send = 'n'
    #     else:
    #         print("Invalid input. Please enter 'y' or 'n'.")

    # if permission_to_send == 'y':
    #     # Click the send button
    #     click_button("outside")
    #     time.sleep(1)
    #     click_button("send")
    #     print("Response sent in chat.")

    # Click the send button
    click_button("outside")
    time.sleep(1)
    click_button("send")
    print("Response sent in chat.")
    # else: return