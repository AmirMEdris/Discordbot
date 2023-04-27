# Discordbot
After seeing tons of diffent applications using gpt 4 I thought that a discord bot that uses ai for its commands would be fun. Built using Python, discord.py library, and the OpenAI API. I talk about it more [here](https://medium.com/@amiredris25/making-a-discord-bot-that-uses-gpt-and-dalle-2-a0c6c4b80ce)

### Features
Help: Shows all available functions and provides a description.
Roast: Generates a funny roast based on a user's message history.
Summarize: Condenses conversations within a specified timeframe, making it easy to catch up on missed discussions.
More features can be added in the future.
Visualize: Takes in prompt from user and uses dalle-2 to make an image and send it to chat.
Nickname: Looks through a users messages and makes a new name based off their chat and sends it.


### Getting Started
Follow these instructions to set up the AI-Powered Discord bot on your own server.

### Prerequisites
Python 3.9 or higher
discord.py library
OpenAI API key
A Discord server to host the bot
Installation
Clone the repository:
```
git clone https://github.com/AmirMEdris/Discordbot.git
```

Install the required dependencies:
```
pip install -r requirements.txt
```

Obtain an OpenAI API key by signing up for an account at https://beta.openai.com/signup/.

Create a new bot on the Discord Developer Portal and get the bot token.

Create a config.yaml file in the project directory and add your OpenAI API key and Discord bot token:
```
openai_key: YOUR_OPENAI_API_KEY
bot_token: YOUR_DISCORD_BOT_TOKEN
```

Invite the bot to your Discord server using the link provided in the Discord Developer Portal.

Run bot.py:
```
python bot.py
```

Your AI-Powered Discord bot is now ready to use on your server!

### Usage
Once active use !!help in a chat with the bot in it and it will show you all the commands and their usage.
### To-Do:
 - Use /commands instead of !!
 - Replace visualize with a free alternative. 
 - Make Summary do a better job when its long intervals of time
 - Add arguements like channel name for applicable functions
 - Come up with more useful methods.
 - Give messages explaining what went wrong when outputs wont be generated cause of openai content filtering.
 - make readme better

## Contributing
This project is open source and contributions are welcome. Feel free to fork the repository, create new features or improve existing ones, and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
