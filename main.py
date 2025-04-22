import discord
import os
import random

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necesario para elegir un usuario al azar

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')

def crear_embed(titulo, descripcion, color=discord.Color.blurple()):
    embed = discord.Embed(title=titulo, description=descripcion, color=color)
    embed.set_footer(text="Bot divertido 😎 | Usa !comandos para ver más")
    return embed

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if content == "!ping":
        embed = crear_embed("🏓 Pong!", "¡Estoy vivo!")
        await message.channel.send(embed=embed)

    elif content == "!dado":
        numero = random.randint(1, 6)
        embed = crear_embed("🎲 Lanzaste un dado", f"Salió el número **{numero}**")
        await message.channel.send(embed=embed)

    elif content == "!broma":
        bromas = [
            "¿Por qué los programadores confunden Halloween con Navidad? Porque OCT 31 = DEC 25. 🎃🎄",
            "¿Cuál es el animal más antiguo? La cebra, porque está en blanco y negro. 🦓",
            "¿Qué le dice una impresora a otra? ¿Esa hoja es tuya o es una impresión mía? 🖨️",
        ]
        embed = crear_embed("😂 Broma del día", random.choice(bromas), discord.Color.green())
        await message.channel.send(embed=embed)

    elif content == "!8ball":
        respuestas = [
            "Sí, definitivamente 🎯",
            "No cuentes con ello ❌",
            "Pregunta de nuevo más tarde ⏳",
            "Tal vez 🤔",
            "¡Por supuesto! 💯",
            "Mis fuentes dicen que no 📉"
        ]
        embed = crear_embed("🎱 Bola mágica dice:", random.choice(respuestas))
        await message.channel.send(embed=embed)

    elif content == "!comandos":
        descripcion = (
            "**!ping** - Comprueba si el bot está vivo 🏓\n"
            "**!dado** - Lanza un dado 🎲\n"
            "**!broma** - Te cuento una broma divertida 😂\n"
            "**!8ball** - Pregunta algo y recibe una respuesta misteriosa 🎱\n"
            "**!quiengay** - Etiqueta a alguien al azar como 'el más gay' 🌈\n"
            "**!comandos** - Muestra esta lista 📜"
        )
        embed = crear_embed("📜 Lista de Comandos", descripcion, discord.Color.orange())
        await message.channel.send(embed=embed)

    elif content == "!quiengay":
        miembros = [miembro for miembro in message.guild.members if not miembro.bot]
        if miembros:
            elegido = random.choice(miembros)
            embed = crear_embed("🌈 Resultado Gayómetro", f"🎉 El más gay del servidor es: {elegido.mention} 🏳️‍🌈", discord.Color.magenta())
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("No hay miembros válidos en el servidor 😢")

# Iniciar el bot
client.run(TOKEN)
