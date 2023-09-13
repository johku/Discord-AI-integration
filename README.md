# Discord-AI-integration
Discord bot that brings ChatGPT and Dall-E to a server


# Setup
## Create bot with no functionality
1. Go to https://discord.com/developers/applications
2. Click new application
3. Configure the bot settings as shown below:

   ![Bot settings](/images/bot_settings.PNG)
   
4. Create a bot invite link with the following permissions:

   ![Bot permissions](/images/bot_permissions.PNG)
   
5. Get the bot token by clicking "Reset Token" as shown below:

   ![Bot get token](/images/bot_get_token.PNG)

## Add functionality
1. Download the contents of this repository
2. Generate OpenAI API key in here: https://platform.openai.com/account/api-keys
3. Navigate to the downloaded repository and fill in Discord token and OpenAI API key to the .env file
4. Open cmd/terminal and navigate to the downloaded repository
5. In cmd/terminal type the following commands:

    1. `pip install virtualenv`
    2. `python -m venv venv`
    3. `venv\Scripts\activate` (or `source venv/bin/activate` if on Linux)
    4. `pip install --upgrade pip`
    5. `pip install discord`
    6. `pip install openai`
    7. `pip install python-dotenv`
    8. `python bot.py`
  
Your bot should now be running for as long as you have the cmd/terminal open
