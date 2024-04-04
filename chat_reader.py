# #chat_reader.py
# import os
# import subprocess
# import anthropic
# import base64
# import json
# from dotenv import load_dotenv

# load_dotenv()

# ADB_PATH = os.getenv("ADB_PATH")

# client = anthropic.Anthropic(
#     api_key=os.getenv("ANTHROPIC_API_KEY")
# )

# def take_screenshot():
#     """Take screenshot on phone and pull to laptop"""
#     print("Taking screenshot...")

#     screenshot_cmd = f"{ADB_PATH} shell screencap -p /sdcard/screenshot.png"
#     pull_cmd = f"{ADB_PATH} pull /sdcard/screenshot.png ./screenshot.png"
#     try:
#         subprocess.run(screenshot_cmd, shell=True, check=True)
#         subprocess.run(pull_cmd, shell=True, check=True)
#         return "./screenshot.png"
#     except subprocess.CalledProcessError as e:
#         print(f"Error: {e}")
#         return None

# def read_chat():
#     print("Reading chat from screenshot...")
#     screenshot_path = take_screenshot()
#     if screenshot_path is None:
#         print("Could not read chat. No screenshot found.")
#         return None

#     with open(screenshot_path, "rb") as image_file:
#         image_data = base64.b64encode(image_file.read()).decode("utf-8")

#     message = client.messages.create(
#         model="claude-3-haiku-20240307",
#         max_tokens=1000,
#         temperature=0.25,
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image",
#                         "source": {
#                             "type": "base64",
#                             "media_type": "image/png",
#                             "data": image_data,
#                         },
#                     },
#                     {
#                         "type": "text",
#                         "text": "Please provide a neat JSON-formatted transcription of the chat in the given screenshot. The response should be a JSON object with a 'chat' key containing an array of 'message' objects. Each 'message' object should have 'author' and 'content' keys. Avoid including any unnecessary information in the response. Here's an example of the desired format:\n```json\n{\n  \"chat\": [\n    {\n      \"author\": \"User1\",\n      \"content\": \"Hello, how are you?\"\n    },\n    {\n      \"author\": \"User2\",\n      \"content\": \"I'm doing well, thanks!\"\n    }\n  ]\n}\n```",
#                     },
#                 ],
#             }
#         ],
#     )

#     response_content = message.content[0].text
#     chat_data = json.loads(response_content)
#     print("Received chat data:", chat_data)
#     return chat_data["chat"]



############################################


import os
import subprocess
import anthropic
import base64
from dotenv import load_dotenv

load_dotenv()

ADB_PATH = os.getenv("ADB_PATH")

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def take_screenshot():
    """Take screenshot on phone and pull to laptop"""
    print("Taking screenshot...")
    screenshot_cmd = f"{ADB_PATH} shell screencap -p /sdcard/screenshot.png"
    pull_cmd = f"{ADB_PATH} pull /sdcard/screenshot.png ./screenshot.png"
    try:
        subprocess.run(screenshot_cmd, shell=True, check=True)
        subprocess.run(pull_cmd, shell=True, check=True)
        return "./screenshot.png"
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def read_chat():
    print("Reading chat from screenshot...")
    screenshot_path = take_screenshot()
    if screenshot_path is None:
        print("Could not read chat. No screenshot found.")
        return None
    
    with open(screenshot_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4096,
            temperature=0.25,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": "Please provide a transcription of the chat in the given screenshot. The response should be a list of 'author:message' pairs, one per line. If you can't see the author's name and the message is on the right side of the screen you can assume that the author is Chat GPT. Avoid including any unnecessary information in the response.",
                        },
                    ],
                }
            ],
        )

        response_content = message.content[0].text
        chat_data = [line.split(":", 1) for line in response_content.strip().split("\n")]
        print("Received chat data:", chat_data)
        return chat_data