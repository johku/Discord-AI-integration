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


def wrap_text_in_file(file_path, line_length=200):
    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    wrapped_lines = []

    for line in lines:
        line = line.rstrip('\n')
        while len(line) > line_length:
            # Find the position to split the line
            split_pos = line.rfind(' ', 0, line_length)
            if split_pos == -1:
                split_pos = line_length
            wrapped_lines.append(line[:split_pos])
            line = line[split_pos:].lstrip()
        wrapped_lines.append(line)

    with open(file_path, 'w') as outfile:
        for line in wrapped_lines:
            outfile.write(line + '\n')


def ChatGPT(message):
    openai.api_key = OPENAI_API_KEY

    completion = openai.chat.completions.create(
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
            # Write response to a text file
            response_file_path = "response.txt"
            with open(response_file_path, "w") as file:
                file.write(response)

            wrap_text_in_file(response_file_path)

            # Send the response as a text file attachment to the Discord channel
            await message.channel.send(file=discord.File(response_file_path))

            # Delete the local text file
            os.remove(response_file_path)
        else:
            # Send the response back to the Discord channel
            await message.channel.send(response)

    # Check if the message starts with "!image"
    if message.content.startswith("!image"):
        description = message.content[len('!image'):].strip()

        url = Dall_E(description)

        await message.channel.send(url)

bot.run(DISCORD_API_TOKEN)




    
        
