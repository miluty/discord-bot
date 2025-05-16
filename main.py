import discord
import os
import random
import asyncio
import json

TOKEN = "MTM3Mjc3ODcxNzc0MjUwMTk0OA.GsnwDn.fBPGT-zclrQxtaj0C9c5JF9TYUXbJ6boU5Bcbc"

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
    client.add_view(TicketView())  # Esto hace persistente el botón si el bot se reinicia
    print(f'✅ Bot conectado como {client.user}')

def crear_embed(titulo, descripcion, color=discord.Color.blurple()):
    embed = discord.Embed(title=titulo, description=descripcion, color=color)
    embed.set_footer(text="Bot divertido 😎 | Usa !comandos para ver más")
    return embed

# ----------------- Sistema de Tickets ------------------

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # No expira

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.green, custom_id="abrir_ticket")
    async def abrir_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        # Verificar si ya tiene ticket abierto (canal que empiece con ticket- y sea visible para el user)
        for canal in guild.channels:
            if canal.name == f"ticket-{user.name.lower()}" and isinstance(canal, discord.TextChannel):
                # Si el usuario ya tiene un ticket abierto
                await interaction.response.send_message("❌ Ya tienes un ticket abierto.", ephemeral=True)
                return
        
        # Crear el canal de ticket
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        canal_ticket = await guild.create_text_channel(f"ticket-{user.name}", overwrites=overwrites, reason="Nuevo ticket abierto")

        embed_ticket = discord.Embed(
            title="🎫 Ticket Abierto",
            description=f"Hola {user.mention}, gracias por abrir un ticket.\nEscribe aquí tu consulta o problema, el staff te atenderá pronto.",
            color=discord.Color.green()
        )
        await canal_ticket.send(content=user.mention, embed=embed_ticket)

        await interaction.response.send_message(f"✅ Tu ticket ha sido creado: {canal_ticket.mention}", ephemeral=True)

# Comando para enviar el mensaje con el botón del ticket
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if content == "!ticket":
        view = TicketView()
        embed = crear_embed(
            "📩 Sistema de Tickets",
            "Haz click en el botón **Abrir Ticket** para crear un canal privado con el staff y solucionar tus dudas o problemas."
        )
        await message.channel.send(embed=embed, view=view)

    elif content == "!ping":
        embed = crear_embed("🏓 Pong!", "¡Estoy vivo!")
        await message.channel.send(embed=embed)

    elif content == "!triv":
        preguntas = [
            # tus preguntas aquí...
        ]
        # Código trivia (el que ya tienes)

# Aquí continúa el resto de tu código (por ejemplo, clase RuletaRusa, etc)

# Iniciar el bot
client.run(TOKEN)
