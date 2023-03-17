import discord
import openai
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = os.environ['OPENAI_API_KEY']
model = "gpt-3.5-turbo"


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type == discord.ChannelType.text:
        thread = await message.create_thread(name='New chat', auto_archive_duration=60)
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": message.content}
            ]
        )
        answer = response['choices'][0]['message']['content']
        await thread.send(answer)

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": f"'{message.content}'를 최대 세 단어로 요약"}
            ]
        )
        answer = response['choices'][0]['message']['content']
        await thread.edit(
            name=answer
        )
    elif message.channel.type == discord.ChannelType.public_thread:
        messages = [
            {"role": "user", "content": message.content}
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        answer = response['choices'][0]['message']['content']
        await message.channel.send(answer)


client.run(os.environ['DISCORD_TOKEN'])
