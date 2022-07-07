import discord
import os
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv

client = commands.Bot(command_prefix="!")

# Loads the .env file that resides on the same level as the script.
load_dotenv()

# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
api_key = os.getenv("api_key")
base_url = "http://api.openweathermap.org/data/2.5/weather?"


@client.command()
async def sää(ctx, *, city: str):

        city_name = city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&lang=fi"
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel

        if x["cod"] != "404":

                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                feels_like = y["feels_like"]
                z = x["weather"]
                weather_description = z[0]["description"]

                embed = discord.Embed(
                    title=f"Dinosää paikassa {city_name}",
                    color=0x7289DA,
                    timestamp=ctx.message.created_at,
                )
                embed.add_field(
                    name="Sää tällä hetkellä:",
                    value=f"**{weather_description}**",
                    inline=False,
                )
                embed.add_field(
                    name="Lämpötila(C):",
                    value=f"**{current_temperature_celsiuis}°C**",
                    inline=False)
                embed.add_field(
                    name="Kosteus(%):", value=f"**{current_humidity}%**", inline=False)
                embed.set_footer(text=f"Tosi reipas Dino vastasi käyttäjän {ctx.author.name} kyselyyn!")

                await channel.send(embed=embed)

        else:
                await channel.send(
                    f"Dino ei ymmärrä... Kirjoita !dinosää saadaksesi apua.")
                
@client.command()
async def dinosää(ctx,):
    await ctx.send("Ohje Dinosään käyttöön: Kirjoita !sää ja kaupungin nimi, esimerkiksi: !sää Helsinki")



print("Bot has started running")
# execute bot with token 
client.run(DISCORD_TOKEN)

input('Press ENTER to exit')