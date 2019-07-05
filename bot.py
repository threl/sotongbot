import os, discord
from discord.ext import commands

bot = commands.Bot(os.environ['COMMAND_PREFIX'])

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

@bot.command()
async def kuy(ctx, gametype = ""):
    msg = "Ada yang mau " + get_valid_game_type(gametype) + ", " + os.environ['ROLE'] + "?"
    await ctx.send(msg)

def get_valid_game_type(gametype = ""):
    return {
        "": "league",
        "league": "league",
        "salmon": gametype,
        "next": "league rotasi berikutnya",
        "pb": gametype,
        "campursari": "league/salmon"
    }.get(gametype, "league")

@bot.command()
async def host(ctx):
    await ctx.message.channel.send(file=discord.File('host.png'))

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="SotongBot", description="Daftar commands:", color=0xeee657)

    embed.add_field(name="!kuy [maen]", value="[maen] bisa diganti dengan league/salmon/next/pb/campursari", inline=False)
    embed.add_field(name="!host", value="menampilkan profile host mabar kebanggaan kita bersama", inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ['BOT_TOKEN'])
