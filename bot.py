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
async def pair(ctx):
	role = discord.utils.get(ctx.guild.roles, name=os.environ['ROLE'])
	message = "Ada yang mau pair {}?".format(role.mention)
	await ctx.send(message)

@bot.command()
async def kuy(ctx, gametype = ""):
    role = discord.utils.get(ctx.guild.roles, name=os.environ['ROLE'])
    msg = "Ada yang mau {}, {}?".format(get_valid_game_type(gametype),role.mention)
    await ctx.send(msg)

def get_valid_game_type(gametype = ""):
    return {
        "": "league",
        "league": gametype,
        "pair": gametype,
        "+1": "league " + gametype,
        "+2": "league " + gametype,
        "salmon": gametype,
        "next": "league rotasi berikutnya",
        "pb": gametype,
        "campursari": "league/salmon"
    }.get(gametype, "league")

@bot.command()
async def host(ctx):
    await ctx.message.channel.send(file=discord.File('host.png'))

@bot.command()
async def maju(ctx):
    await ctx.message.channel.send(file=discord.File('nevergiveup.png'))

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="SotongBot", description="Daftar commands:", color=0xeee657)

    embed.add_field(name="!kuy [maen]", value="ngajak mabar, [maen] bisa diganti dengan league/pair/+1/+2/salmon/next/pb/campursari", inline=False)
    embed.add_field(name="!pair", value="ngajak league pair", inline=False)
    embed.add_field(name="!host", value="menampilkan profile host mabar kebanggaan kita bersama", inline=False)
    embed.add_field(name="!maju", value="menampilkan prinsip yang harus dipegang tiap inkling/octoling", inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ['BOT_TOKEN'])
