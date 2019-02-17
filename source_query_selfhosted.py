import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
import asyncio
import aiohttp

###################################################################################################################################################################
# Config
bot_token = "" # Discord bot token. Find at https://discordapp.com/developers/applications/me
set_prefix = '!' # Sets command prefix.
server_channel = '' # Channel ID for servers to be posted in.
embed_color = 0xE8CA11   # Do not remove 0x  || Message Color. Hex, 6 characters. Do NOT include # | Helpful link https://htmlcolorcodes.com/color-picker/
update_time  = 120 # How many seconds should it take to update.

ips = "ip:port-ip:port-ip:port" # The amount of servers are limited due to discord's message character limit.
###################################################################################################################################################################

bot = commands.Bot(command_prefix=set_prefix)

@bot.event
async def on_ready():
    print("Bot connected!\nCurrently linked to {}".format(bot.user.name))

async def background_loop():
    await bot.wait_until_ready()
    first_load = 1
    while not bot.is_closed:
        server_details = ''
        async with aiohttp.get('https://districtnine.host/api/serverquery/?ip={}'.format(ips)) as r:
            if r.status == 200:
                data = await r.json()
                for query in data:
                    if query["error"] != "server-down":
                        server_details += "\n\n**Name:** {} \n**Map**: {}\n**Players:** {}\{} \nsteam://connect/{}".format(query["name"], query["map"], query["players"], query["maxplayers"], query["ip"])
                    else:
                        server_details += "\n\n**IP:** {} \n**Status:** Offline".format(query["ip"])
                embed = discord.Embed(colour=discord.Colour(embed_color))
                embed.add_field(name="SERVERS", value=server_details, inline=False)
                if first_load == 1:
                    first_load = 0
                    msg = await bot.send_message(bot.get_channel(server_channel), embed=embed)
                else:
                    msg = await bot.edit_message(msg, embed=embed)

        await asyncio.sleep(update_time)

bot.loop.create_task(background_loop())

bot.run(bot_token)