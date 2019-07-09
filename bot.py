import os, discord
from discord.ext import commands
import json
import requests
import datetime

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
	message = "Ada yang mau league pair {}?".format(role.mention)
	await ctx.send(message)

@bot.command()
async def team(ctx, kurang=""):
	role = discord.utils.get(ctx.guild.roles, name=os.environ['ROLE'])
	message = "Ada yang mau league team {} {}?".format(kurang,role.mention)
	await ctx.send(message)

@bot.command()
async def kuy(ctx, gametype = ""):
    role = discord.utils.get(ctx.guild.roles, name=os.environ['ROLE'])
    valid_gametype = get_valid_game_type(gametype)
    schedule = get_schedule(valid_gametype)
    msg = "Ada yang mau {}, {}? {}".format(valid_gametype,role.mention, schedule)
    await ctx.send(msg)

def get_valid_game_type(gametype = ""):
    return {
        "": "league",
        "league": gametype,
        "pair": gametype,
        "team": gametype,
        "-1": "league " + gametype,
        "-2": "league " + gametype,
        "salmon": gametype,
        "next": "league rotasi berikutnya",
        "pb": gametype,
        "campursari": "league/salmon"
    }.get(gametype, "league")

def get_schedule_gametype(gametype):
    defaulttype = "league"
    return {
        "salmon": "salmon",
        "pb": "none",
        "campursari": "all"
    }.get(gametype, defaulttype)

def get_schedule(gametype):
    sched_gametype = get_schedule_gametype(gametype)
    print('gametype ' + gametype)
    print('sched gametype ' + sched_gametype)
    schedule_msg = ""
    if sched_gametype != "none":
        if sched_gametype == "all":
            league_schedule = json.loads(requests.get(get_schedule_url("league")).text)
            schedule_msg += generate_schedule_message("league",league_schedule)
            salmon_schedule = json.loads(requests.get(get_schedule_url("salmon")).text)
            schedule_msg += generate_schedule_message("salmon",salmon_schedule)
        else:
            schedules = json.loads(requests.get(get_schedule_url(sched_gametype)).text)
            schedule_msg = generate_schedule_message(sched_gametype,schedules)
    return schedule_msg

def get_schedule_url(gametype):
    defaulturl = "https://splatoon2.ink/data/schedules.json"
    return {
        "league": defaulturl,
        "salmon": "https://splatoon2.ink/data/salmonruncalendar.json"
    }.get(gametype, defaulturl)

def generate_schedule_message(gametype,schedules):
    schedule_message = ""
    if gametype == "league":
        schedule_message = generate_league_schedule_message(schedules)
#    elif gametype == "salmon":
#        schedule_message = generate_salmon_schedule_message(schedules)
    return schedule_message

def generate_league_schedule_message(schedules):
    schedule_msg = "\n"
    league = schedules['league'][0]
    schedule_msg += "Rotasi sekarang: " +league['rule']['name'] + " di " + league['stage_a']['name'] + "/" + league['stage_b']['name']
    next_league = schedules['league'][1]
    schedule_msg += "\nRotasi berikutnya: " + next_league['rule']['name'] + " di " + next_league['stage_a']['name'] + "/" + next_league['stage_b']['name']
    return schedule_msg

def generate_salmon_schedule_message(schedules):
    schedule_msg = "\n"
    salmon = schedules['schedules'][0]

    fromutc = datetime.datetime.utcfromtimestamp
    salmon_start = fromutc(salmon['start_time'])
    salmon_end = fromutc(salmon['end_time'])

    if not is_current(salmon_start, salmon_end):
        schedule_msg += "Maaf, Grizzco Industries sedang tutup."
    else:
        schedule_msg += salmon['stage']['name'] + "\n"
        weapons = salmon['weapons']
        sr_weapons = []
        for weapon in weapons:
            actual_weapon_data = weapon.get('weapon')
            if actual_weapon_data is None:
                weapon_name = 'Rare-only Mystery' if weapon['id'] == '-2' else 'Mystery'
            else:
                weapon_name = actual_weapon_data.get('name', 'Mystery')
            sr_weapons.append(weapon_name)

        schedule_msg += "Senjata: ".join(sr_weapons)

    return schedule_msg

def is_current(start_time, end_time):
    now = datetime.datetime.utcnow()
    return start_time <= now <= end_time

@bot.command()
async def host(ctx):
    await ctx.message.channel.send(file=discord.File('host.png'))

@bot.command()
async def maju(ctx):
    await ctx.message.channel.send(file=discord.File('nevergiveup.png'))

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="SotongBot", description="Daftar commands:", color=0xeee657)

    embed.add_field(name="!kuy [maen]", value="ngajak mabar, [maen] bisa diganti dengan league/pair/team/-1/-2/salmon/next/pb/campursari", inline=False)
    embed.add_field(name="!pair", value="ngajak league pair", inline=False)
    embed.add_field(name="!team [yuk]", value="ngajak league team, [yuk] bisa diganti dengan -1/-2", inline=False)
    embed.add_field(name="!host", value="menampilkan profile host mabar kebanggaan kita bersama", inline=False)
    embed.add_field(name="!maju", value="menampilkan prinsip yang harus dipegang tiap inkling/octoling", inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ['BOT_TOKEN'])
