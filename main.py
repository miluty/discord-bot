import discord
import os
import random
import asyncio

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

    elif content == "!coinflip":
        resultado = random.choice(["🪙 Cara", "🪙 Cruz"])
        embed = crear_embed("Lanzamiento de moneda", f"Resultado: **{resultado}**", discord.Color.gold())
        await message.channel.send(embed=embed)

    elif content.startswith("!r"):
        # Enviar mensaje pidiendo al usuario elegir
        instrucciones = "¡Es tu turno! Elige entre: ✊ Piedra, 📄 Papel o ✂️ Tijera. Tienes 10 segundos para elegir. ⏳"
        embed = crear_embed("Piedra, Papel o Tijera", instrucciones, discord.Color.teal())
        await message.channel.send(embed=embed)

        def check(msg):
            return msg.author == message.author and msg.content.lower() in ["!piedra", "!papel", "!tijera"]

        try:
            # Esperar la respuesta del usuario por 5 segundos
            user_msg = await client.wait_for('message', timeout=10.0, check=check)
            user_choice = user_msg.content.lower()
            opciones = ["!piedra", "!papel", "!tijera"]

            if user_choice not in opciones:
                await message.channel.send(f"¡Tiempo agotado! No elegiste una opción válida.")
                return

        except asyncio.TimeoutError:
            await message.channel.send("¡Tiempo agotado! No elegiste una opción a tiempo.")
            return

        # Elección del bot
        elecciones = {
            "!piedra": "✊ Piedra",
            "!papel": "📄 Papel",
            "!tijera": "✂️ Tijera"
        }
        eleccion_bot = random.choice(["!piedra", "!papel", "!tijera"])
        eleccion_usuario = elecciones[user_choice]
        eleccion_bot_texto = elecciones[eleccion_bot]

        # Resultado
        resultado = ""
        if user_choice == eleccion_bot:
            resultado = "Es un empate. 🤝"
        elif (user_choice == "!piedra" and eleccion_bot == "!tijera") or (user_choice == "!papel" and eleccion_bot == "!piedra") or (user_choice == "!tijera" and eleccion_bot == "!papel"):
            resultado = "¡Ganaste! 🎉"
        else:
            resultado = "¡Perdiste! 😞"

        embed = crear_embed(
            "Piedra, Papel o Tijera",
            f"**Tú elegiste:** {eleccion_usuario}\n**Yo elegí:** {eleccion_bot_texto}\n{resultado}",
            discord.Color.green() if resultado == "¡Ganaste! 🎉" else discord.Color.red()
        )
        await message.channel.send(embed=embed)

    elif content == "!insulto":
        insultos = [
            "Tu lógica tiene más bugs que Windows Vista. 🐛",
            "¡Eres más inútil que un ; en Python! 😂",
            "Si fueras código, te tirarías errores hasta dormido.",
            "Tus ideas tienen tanto sentido como un `print('Hola')` en C++. 🤯"
        ]
        embed = crear_embed("🔥 Insulto", random.choice(insultos), discord.Color.red())
        await message.channel.send(embed=embed)

    elif content == "!frase":
        frases = [
            "No te rindas, el principio siempre es lo más difícil 💪",
            "El código es como el amor: confuso, pero hermoso ❤️",
            "Cada error es una oportunidad para aprender 👨‍💻",
            "A veces ganarás, otras aprenderás 📈"
        ]
        embed = crear_embed("💡 Frase motivadora", random.choice(frases), discord.Color.yellow())
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
            "**!coinflip** - Lanza una moneda (cara o cruz) 🪙\n"
            "**!beso @usuario** - Manda un beso a alguien 😘\n"
            "**!abrazo @usuario** - Da un abrazo a alguien 🤗\n"
            "**!r** - Juega piedra, papel o tijera contra el bot ✊📄✂️\n"
            "**!insulto** - Recibe un insulto de programador amistoso 💀\n"
            "**!frase** - Te doy una frase motivadora 💡\n"
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


client.run(TOKEN)
