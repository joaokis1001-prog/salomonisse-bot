import os
import random
import asyncio
from datetime import datetime
import pytz

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

bot = commands.Bot(command_prefix="!", intents=intents)

# ========= EVENTO =========
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

    # ===== ESPERA ATÉ A MEIA-NOITE =====
    while True:
        agora = datetime.now(TIMEZONE)

        if agora.hour == 0:
            print("Meia-noite detectada. Executando evento diário.")
            break

        await asyncio.sleep(30)  # verifica a cada 30 segundos

    # ===== EXECUÇÃO DIÁRIA =====
    for guild in bot.guilds:
        salomonisse = guild.get_role(SALOMONISSE_ROLE_ID)
        quarentena  = guild.get_role(QUARENTENA_ROLE_ID)
        cronica     = guild.get_role(CRONICA_ROLE_ID)
        canal_q     = guild.get_channel(QUARENTENA_CHANNEL_ID)

        if not all([salomonisse, quarentena, cronica, canal_q]):
            continue

        # ====== PARTE 1: CRÔNICA ======
        for member in guild.members:
            if member.bot:
                continue

            if salomonisse in member.roles and cronica not in member.roles:
                await member.remove_roles(
                    salomonisse,
                    quarentena,
                    reason="Salomonisse Crônica"
                )
                await member.add_roles(
                    cronica,
                    reason="Salomonisse Crônica"
                )

                await canal_q.send(
                    f"☠️ **SALOMONISSE CRÔNICA**\n"
                    f"{member.mention} não se tratou a tempo e agora está em estado **crônico**.\n"
                    f"Acesso à quarentena revogado."
                )

        # ====== PARTE 2: INFECÇÃO ======
        candidatos = [
            m for m in guild.members
            if not m.bot
            and salomonisse not in m.roles
            and cronica not in m.roles
        ]

        if not candidatos:
            await canal_q.send("🦠 Nenhum membro disponível para infecção hoje.")
            continue

        infectado = random.choice(candidatos)
        await infectado.add_roles(
            salomonisse,
            reason="Infecção diária"
        )

        await canal_q.send(
            f"🦠 **INFECÇÃO CONFIRMADA**\n"
            f"{infectado.mention} foi contaminado pela **Salomonisse (SAV)**.\n"
            f"Vá para a quarentena se quiser se tratar."
        )

        print(f"{infectado} infectado em {guild.name}")

    # ===== ENCERRA O BOT =====
    await bot.close()

bot.run(TOKEN)
