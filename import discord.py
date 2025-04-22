import discord
import os


TOKEN = os.getenv("MTI3ODg0NjYzNjYxNzEwOTYzNw.Gc8wUQ.P0mYNwZXQUwiX4MO4gQCOeFinUbVQ1VMal2hjg")


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "!ping":
        await message.channel.send("🏓 Pong!")

client.run(TOKEN)
