import discord
import os
import random
import asyncio
import json

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

PUNTOS_FILE = "puntos.json"
puntos = {}

def guardar_puntos():
    with open(PUNTOS_FILE, "w") as f:
        json.dump(puntos, f)

def cargar_puntos():
    global puntos
    if os.path.exists(PUNTOS_FILE):
        with open(PUNTOS_FILE, "r") as f:
            puntos = json.load(f)

@client.event
async def on_ready():
    cargar_puntos()
    print(f'✅ Bot conectado como {client.user}')

def crear_embed(titulo, descripcion, color=discord.Color.blurple()):
    embed = discord.Embed(title=titulo, description=descripcion, color=color)
    embed.set_footer(text="Bot divertido 😎 | Usa !comandos para ver más")
    return embed

class RuletaRusa(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.players = []

    @discord.ui.button(label="Unirme a la ruleta rusa", style=discord.ButtonStyle.red)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            self.players.append(interaction.user)
            await interaction.response.send_message(f"{interaction.user.mention} se ha unido a la ruleta rusa!", ephemeral=True)
        else:
            await interaction.response.send_message("¡Ya te has unido a la ruleta rusa!", ephemeral=True)

    async def iniciar_ruleta(self, channel):
        if len(self.players) < 2:
            await channel.send("¡No hay suficientes jugadores! Se necesitan al menos 2 jugadores para jugar.")
            return

        await channel.send(f"🎰 ¡La ruleta rusa comenzará ahora con {len(self.players)} jugadores! 🎰")
        await asyncio.sleep(3)
        
        while len(self.players) > 1:
            await asyncio.sleep(5)
            eliminado = random.choice(self.players)
            self.players.remove(eliminado)

            comentarios = [
                f"💥 ¡{eliminado.mention} ha muerto! ¿De verdad pensabas que sobrevivirías? 🤣",
                f"💥 ¡{eliminado.mention} se fue al otro lado! Menos mal que ya no tendremos que escuchar esas tonterías. 😂",
                f"💥 ¡{eliminado.mention} ha muerto! Si sobrevivías, ¿qué pensabas, que ibas a ganar? ¡JAJA! 😆",
                f"💥 ¡{eliminado.mention} ha muerto! Aunque estés muerto, aún sigues siendo el más inútil de todos. 😜",
                f"💥 ¡{eliminado.mention} cayó! Te faltó suerte... o cerebro. 🧠😂"
            ]
            comentario = random.choice(comentarios)

            embed = crear_embed("⚰️ Jugador muerto", comentario, discord.Color.red())
            await channel.send(embed=embed)
        
        ganador = self.players[0]
        await channel.send(f"🏆 ¡{ganador.mention} ha ganado! ¡El primero en morir fue el más gay! 🎉")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if content == "!ping":
        embed = crear_embed("🏓 Pong!", "¡Estoy vivo!")
        await message.channel.send(embed=embed)
    elif message.content.lower() == "!triv":
        preguntas = [
            {"pregunta": "¿Quién pintó la Mona Lisa?", "respuesta": "Leonardo da Vinci"},
            {"pregunta": "¿Cuál es el planeta más grande del sistema solar?", "respuesta": "Júpiter"},
            {"pregunta": "¿En qué año cayó el Muro de Berlín?", "respuesta": "1989"},
            {"pregunta": "¿Cuál es el río más largo del mundo?", "respuesta": "El Amazonas"},
            {"pregunta": "¿Qué instrumento tiene 88 teclas?", "respuesta": "Piano"},
            {"pregunta": "¿Quién es conocido como el padre de la teoría de la relatividad?", "respuesta": "Albert Einstein"},
            {"pregunta": "¿Qué gas constituye la mayor parte de la atmósfera terrestre?", "respuesta": "Nitrógeno"},
            {"pregunta": "¿En qué continente se encuentra el desierto de Sahara?", "respuesta": "África"},
            {"pregunta": "¿Qué ciudad es conocida como la 'Gran Manzana'?", "respuesta": "Nueva York"},
            {"pregunta": "¿Quién escribió 'Don Quijote de la Mancha'?", "respuesta": "Miguel de Cervantes"},
            {"pregunta": "¿Cuál es el país más grande del mundo?", "respuesta": "Rusia"},
            {"pregunta": "¿Cuántos planetas hay en nuestro sistema solar?", "respuesta": "8"},
            {"pregunta": "¿En qué año llegó el hombre a la Luna?", "respuesta": "1969"},
            {"pregunta": "¿Quién fue el primer presidente de los Estados Unidos?", "respuesta": "George Washington"},
            {"pregunta": "¿Qué elemento químico tiene el símbolo 'O'?", "respuesta": "Oxígeno"},
            {"pregunta": "¿Cuál es la capital de Japón?", "respuesta": "Tokio"},
            {"pregunta": "¿En qué país se encuentra la pirámide de Giza?", "respuesta": "Egipto"},
            {"pregunta": "¿Cuántos huesos tiene el cuerpo humano adulto?", "respuesta": "206"},
            {"pregunta": "¿Qué animal es el mamífero más grande del mundo?", "respuesta": "Ballena azul"},
            {"pregunta": "¿Cuál es la lengua más hablada del mundo?", "respuesta": "Chino mandarín"},
            {"pregunta": "¿Cuál es el metal precioso más caro?", "respuesta": "Oro"},
            {"pregunta": "¿Qué famoso científico formuló la ley de la gravedad?", "respuesta": "Isaac Newton"},
            {"pregunta": "¿Quién fue el primer emperador romano?", "respuesta": "Augusto"},
            {"pregunta": "¿En qué país nació la salsa como género musical?", "respuesta": "Cuba"},
            {"pregunta": "¿Qué ciudad es conocida como la 'Ciudad de la Luz'?", "respuesta": "París"},
            {"pregunta": "¿En qué año terminó la Segunda Guerra Mundial?", "respuesta": "1945"},
            {"pregunta": "¿Qué famoso líder sudafricano fue encarcelado durante 27 años?", "respuesta": "Nelson Mandela"},
            {"pregunta": "¿Qué animal tiene el cerebro más grande en relación a su tamaño?", "respuesta": "Delfín"},
            {"pregunta": "¿Cuál es el océano más grande del mundo?", "respuesta": "Océano Pacífico"},
            {"pregunta": "¿Qué famoso pintor cortó una parte de su oreja?", "respuesta": "Vincent van Gogh"},
            {"pregunta": "¿Qué país tiene más habitantes del mundo?", "respuesta": "China"}
        ]

        trivia = random.choice(preguntas)
        await message.channel.send(f"🎤 **Trivia:** {trivia['pregunta']}")
        await message.channel.send("¡Responde en el chat y sé rápido para ganar! ⏳")

        def check(msg):
            return msg.author != client.user and msg.content.lower() == trivia["respuesta"].lower()

        try:
            respuesta = await client.wait_for('message', check=check, timeout=30.0)
            user_id = str(respuesta.author.id)
            if user_id not in puntos:
                puntos[user_id] = 0
            puntos[user_id] += 10
            guardar_puntos()
            await message.channel.send(f"¡Correcto! {respuesta.author.mention} ha ganado 10 puntos. Ahora tiene {puntos[user_id]} puntos 🏆")
        except asyncio.TimeoutError:
            await message.channel.send(f"Tiempo agotado 😢. La respuesta correcta era: **{trivia['respuesta']}**")

   
    elif message.content.lower() == "!puntos":
        user_id = str(message.author.id)
        if user_id not in puntos:
            puntos[user_id] = 0
        await message.channel.send(f"🎯 **{message.author.mention}, tienes {puntos[user_id]} puntos.**")


    elif message.content.lower() == "!ranking":
        ranking = sorted(puntos.items(), key=lambda x: x[1], reverse=True)[:5] 
        if ranking:
            mensaje_ranking = "🏆 **Ranking de Puntos:**\n"
            for i, (user_id, score) in enumerate(ranking, 1):
                user = await client.fetch_user(user_id)
                mensaje_ranking += f"{i}. {user.mention} - {score} puntos\n"
            await message.channel.send(mensaje_ranking)
        else:
            await message.channel.send("No hay jugadores con puntos aún.")
    elif content == "!dado":
        numero = random.randint(1, 6)
        embed = crear_embed("🎲 Lanzaste un dado", f"Salió el número **{numero}**")
        await message.channel.send(embed=embed)

    elif content == "!coinflip":
        resultado = random.choice(["🪙 Cara", "🪙 Cruz"])
        embed = crear_embed("Lanzamiento de moneda", f"Resultado: **{resultado}**", discord.Color.gold())
        await message.channel.send(embed=embed)

    elif content.startswith("!beso"):
        if message.mentions:
            persona = message.mentions[0]
            embed = crear_embed("💋 Beso virtual", f"{message.author.mention} le da un beso a {persona.mention} 😘", discord.Color.red())
        else:
            embed = crear_embed("💋 Beso perdido", "¡Menciona a alguien para mandarle un beso!", discord.Color.red())
        await message.channel.send(embed=embed)

    elif content.startswith("!abrazo"):
        if message.mentions:
            persona = message.mentions[0]
            embed = crear_embed("🤗 Abrazo virtual", f"{message.author.mention} abraza fuertemente a {persona.mention} 🫂", discord.Color.green())
        else:
            embed = crear_embed("🤗 Abrazo al aire", "¡Menciona a alguien para abrazarlo!", discord.Color.green())
        await message.channel.send(embed=embed)

    elif content == "!r":
        opciones = ["✊ Piedra", "📄 Papel", "✂️ Tijera"]
        eleccion_bot = random.choice(opciones)
        embed = crear_embed("Piedra, papel o tijera", f"Yo elijo: **{eleccion_bot}**", discord.Color.teal())
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
            "**!coinflip** - Lanza una moneda (cara o cruz) 🪙\n"
            "**!beso @usuario** - Manda un beso a alguien 😘\n"
            "**!abrazo @usuario** - Da un abrazo a alguien 🤗\n"
            "**!r** - Juega piedra, papel o tijera contra el bot ✊📄✂️\n"
            "**!insulto** - Recibe un insulto de programador amistoso 💀\n"
            "**!frase** - Te doy una frase motivadora 💡\n"
            "**!comandos** - Muestra esta lista 📜\n"
            "**!ruletarusa** - Juega a la ruleta rusa con otros jugadores 🎰"
        )
        embed = crear_embed("📜 Lista de Comandos", descripcion, discord.Color.orange())
        await message.channel.send(embed=embed)
    elif content == "!mods":
        enlace = "https://www.mediafire.com/file/kb03nh03rjefd1x/pet.rar/file"  
        embed = crear_embed(
            "🛠️ Descarga de Mods - Pack oficial",
            "🎮 ¡Prepara tu juego con estilo! Aquí tienes el pack de mods para disfrutar al máximo.\n\n"
            f"🔗 [**Haz clic aquí para descargar**]({enlace})",
            discord.Color.dark_gold()
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/3135/3135715.png")  # Icono opcional
        await message.channel.send(embed=embed)

    elif content == "!server":
        ip_mc = "nebulas.playghosting.com"
        embed = crear_embed(
            "🌐 Servidor de Minecraft - Comunidad Nebulas",
            "🎉 ¡Únete al servidor oficial y juega con amigos!\n\n"
            f"💻 **IP del servidor:** `{ip_mc}`\n"
            "🧱 Modded y lleno de aventuras, ¡no te lo pierdas!\n"
            "🎁 Eventos, retos, y diversión 24/7.",
            discord.Color.green()
        )
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f9/Grass_Block_JE5_BE3.png")  # Bloque de Minecraft
        await message.channel.send(embed=embed)

    elif content == "!ruletarusa":
        # Crea la vista para la ruleta rusa
        view = RuletaRusa()
        await message.channel.send("¡La ruleta rusa está lista! Haz clic en el botón para unirte.", view=view)

        #
        await asyncio.sleep(30)
        await view.iniciar_ruleta(message.channel)

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
