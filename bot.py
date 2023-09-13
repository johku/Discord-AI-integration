import discord
from discord.ext import commands
import os
import openai
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Load enviroment variables from .env
load_dotenv()
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def ChatGPT(message):
    openai.api_key = OPENAI_API_KEY

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ],
    max_tokens=500
    )

    return completion.choices[0].message.content


def Dall_E(description):
    response = openai.Image.create(
    prompt=description,
    n=1,
    size="512x512"
)
    
    image_url = response['data'][0]['url']
    
    return image_url

@bot.event
async def on_ready():
    print('Logged on as', bot.user)

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return

    # Check if the message starts with "!prompt"
    if message.content.startswith('!prompt'):
        # Extract the prompt after "!prompt" (excluding the command itself)
        prompt = message.content[len('!prompt'):].strip()
        
        # Generate a response using ChatGPT
        response = ChatGPT(prompt)

        # Limit the lenght of response to 2000 characters as required by Discord
        if len(response) > 2000:
            response = response[:2000]
        
        # Send the response back to the Discord channel
        await message.channel.send(response)

    # Check if the message starts with "!image"
    if message.content.startswith("!image"):
        description = message.content[len('!image'):].strip()

        url = Dall_E(description)

        await message.channel.send(url)

bot.run(DISCORD_API_TOKEN)




    
        
