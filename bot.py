@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(evento_diario())


async def evento_diario():
    # ===== ESPERA ATÉ A MEIA-NOITE =====
    while True:
        agora = datetime.now(TIMEZONE)

        if agora.hour == 0 and agora.minute == 0:
            print("Meia-noite detectada. Executando evento diário.")
            break

        await asyncio.sleep(20)

    # ===== EXECUÇÃO =====
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
                    f"{member.mention} entrou em estado crônico.\n"
                    f"Acesso à quarentena revogado."
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

    print("Evento finalizado. Encerrando bot.")

    await bot.close()
    os._exit(0)  # 🔥 encerra o processo de vez
