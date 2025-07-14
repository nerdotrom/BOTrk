import os
import random
import json
from discord.ext import commands
import discord
from discord import app_commands
import re

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix="/", intents=intents, case_insensitive=False)

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Goth holčiny"))
    try:
        synced = await bot.tree.sync()  # Synchronizace příkazů
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error during sync: {e}")
    print(f'Bot connected as {bot.user}')

# Custom check to verify if the user is an administrator
def is_admin(interaction: discord.Interaction) -> bool:
     return interaction.user.guild_permissions.administrator

@bot.tree.command(name="autori", description="Zobrazí autory")
async def autori(interaction: discord.Interaction):
    author_ids = [506557497000329227, 342309656720572426]
    mentions = ' '.join([f'<@{user_id}>' for user_id in author_ids])
    await interaction.response.send_message(f"Stvořili:  {mentions}", ephemeral=True)

@bot.tree.command(name="hra", description="Vysledek hry") # id test server vysledky - 1311330741396705282 #id real server vysledky - 1298913647338323978
@app_commands.check(is_admin)
async def hra(interaction: discord.Interaction, vyherce: discord.Role, proherce: discord.Role, vysledek: str):
    #await interaction.response.defer()

    channel = bot.get_channel(1298913647338323978)
    


    if not re.match(r"^2:(0|1)$", vysledek):
        await interaction.response.send_message("Špatný formát výsledku", ephemeral=True)
        return

    embed = discord.Embed(title="Výsledek hry", color=discord.Color.random())
    embed.add_field(name="🎉 Vítěz: ", value=f"{vyherce.mention}", inline=False)
    embed.add_field(name="💔 Poražený: ", value=f"{proherce.mention}", inline=False)
    embed.add_field(name="Výsledek", value=f"{vysledek}", inline=False)

    await channel.send(content=f"{vyherce.mention} {proherce.mention}", embed=embed)
    await interaction.response.send_message("Výsledek hry byl odeslán.", ephemeral=True)

    # Update JSON data
    last_number = vysledek.split(":")[-1]

    for team in data['teams']:
        if team['team'] == vyherce.name:
            if last_number == "0":
                team['body'] += 3
            else:
                team['body'] += 2
            team['vyhry'] += 1
        if team['team'] == proherce.name:
            if last_number == "1":
                team['body'] += 1
            team['prohry'] += 1

    # Save updated data back to JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Sort teams by body (score) in descending order
    sorted_teams = sorted(data['teams'], key=lambda x: x['body'], reverse=True)

    # Create an embed for the leaderboard
    embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())

    pocitadlo = 0
    for team in sorted_teams:
        pocitadlo += 1
        embed.add_field(name=f"{pocitadlo}. {team['team']}", value=f"Body: **{team['body']}**, Výhry: {team['vyhry']}, Prohry: {team['prohry']}", inline=False)
        

    channel = bot.get_channel(1303096319346343958) #test 1311330934066511903 #real 1303096319346343958
    await channel.send(embed=embed)
    
    
@bot.tree.command(name="tabulka", description="Zobrazí pořadí týmů")
@app_commands.check(is_admin)
async def tabulka(interaction: discord.Interaction):
    # Save updated data back to JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Sort teams by body (score) in descending order
    sorted_teams = sorted(data['teams'], key=lambda x: x['body'], reverse=True)

    # Create an embed for the leaderboard
    embed = discord.Embed(title="🏆 Leaderboard", color=discord.Color.gold())

    pocitadlo = 0
    for team in sorted_teams:
        pocitadlo += 1
        embed.add_field(name=f"{pocitadlo}. {team['team']}", value=f"Body: **{team['body']}**, Výhry: {team['vyhry']}, Prohry: {team['prohry']}", inline=False)
        

    channel = bot.get_channel(1303096319346343958) #test 1311330934066511903 #real 1303096319346343958
    await channel.send(embed=embed)
    await interaction.response.send_message("Tabulka updatována.", ephemeral=True)
@hra.error
async def hra_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("Chtěl sis připsat bodíky co?", ephemeral=True)

bot.run("MTMxMTMyOTc4NjM5NTc1NDU3OQ.Gjc0vW.y4JaNpOeAV6ryC-YPsteuS82Q7IIRZTrllI6M4")