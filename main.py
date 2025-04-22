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
const minecraft = require('minecraft-server-util');
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
            await channel.send("❌ ¡No hay suficientes jugadores! Se necesitan al menos 2 para jugar.")
            return

        embed_inicio = discord.Embed(
            title="🎰 ¡Comienza la Ruleta Rusa!",
            description=f"🎮 Jugadores en la partida: {', '.join(p.mention for p in self.players)}\n\n🔫 Cargando balas...",
            color=discord.Color.dark_red()
        )
        mensaje = await channel.send(embed=embed_inicio)
        await asyncio.sleep(2)

        while len(self.players) > 1:
            await asyncio.sleep(3)

            actual = random.choice(self.players)
            embed_ronda = discord.Embed(
                title="🔫 Girando el tambor...",
                description=f"🎯 Apuntando a {actual.mention}...",
                color=discord.Color.orange()
            )
            await mensaje.edit(embed=embed_ronda)
            await asyncio.sleep(2)

            disparo = random.randint(1, 6)
            if disparo == 1:
                self.players.remove(actual)

                comentarios = [
                    f"💥 ¡{actual.mention} ha muerto! ¿De verdad pensabas que sobrevivirías? 🤣",
                    f"🧠 ¡{actual.mention} se fue al otro lado! Menos mal que ya no tendremos que escuchar sus tonterías. 😂",
                    f"⚰️ ¡{actual.mention} ha muerto! Aunque estés muerto, aún sigues siendo el más inútil de todos. 😜",
                    f"🩸 ¡{actual.mention} cayó! Te faltó suerte... o cerebro. 🧠💀",
                    f"🔫 ¡{actual.mention} perdió! La vida no es para los débiles. 😈"
                ]
                comentario = random.choice(comentarios)

                embed_muerto = discord.Embed(
                    title="☠️ ¡Jugador Eliminado!",
                    description=comentario,
                    color=discord.Color.red()
                )
                await mensaje.edit(embed=embed_muerto)
            else:
                embed_salvado = discord.Embed(
                    title="😮 ¡Sobrevivió!",
                    description=f"{actual.mention} se salvó esta vez... pero no te confíes.",
                    color=discord.Color.green()
                )
                await mensaje.edit(embed=embed_salvado)

        ganador = self.players[0]
        embed_ganador = discord.Embed(
            title="🏆 ¡Tenemos un sobreviviente!",
            description=f"🎉 **{ganador.mention} ha ganado la Ruleta Rusa!**\n\n💀 Todos los demás han caído... ¿Valió la pena?",
            color=discord.Color.gold()
        )
        await channel.send(embed=embed_ganador)

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
    elif content == "!status":
        server_ip = "nebulas.playghosting.com"  # Cambia por la IP de tu servidor
        server = MinecraftServer.lookup(server_ip)

        try:
            status = server.status()
            embed = discord.Embed(
                title="Estado del Servidor de Minecraft",
                description="🟢 ¡El servidor de Minecraft está activo!",
                color=discord.Color.green()
            )
            embed.add_field(name="Jugadores en línea", value=f"👾 {status.players.online} jugadores conectados.")
            embed.add_field(name="IP del Servidor", value=f"🖥️ `{server_ip}`")
        except:
            embed = discord.Embed(
                title="Estado del Servidor de Minecraft",
                description="🔴 No se puede conectar al servidor de Minecraft.",
                color=discord.Color.red()
            )
            embed.add_field(name="Servidor", value="🔴 El servidor está caído o no es accesible en este momento.")

        await message.channel.send(embed=embed)

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
        opciones = {"✊": "Piedra", "📄": "Papel", "✂️": "Tijera"}

        view = discord.ui.View()

        for emoji in opciones:
            async def callback(interaction, emoji=emoji):
                eleccion_usuario = opciones[emoji]
                eleccion_bot = random.choice(list(opciones.values()))

                resultado = ""
                if eleccion_usuario == eleccion_bot:
                    resultado = "🤝 ¡Empate!"
                elif (
                    (eleccion_usuario == "Piedra" and eleccion_bot == "Tijera") or
                    (eleccion_usuario == "Papel" and eleccion_bot == "Piedra") or
                    (eleccion_usuario == "Tijera" and eleccion_bot == "Papel")
                ):
                    resultado = "🎉 ¡Ganaste!"
                else:
                    resultado = "💀 ¡Perdiste!"

                embed = crear_embed(
                    "✊📄✂️ Piedra, Papel o Tijera",
                    f"Tú elegiste: **{eleccion_usuario}**\nYo elegí: **{eleccion_bot}**\n\n**{resultado}**",
                    discord.Color.teal()
                )
                await interaction.response.edit_message(embed=embed, view=None)

            boton = discord.ui.Button(label=opciones[emoji], emoji=emoji, style=discord.ButtonStyle.primary)
            boton.callback = callback
            view.add_item(boton)

        await message.channel.send("🕹️ Elige una opción:", view=view)

    elif content == "!insulto":
        insultos = [
            "Tu lógica tiene más bugs que Windows Vista. 🐛",
            "¡Eres más inútil que un ; en Python! 😂",
            "Si fueras código, te tirarías errores hasta dormido.",
            "Tus ideas tienen tanto sentido como un `print('Hola')` en C++. 🤯"
            "Tu lógica tiene más bugs que Windows Vista. 🐛",
            "¡Eres más inútil que un ; en Python! 😂",
            "Si fueras código, te tirarías errores hasta dormido.",
             "Tus ideas tienen tanto sentido como un `print('Hola')` en C++. 🤯",
             "Tu CPU mental necesita urgentemente un reinicio. 🔁",
             "Eres como una promesa en JavaScript... nunca te resuelves. 💥",
             "No eres lento, eres asincrónico sin `await`. 🐌",
             "Eres más irrelevante que un `break` fuera de un loop.",
             "Tienes menos lógica que un condicional sin condición.",
             "Eres el `404 Not Found` de la inteligencia. 🚫",
             "Hasta Clippy tiene mejores aportes que tú. 📎",
             "Tu nivel de sarcasmo está en `undefined`.",
             "Eres como un semáforo en rojo en GTA... nadie te respeta. 🚗💥",
            "Tienes menos propósito que un div sin estilo. 🧱",
            "Tu flow es más roto que un servidor sin mantenimiento.",
            "Eres como una función sin return... no sirves para nada. 🫠",
            "Tienes más errores que código copiado de Stack Overflow sin entender. 🧠",
            "Tu argumento es tan válido como un else sin if.",
            "Eres el `NullPointerException` de la vida. 🧨",
            "Tu lógica tiene menos sentido que una IA programando con emociones.",
            "Más perdido que un include en un .py.",
            "Tu presencia online tiene más lag que un Wi-Fi de McDonald's. 🍟📶",
            "Eres como un `try` sin `except`, puro crash. 💻🔥",
            "Tu existencia tiene menos compatibilidad que Internet Explorer en 2025. 🗑️",
            "Te faltan más líneas de código que a Flappy Bird. 🐦",
            "Tu energía es más negativa que un bug en producción.",
            "Tienes menos alcance que una variable local fuera del scope.",
            "Eres el print() de los debates: solo haces ruido.",
            "Eres como un teclado sin tecla Enter: innecesario.",
            "Tienes más errores que un estudiante en su primer `merge`. 🧪",
            "Tu habilidad social es equivalente a un servidor sin puertos abiertos. 🔒",
            "Más roto que un shader en Minecraft con 2GB de RAM. 🧱🔥",
            "Si fueras una app, nadie te actualizaría.",
             "Eres como un `while True:` sin break... solo das vueltas. 🌀",
            "Tienes menos sentido común que una IA sin dataset. 🤖📉",
            "Tu lógica haría llorar a un compilador. 😭",
            "Eres más torpe que un NPC con pathfinding roto.",
            "Eres como un código sin comentarios... nadie te entiende. 🤷‍♂️",
              "Tu estilo tiene menos sentido que un CSS en un backend. 🎨💀",
            "Más predecible que un código hardcodeado.",
           "Tu IQ tiene un timeout. ⏳"
        ]
        embed = crear_embed("🔥 Insulto", random.choice(insultos), discord.Color.red())
        await message.channel.send(embed=embed)
    elif content.startswith("!ship"):
        menciones = message.mentions
        if len(menciones) == 2:
            user1 = menciones[0]
            user2 = menciones[1]
            porcentaje = random.randint(0, 100)

            # Emoji de corazones según compatibilidad
            if porcentaje >= 90:
                corazon = "💖💖💖"
                mensaje = "¡Amor verdadero, sin duda alguna! 💍"
            elif porcentaje >= 70:
                corazon = "💘💘"
                mensaje = "¡Una pareja con potencial! 🌹"
            elif porcentaje >= 50:
                corazon = "💗"
                mensaje = "Hmm... podría funcionar 😅"
            elif porcentaje >= 30:
                corazon = "💔"
                mensaje = "Ufff... no pinta bien 😬"
            else:
                corazon = "❌"
                mensaje = "Amistad es lo mejor para ustedes 😂"

            embed = crear_embed(
                "💞 Test de Compatibilidad",
                f"{user1.mention} ❤️ {user2.mention}\n\n"
                f"**Compatibilidad:** `{porcentaje}%` {corazon}\n\n"
                f"_{mensaje}_",
                discord.Color.purple()
            )
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Debes mencionar a dos usuarios para hacer el ship. Ejemplo: `!ship @usuario1 @usuario2`")

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
            "¿Por qué el libro de matemáticas está triste? Porque tiene demasiados problemas. 📘",
            "¿Qué hace una abeja en el gimnasio? ¡Zum-ba! 🐝",
            "¿Cómo se llama el campeón de buceo japonés? Tokofondo. 🏊",
            "¿Y el subcampeón? Kasitoko. 😆",
            "¿Qué le dice un bit a otro? Nos vemos en el bus. 💾",
            "¿Por qué no puedes confiar en un átomo? Porque hacen todo a escondidas. ⚛️",
            "¿Cómo saluda un jardinero? ¡Hola, soy Eduardo y esta es mi pala! 👋",
            "¿Qué le dijo el WiFi al modem? Sin ti no tengo conexión. ❤️",
            "¿Por qué los peces no usan Facebook? Porque ya tienen muchos seguidores. 🐟",
            "¿Qué hace un pez? ¡Nada! 🏊‍♂️",
            "¿Por qué lloraba el libro de historia? Porque tenía demasiados conflictos. 📚",
            "¿Cómo se despiden los químicos? Ácido un placer. 👋",
            "¿Por qué la escoba está feliz? Porque va barriendo éxitos. 🧹",
            "¿Por qué el tomate se puso rojo? Porque vio al otro tomate desnudo. 🍅",
            "¿Qué pasa si tiras un pato al agua? Nada. 🦆",
            "¿Cómo se llama el campeón de buceo alemán? Hunderwasser. 🇩🇪",
            "¿Cómo se llama el padre de todos los chistes malos? Papá chiste. 👨‍🦰",
            "¿Cuál es el colmo de un electricista? No encontrar su corriente ideal. ⚡",
            "¿Qué hace un león en la nevera? ¡Frigorífico! 🦁❄️",
            "¿Qué le dijo un teclado a otro? ¡No te metas en mis espacios! ⌨️",
            "¿Por qué los esqueletos no pelean entre ellos? Porque no tienen agallas. ☠️",
            "¿Qué es lo más divertido de un código mal hecho? Que siempre da risa... de desesperación. 💻",
            "¿Por qué el programador fue al psicólogo? Porque tenía problemas de *cache*. 🧠",
            "¿Por qué el servidor rompió con la base de datos? Porque tenía muchas relaciones. 💔",
            "¿Qué dijo el compilador al código feo? ¡No puedo contigo! 😩",
            "¿Cómo se dice pañuelo en japonés? Saka-moko. 🤧",
            "¿Por qué la luna fue al colegio? Para mejorar sus fases. 🌕",
            "¿Qué hace una neurona en una fiesta? ¡Sinapsis! 🧠🎉",
            "¿Qué hacen dos pollos en un ascensor? ¡Ponen huevos! 🐔",
            "¿Qué hace una vaca con los ojos cerrados? Leche concentrada. 🐄",
            "¿Cómo se despiden los programadores? return 0; 👨‍💻",
            "¿Qué hace un gato en la computadora? Busca el mouse. 🐱🖱️",
            "¿Cuál es el colmo de un matemático? Tener problemas en casa. ➕➖",
            "¿Qué hace un buzo con un libro? Busca el índice. 📖",
            "¿Qué le dijo el café al azúcar? Sin ti, mi vida es amarga. ☕",
            "¿Qué hace una oreja en una fiesta? Escucha música. 👂",
            "¿Qué le dice un programador a su cita? Estás fuera de mi *scope*, pero lo intento. ❤️‍🔥",
        ]
        broma = random.choice(bromas)
        embed = crear_embed("😂 ¡Broma del día!", broma, discord.Color.gold())
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

        if not miembros:
            await message.channel.send("No hay miembros válidos en el servidor 😢")
            return

        embed = discord.Embed(
            title="🌈 Escaneando con el Gayómetro...",
            description="🔎 Preparando escaneo...",
            color=discord.Color.magenta()
        )
        mensaje = await message.channel.send(embed=embed)

        for _ in range(15):  # Número de "pasadas"
            elegido_temp = random.choice(miembros)
            embed.description = f"🔎 Posible gay detectado: {elegido_temp.mention}...\n🌈 Escaneando..."
            await mensaje.edit(embed=embed)
            await asyncio.sleep(0.4)

        elegido_final = random.choice(miembros)
        embed.title = "🌈 Resultado Final del Gayómetro"
        embed.description = f"🎉 ¡El más gay del servidor es: {elegido_final.mention}! 🏳️‍🌈"
        await mensaje.edit(embed=embed)



# Iniciar el bot
client.run(TOKEN)
