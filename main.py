import discord
from discord.ext import commands
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# --- 🎭 CAMUFLAJE TÁCTICO (SERVIDOR WEB) ---
app = Flask('')

@app.route('/')
def home():
    return "¡SISTEMA OPERATIVO! El bot está vivo."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 🔐 CONFIGURACIÓN ---
# OJO: Ya no pegamos las claves aquí. Las leeremos de Render.
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ UNIDAD {bot.user} EN LÍNEA EN LA NUBE")
    await bot.change_presence(activity=discord.Game(name="Protegiendo el Server ☁️"))

@bot.command()
async def ia(ctx, *, pregunta):
    async with ctx.typing():
        try:
            response = model.generate_content(pregunta)
            text = response.text
            if len(text) > 2000:
                await ctx.send(text[:2000] + "...")
            else:
                await ctx.send(text)
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

# --- ARRANQUE ---
keep_alive() # Activamos el servidor web primero
bot.run(DISCORD_TOKEN) # Luego el bot