import os
import random
import asyncio
from datetime import datetime
import pytz
import sys

import discord
from discord.ext import commands

# ========= CONFIGURAÇÕES =========

SALOMONISSE_ROLE_ID = 1453502439167623289
QUARENTENA_ROLE_ID  = 1453505974282485956
CRONICA_ROLE_ID     = 1453808748387766334

QUARENTENA_CHANNEL_ID = 1453640324097376391

TIMEZONE = pytz.timezone("America/Sao_Paulo")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN não definido")

# ========= INTENTS =========
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

# 👉 BOT PRECISA SER CRIADO ANTES DOS DECORATORS
bot = commands.Bot(command_prefix="!", intents=intents)

# ========= EVENTOS =========
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    await executar_evento()
    await bot.close()
    os._exit(0)

# ========= LÓGICA =========
async def executar_evento():
    for guild in bot.guilds:
        salomonisse = guild.get_role(SALOMONISSE_ROLE_ID)
        quarentena  = guild.get_role(QUARENTENA_ROLE_ID)
        cronica     = guild.get_role(CRONICA_ROLE_ID)
        canal_q     = guild.get_channel(QUARENTENA_CHANNEL_ID)

        if not all([salomonisse, quarentena, cronica, canal_q]):
            continue

        # ===== CRÔNICA =====
        for member in guild.members:
            if member.bot:
                continue

            if salomonisse in member.roles and cronica not in member.roles:
                await member.remove_roles(salomonisse, quarentena)
                await member.add_roles(cronica)

                await canal_q.send(
                    f"☠️ **SALOMONISSE CRÔNICA**\n"
                    f"{member.mention} entrou em estado crônico."
                )

        # ===== INFECÇÃO =====
        candidatos = [
            m for m in guild.members
            if not m.bot
            and salomonisse not in m.roles
            and cronica not in m.roles
        ]

        if candidatos:
            infectado = random.choice(candidatos)
            await infectado.add_roles(salomonisse)

            await canal_q.send(
                f"🦠 **INFECÇÃO CONFIRMADA**\n"
                f"{infectado.mention} foi contaminado pela **Salomonisse (SAV)**."
            )

    print("Evento diário concluído.")

# ========= START =========
bot.run(TOKEN)
