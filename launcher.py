import random
from discord.ext import commands
import discord
import config
import emoji


bot = commands.Bot(command_prefix="!")
OK_SIGN = ':thumbsup:'


def is_exception(USERS_NUM):
    EXCEPTIONS = [1, 2, 5]
    for exception in EXCEPTIONS:
        if USERS_NUM == exception:
            return True
    return False


def get_capacity_per_room(users_num):
    ROOMS_NUM = users_num // 3
    capacity_per_room = [3] * ROOMS_NUM
    REMAINDER = users_num % 3
    for i in range(REMAINDER):
        capacity_per_room[i] += 1
    return capacity_per_room


def make_line(room_num, room_members):
    return f"{room_num}号室: {' / '.join(room_members)}\n"


def get_result_str(users):
    USERS_NUM = len(users)
    if USERS_NUM == 0:
        return False

    if is_exception(USERS_NUM):
        result_str = make_line(1, users)
        return result_str

    CAPACITY_PER_ROOM = get_capacity_per_room(USERS_NUM)
    random.shuffle(users)
    result_str = ''
    start_i = 0
    for i, capacity in enumerate(CAPACITY_PER_ROOM, start=1):
        end_i = start_i + capacity
        result_str += make_line(i, users[start_i:end_i])
        start_i += capacity
    return result_str


@bot.event
async def on_ready():
    print("on_ready")


@bot.command()
async def chnick(ctx):
    await ctx.guild.me.edit(nick="おもてなし")


@bot.command()
async def navi(ctx):
    msg = await ctx.fetch_message(config.MESSAGE_ID)
    reactions = msg.reactions
    users = []
    for reaction in reactions:
        if emoji.demojize(reaction.emoji) == ':thumbs_up:':
            reaction_users = await reaction.users().flatten()
            for user in reaction_users:
                users.append(user.mention)
            break
    channel = bot.get_channel(config.CHANNEL_ID)
    result_str = get_result_str(users)
    await channel.send(result_str)


@bot.command()
async def call(ctx):
    embed = discord.Embed()
    color = discord.Color
    green = color.green()
    embed.color = green
    NOTIFICATION = "**新入生コアタイムだよ！ 全員集合！**"
    embed.description = NOTIFICATION

    msg = await ctx.send(embed=embed)
    await msg.add_reaction('\N{THUMBS UP SIGN}')

bot.run(config.TOKEN)