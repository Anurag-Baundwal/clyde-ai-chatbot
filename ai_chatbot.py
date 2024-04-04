# Note: If not able to simulate go to developer settigns -> debugging -> amd enable security settings
# ai_chatbot.py
import base64
import os
import subprocess
import time
import json
import anthropic
from dotenv import load_dotenv
from chat_reader import read_chat, take_screenshot
from chat_responder import send_response
from pair import pair_and_connect

load_dotenv()

ADB_PATH = os.getenv("ADB_PATH")

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

BOT_NAME = "ChatGPT"  # Replace with the desired bot name

# system_prompt = """You are playing the role of ChatGPT, and talking to players in the chat of a mobile game called whiteout survival. Based on the chat history and (sometimes a screenshot) given, you should respond with only what you you would say as chatGPT in the in game chat, and nothing else, ie, don't say 'As chat GPT, I would say "xyz"'. Just give your response directly. You can write something to say to everyone, for example 'Hello world!', or mention a specific player/user and talk to them. Also, don't let your responses get too long. Only let the response be longer than 4-5 lines if you really have to. Don't be rude to anyone, and when mentioning someone don't mention their alliance tag. Instead you might use an @ character. For example, to talk to Anurag from RND alliance, don't say 'Yo [RND]Anurag'. Instead, you could try responding like so - '@Anurag Hi'. But don't randomly mention people unless they take to you or you really need to talk to them. Lastly, if you're reading the world chat and there no messages from yourself in the message history, you might start with something like 'Hello world!'

# Also don't give long weird responses like this:
# Hello world! I see the chat has been quite lively. It seems there's some playful banter going on, with players teasing each other and making jokes. I'm not familiar with the game or the players, but it looks like an entertaining conversation. I'll refrain from directly addressing any specific individuals, but feel free to keep the chat going!

# ^Most of this is just weird. Try to talk like a real person and don't send lengthy messages like this unless necessary. Also, you said 'I'll refrain from directly addressing any specific individuals' and 'I'm not familiar with the game or the players' - Don't do this. Don't talk too much about yourself or your system prompt unless asked You could start with something as simple as a hello ("Hello!"). Keep it short like a real person. Also, never use emojis in your responses; it breaks my app.

# Lastly, even though your username in the game is going to be chat gpt, you have to try talking like a real, smart, sophisticated, educated person.
# """

system_prompt = """You are playing the role of ChatGPT, and talking to players in the chat of a mobile game called whiteout survival. Based on the chat history and (sometimes a screenshot) given, you should respond with only what you would say as ChatGPT in the in-game chat, and nothing else. Just give your response directly. *KEEP YOUR RESPONSES CONCISE, around 2-3 lines maximum*, unless absolutely necessary. USUALLY YOUR RESPONSES SHOULD BE 1 or 2 LINES OR EVN SHORTER THAN THAT, AND SOMETIMES EVEN JUST 1 or 2 WORDS LIKE HELLO!. Be respectful to everyone and when mentioning a specific player, use the @ character followed by their username without including their alliance tag. For example, '@Anurag Hi' instead of 'Yo [RND]Anurag'.

If you're reading the world chat and there are no messages from yourself in the message history, start with a simple greeting like 'Hello everyone!' - this is a must. Don't mention or talk to a specific player unless they talk to you first. Engage in the conversation naturally, as a real, smart, sophisticated, and educated person would. Avoid talking about yourself or your system prompt unless directly asked - for example that you're a bot or you've never played this game yourself - don't say that unless asked.

Remember, your goal is to participate in the chat as a player, not as an AI assistant. Specifically, try to talk like an American. Never ever use emojis in your responses. Focus on providing meaningful, concise, and context-appropriate responses that contribute to the ongoing conversation.

Last but not least: YOUR GOAL IS TO TRY TO TALK LIKE A HUMAN AND BLEND IN. TRY YOUR BEST NOT TO SOUND LIKE A BOT.x"""

def generate_response(chat_history, chat_screenshot):
    print("Generating response...")
    # with open(chat_screenshot, "rb") as image_file:
    #     image_data = base64.b64encode(image_file.read()).decode("utf-8")
    # #################### not using screenshots for opus model
    message = client.messages.create(
        model="claude-3-opus-20240229", # replace with opus and remove image to reduce token usage
        max_tokens=256,
        temperature=0.7,
        system= system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        # "text": f"You are {BOT_NAME}. Based on the following chat history and the fresh screenshot, please generate a response to write in chat.",
                        "text": f"Based on the following chat, please generate a response to say something in chat.",
                    },
                    {
                        "type": "text",
                        "text": json.dumps(chat_history),
                    },
                    # {
                    #     "type": "image",
                    #     "source": {
                    #         "type": "base64",
                    #         "media_type": "image/png",
                    #         "data": image_data,
                    #     },
                    # },
                ],
            }
        ],
    )
    print("Generated response:", message.content[0].text)
    return message.content[0].text

# def restart_adb_as_root():
#     try:
#         # Restart ADB with root privileges
#         subprocess.run([ADB_PATH, "root"], check=True)
#         print("ADB restarted as root.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error restarting ADB as root: {e}")
#         print("Please make sure ADB is installed and properly set up.")

# # def grant_inject_events_permission():
#     try:
#         # Grant the INJECT_EVENTS permission using ADB
#         subprocess.run([ADB_PATH, "shell", "pm", "grant", "com.android.shell", "android.permission.INJECT_EVENTS"], check=True)
#         print("INJECT_EVENTS permission granted successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error granting INJECT_EVENTS permission: {e}")
#         print("Please grant the permission manually using the following ADB command:")
#         print("adb shell pm grant com.android.shell android.permission.INJECT_EVENTS")

def main():
    print("Welcome to ai_chatbot, created by ANURAG and powered by Claude 3 Haiku.")
    pair_and_connect()

    # print("Restarting ADB as root...")
    # restart_adb_as_root()


    chat_history = []
    while True:
        # scroll to the bottom
        x1, y1 = 208, 1190
        x2, y2 = 208, 1756
        swipe_cmd = f"{ADB_PATH} shell input swipe {x2} {y2} {x1} {y1}"
        subprocess.run(swipe_cmd, shell=True)


        print("Reading chat...")
        chat_content = read_chat()
        if chat_content is not None:
            print("Chat content:", chat_content)
            new_messages = [msg for msg in chat_content if msg not in chat_history]
            chat_history.extend(new_messages)
            print("Chat history:", chat_history)
            if new_messages:
                print("New messages found. Generating response...")
                chat_screenshot = take_screenshot()
                response_text = generate_response(chat_history, chat_screenshot)
                print("Sending response:", response_text)
                send_response(response_text)

            # Save chat history as JSON
                with open("chat_history.json", "w") as file:
                    json.dump(chat_history, file, indent=4)
        print("Waiting for 15 seconds before checking the chat again...")
        time.sleep(25)

if __name__ == "__main__":
    main()