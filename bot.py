import discord
import openai
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = os.environ['OPENAI_API_KEY']
model = "gpt-3.5-turbo"


@client.event
async def on_message(query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query.content}
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    await query.channel.send(answer)


client.run(os.environ['DISCORD_TOKEN'])