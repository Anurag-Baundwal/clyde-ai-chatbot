# AI Chatbot for Mobile Game

Clyde is a fully working, autonomous AI chatbot designed to engage with players in a mobile game chat. The chatbot periodically reads the chat messages, generates relevant responses using the Anthropic Claude AI model (Claude 3 Haiku), and sends the responses back to the game chat by simulating input using adb platform tools.

## Features

- Automatically reads chat messages from the mobile game using screenshots and OCR.
- Maintains a history of chat messages to provide context for generating responses.
- Uses the Anthropic Claude AI model to generate engaging and relevant responses.
- Simulates button clicks on the mobile device to send the generated responses.
- Configurable bot name and response generation parameters.

## Requirements

- Python 3.x
- Android Debug Bridge (ADB) installed and configured
- Anthropic API key

## Installation

1. Clone the repository: `git clone https://github.com/your-username/ai-chatbot.git`
2. Download Android Debug Bridge (ADB) platform tools from [https://developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools) and extract the zip file.
3. Create a virtual environment (optional but recommended): `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install the required Python packages: `pip install -r requirements.txt`
6. Set up the Anthropic API key and the path to the ADB executable in the `.env` file:
7. On the phone, make sure to enable "USB Debugging (Security Settings)" in order to grant permission to send input using adb

## Todo:

Update the ai to let Claude 3 Haiku decide what to do - whether to scroll up and capture more screenshots for more context, say something, or simply remain silent - rather than waiting a fixed amount of time before chatting again.
