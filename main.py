import discord
import asyncio
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

# Crea un cliente de Discord
client = discord.Client(intents=intents)

# ID del canal donde se enviarán las sugerencias y el mensaje de bienvenida
canal_sugerencias_id = 1224882937078612030

# Mensaje de bienvenida
mensaje_bienvenida = "¡Bienvenido al canal de sugerencias! Aquí puedes enviar tus sugerencias y votar por ellas. Después de 1 día, aquellas sugerencias con al menos 5 reacciones positivas permanecerán."


@client.event
async def on_ready():
  print('¡Bot conectado como {0.user}!'.format(client))
  canal_sugerencias = client.get_channel(canal_sugerencias_id)
  # Envía un mensaje de bienvenida al canal de sugerencias
  await canal_sugerencias.send(mensaje_bienvenida)


# Manejador de eventos al detener el bot
@client.event
async def on_shutdown():
  canal_sugerencias = client.get_channel(canal_sugerencias_id)
  await canal_sugerencias.purge(check=lambda m: m.author == client.user)


@client.event
async def on_message(message):
  if message.author == client.user:  # Ignora los mensajes del bot
    return

  if message.channel.id == canal_sugerencias_id:
    canal_sugerencias = client.get_channel(canal_sugerencias_id)
    await message.delete()

    embed = create_suggestion_embed(message.author, message.content)
    suggestion = await canal_sugerencias.send(embed=embed)
    await suggestion.add_reaction('👍'
                                  )  # Agrega el emoji de reacción 'me gusta'
    await asyncio.sleep(86400*3)  # Espera 1 día (86400 segundos)
    suggestion = await canal_sugerencias.fetch_message(suggestion.id)
    thumbs_up = discord.utils.get(suggestion.reactions, emoji='👍')

    if thumbs_up and thumbs_up.count < 5:
      await suggestion.delete()  # Borra el mensaje de sugerencia


def create_suggestion_embed(author, message):
  embed = discord.Embed(title=f"{author}'s suggestion",
                        description=message,
                        color=discord.Color.green())
  embed.set_footer(
      text=
      "React to this message if you want to this to be added.  A minimum of 5 reactions are required within 3 days for the suggestion to be accepted."
  )
  return embed

keep_alive()
token = os.environ['TOKEN']
# Ejecuta el bot con su token
client.run(token)
