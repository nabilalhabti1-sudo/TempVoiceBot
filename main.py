import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

TEMP_CATEGORY_NAME = "Temporary Voice Channels"
JOIN_CHANNEL_NAME = "Join to Create"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # User joins the "Join to Create" channel
    if after.channel and after.channel.name == JOIN_CHANNEL_NAME:
        guild = member.guild
        category = discord.utils.get(guild.categories, name=TEMP_CATEGORY_NAME)
        if not category:
            category = await guild.create_category(TEMP_CATEGORY_NAME)

        temp_channel = await guild.create_voice_channel(
            name=f"{member.name}’s Room",
            category=category
        )

        await member.move_to(temp_channel)
        print(f"Created room for {member.name}")

    # Delete empty temp channels
    if before.channel and before.channel.category and before.channel.category.name == TEMP_CATEGORY_NAME:
        if len(before.channel.members) == 0 and before.channel.name != JOIN_CHANNEL_NAME:
            await before.channel.delete()
            print(f"Deleted empty channel: {before.channel.name}")

bot.run(os.getenv("TOKEN"))
