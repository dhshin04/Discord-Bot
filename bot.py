from typing import Final
from discord import Intents, Client, Message
import random
from weather import get_weather
from config import TOKEN


#Step 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#Step 2: Message Function
async def send_message(message: Message,user_message: str) -> None:
    # ---------------------------------------------------------------------
    # WRITE NEW RESPONSES HERE !!
    msg_lower = user_message.lower()
    city = 'Charlottesville'

    if 'hi' in msg_lower:
        await message.channel.send('Hello!')
        return
    if 'introduce' in msg_lower:
        await message.channel.send(f'My name is {client.user}.')
        return
    if ('roll' in msg_lower and 'die' in msg_lower) or 'random' in msg_lower:
        await message.channel.send(f'Rolling a die... {random.randint(1, 6)}.')
        return
    if 'weather' in msg_lower and ('today' in msg_lower or 'current' in msg_lower or 'now' in msg_lower):
        await message.channel.send(get_weather(city))
        return


def startWith(msg: str, prompt: str) -> bool:
    return msg.lower().startswith(prompt)

    # ---------------------------------------------------------------------

#Step 3: Handle the startup of the bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

#Step 4:  Handles the messages: waits for a message to be sent, then calls "send_message()" to send a response
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: #The bot wrote the message, or the bot talks to itself
        return

    username: str= str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

#Step 5 Main Starting point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()