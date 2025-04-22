import discord
import os


TOKEN = os.getenv("DISCORD_TOKEN")


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

# Iniciar el bot
client.run(TOKEN)
