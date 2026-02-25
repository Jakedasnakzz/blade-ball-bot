import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---- ABILITY DATA ---- #

abilities = {
    "Dribble": {"v2": True},
    "Singularity": {"v2": True},
    "Necromancer": {"v2": True},
    "Slashes Of Fury": {"v2": True},
    "Infinity": {"v2": False},
    "Slash of Duality": {"v2": True},
    "Death Slash": {"v2": True},
    "Titan": {"v2": True},
    "Time Hole": {"v2": True},
    "Dragon Spirit": {"v2": True},
    "DOPPELGÄNGER": {"v2": True},
    "Phantom": {"v2": True},
    "Fracture": {"v2": True},
    "Bunny Leap": {"v2": True},
}

# ---- BOT READY ---- #

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# ---- SLASH COMMAND TO CREATE MENUS ---- #

@bot.tree.command(name="setup", description="Setup ability role menus")
async def setup(interaction: discord.Interaction):
    await interaction.response.send_message("Ability menus created!", ephemeral=True)

    for ability, data in abilities.items():

        options = []

        if data["v2"]:
            options.append(discord.SelectOption(label=f"{ability} V1"))
            options.append(discord.SelectOption(label=f"{ability} V2"))
        else:
            options.append(discord.SelectOption(label=f"{ability}"))

        select = discord.ui.Select(
            placeholder=f"Select {ability}",
            options=options,
            custom_id=ability
        )

        async def select_callback(inter: discord.Interaction, ability_name=ability):
            selected = inter.data["values"][0]
            guild = inter.guild
            member = inter.user

            # Remove opposite version if exists
            if "V1" in selected:
                opposite = f"{ability_name} V2"
            elif "V2" in selected:
                opposite = f"{ability_name} V1"
            else:
                opposite = None

            if opposite:
                role = discord.utils.get(guild.roles, name=opposite)
                if role in member.roles:
                    await member.remove_roles(role)

            role = discord.utils.get(guild.roles, name=selected)
            if role:
                await member.add_roles(role)

            # IMAGE SWITCH LOGIC
            if "V2" in selected:
                image_url = f"https://your-image-link.com/{ability_name}-v2.png"
            else:
                image_url = f"https://your-image-link.com/{ability_name}-v1.png"

            embed = discord.Embed(
                title=selected,
                description=f"You now have {selected}",
                color=discord.Color.random()
            )
            embed.set_image(url=image_url)

            await inter.response.send_message(embed=embed, ephemeral=True)

        select.callback = select_callback

        view = discord.ui.View()
        view.add_item(select)

        embed = discord.Embed(
            title=ability,
            description="Select your version below",
            color=discord.Color.blue()
        )

        await interaction.channel.send(embed=embed, view=view)

bot.run(TOKEN)