import discord
import openai
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

openai.api_key = os.environ['OPENAI_API_KEY']
model = "gpt-3.5-turbo"
text_limit = 2000

sessions = {}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.type == discord.ChannelType.text:
        thread = await message.create_thread(name='New chat', auto_archive_duration=60)
        messages = [
            {"role": "user", "content": message.content}
        ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        answer = response['choices'][0]['message']['content']
        sessions[thread.id] = messages
        sessions[thread.id].append({"role": "assistant", "content": answer})
        for i in range(0, len(answer), text_limit):
            await thread.send(answer[i:i + text_limit])

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
        sessions[message.channel.id].append({"role": "user", "content": message.content})

        response = openai.ChatCompletion.create(
            model=model,
            messages=sessions[message.channel.id]
        )
        answer = response['choices'][0]['message']['content']
        sessions[message.channel.id].append({"role": "assistant", "content": answer})
        for i in range(0, len(answer), text_limit):
            await message.channel.send(answer[i:i + text_limit])


client.run(os.environ['DISCORD_TOKEN'])
