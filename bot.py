from typing import Final
from discord import Intents, Client, Message
from groq import Groq
import random
from weather import get_weather
from config import TOKEN, GROQ_KEY

# LLM Setup
groq_client = Groq(api_key=GROQ_KEY)

# Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# Message Function - Custom Code
async def send_message(message: Message,user_message: str) -> None:
    # ---------------------------------------------------------------------
    # Interact with LLM
    msg_lower = user_message.lower()

    if msg_lower.startswith('/llm'):
        msg = ask_llm(msg_lower.replace('/llm', ''))
        await message.channel.send(msg[:2000])
        return
    
    city = 'Charlottesville'

    # Interact with pre-defined commands
    prompt = f'''Given a prompt, choose a command that best aligns 
    with what the user asks: 
        1. "today's weather in celsius" if user wants today's weather in celsius
        2. "today's weather" if user wants today's weather
        3. "roll a die/random" if user wants to roll a die or wants a random number
        4. "introduce" if user wants an introduction from you
        5. "hi" if user says something like hi or hello
        6. "uncertain" if no words match.
    Word/phrase that appear earlier in the list has higher priority. For instance, 
    "today's weather in celsius" is item 1 so you should choose this over "hi", which is item 5.
    Return just the chosen command without any extra words in your response.

    User asks "{user_message}".
    '''

    response = ask_llm(prompt)
    print(response)
    bot_response = ''

    if 'hi' in response:
        bot_response += 'Hello!'
        #return
    if 'introduce' in response:
        bot_response += f'My name is {client.user}.'
        #return
    if 'roll a die/random' in response:
        bot_response += f'Rolling a die... {random.randint(1, 6)}.'
        #return
    if 'today\'s weather' in response:
        if 'celsius' in response:
            bot_response += f'This is today\'s weather in {get_weather(city, temp_mode='celsius')}'
            #return
        else:
            bot_response += f'This is today\'s weather in {get_weather(city)}'
    if 'uncertain' in response:
        bot_response += 'Hmm... I\'m not sure if I understand.'
    
    await message.channel.send(bot_response)
    return


def ask_llm(prompt):
    chat_completion = groq_client.chat.completions.create(
        messages=[{
            'role': 'user',
            'content': prompt,
        }],
        model='llama3-8b-8192',
    )
    msg = chat_completion.choices[0].message.content
    return msg


# Handle the startup of the bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# Handles the messages: waits for a message to be sent, then calls "send_message()" to send a response
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: #The bot wrote the message, or the bot talks to itself
        return

    username: str= str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message)

# Main Starting point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
