import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.presences = True
intents.message_content = True  # Needed for commands

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 1357179088405663904
ROLE_NAME = "Diamond Boosters"
LOG_CHANNEL_ID = 1388343324888403998  # Replace with your actual log channel ID

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.event
async def on_member_update(before, after):
    guild = after.guild
    channel = guild.get_channel(LOG_CHANNEL_ID)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)

    if before.premium_since is None and after.premium_since is not None:
        if role:
            await after.add_roles(role)
            print(f"Gave {ROLE_NAME} to {after.name}")
            if channel:
                await channel.send(f"🌟 {after.mention} just boosted the server! Role given.")

    elif before.premium_since is not None and after.premium_since is None:
        if role:
            await after.remove_roles(role)
            print(f"Removed {ROLE_NAME} from {after.name}")
            if channel:
                await channel.send(f"⚠️ {after.mention} stopped boosting. Role removed.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def syncboosters(ctx):
    role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
    if not role:
        await ctx.send(f"❌ '{ROLE_NAME}' role not found.")
        return

    count_added = 0
    count_removed = 0

    for member in ctx.guild.members:
        is_boosting = member.premium_since is not None
        has_role = role in member.roles

        if is_boosting and not has_role:
            await member.add_roles(role)
            count_added += 1
        elif not is_boosting and has_role:
            await member.remove_roles(role)
            count_removed += 1

    await ctx.send(f"✅ Sync complete: {count_added} given, {count_removed} removed.")

@bot.command()
@commands.has_permissions(manage_roles=True)  # Optional: limit to admins
async def checkboosters(ctx):
    boosters = []
    for member in ctx.guild.members:
        if member.premium_since is not None:
            boosters.append(member.display_name)

    if not boosters:
        await ctx.send("😢 No one is currently boosting the server.")
    else:
        booster_list = "\n".join([f"- {name}" for name in boosters])
        await ctx.send(f"💎 Current boosters ({len(boosters)}):\n{booster_list}")
                

# Make sure this is LAST
bot.run("TOKEN")