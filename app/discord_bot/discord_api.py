from dotenv import load_dotenv
import discord
import os

from app.chatgpt_ai.openai import chatgpt_response

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")

channels = {'gpt-questions', 'chatgpt', 'gpt-bot'}


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        channel_name = message.channel.name
        valid_channel = False

        for channel in channels:
            if channel_name == channel:
                valid_channel = True
                break

        if message.author == self.user:
            return
        command, user_message = None, None
        for text in ['/ai', '/bot', '/chatgpt']:
            if message.content.startswith(text):
                command = message.content.split(' ')[0]
                user_message = message.content.replace(text, '')
                print(command, user_message)
                break

        if command == '/ai' or command == '/bot' or command == '/chatgpt':
            if valid_channel:
                bot_response = chatgpt_response(prompt=user_message)
                await message.channel.send(f'Answer: {bot_response}')
            else:
                return


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
