# Discordbot
This AI-powered Discord bot provides a variety of entertaining and useful features to enhance your Discord server experience. Built using Python, discord.py library, and the OpenAI API, this bot offers a lighthearted roast command, a conversation summarizing command, and more.

Features
Roast: Generates a funny roast based on a user's message history.
Summarize: Condenses conversations within a specified timeframe, making it easy to catch up on missed discussions.
More features can be added in the future.
Getting Started
Follow these instructions to set up the AI-Powered Discord bot on your own server.

Prerequisites
Python 3.6 or higher
discord.py library
OpenAI API key
A Discord server to host the bot
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/AmirMEdris/Discordbot.git
Install the required dependencies:

Copy code
pip install -r requirements.txt
Obtain an OpenAI API key by signing up for an account at https://beta.openai.com/signup/.

Create a new bot on the Discord Developer Portal and get the bot token.

Create a config.yaml file in the project directory and add your OpenAI API key and Discord bot token:

yaml
Copy code
openai_key: YOUR_OPENAI_API_KEY
bot_token: YOUR_DISCORD_BOT_TOKEN
Invite the bot to your Discord server using the link provided in the Discord Developer Portal.

Run main.py:

css
Copy code
python main.py
Your AI-Powered Discord bot is now ready to use on your server!

Usage
Use the !!roast @username command to generate a roast for a specific user.
Use the !!summarize [timeframe] command to summarize conversations within a specified timeframe.
Contributing
This project is open source and contributions are welcome. Feel free to fork the repository, create new features or improve existing ones, and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for more information.
