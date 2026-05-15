import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from flask import Flask
from threading import Thread

# Carrega o arquivo .env
load_dotenv()

# Pega o token do .env
TOKEN = os.getenv("TOKEN")
print("TOKEN encontrada:", TOKEN is not None)

# Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot online"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ID do canal proibido
# Clique no canal do Discord > Copiar ID
CANAL_PROIBIDO = 1504581872968007770

# Intents necessárias
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Cria o bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Quando o bot ligar
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# Detecta mensagens
@bot.event
async def on_message(message):

    # Ignora mensagens do próprio bot
    if message.author.bot:
        return
    # Ignora administradores
    if message.author.guild_permissions.administrator:
        return

    # Verifica se a mensagem foi no canal proibido
    if message.channel.id == CANAL_PROIBIDO:

        try:
            # Apaga a mensagem enviada
            await message.delete()

            # Embed de aviso
            embed = discord.Embed(
                title="🚫 MENSAGEM PROIBIDA",
                description=(
                    f"{message.author.mention} enviou mensagem no canal proibido.\n\n"
                    f"🔨 Ban automático aplicado."
                ),
                color=discord.Color.red()
            )

            # Envia aviso
            await message.channel.send(embed=embed)

            # Bane o usuário
            await message.guild.ban(
                message.author,
                reason="Mensagem enviada em canal proibido"
            )

            print(f"{message.author} foi banido.")

        except Exception as e:
            print(f"Erro: {e}")
# Inicia Flask
keep_alive()

# Liga o bot
bot.run(TOKEN)