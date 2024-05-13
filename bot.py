from info import *
import discord
from discord.ext import commands
import aiohttp


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Online")

@bot.command()
async def req(ctx: commands.Context, *, prompt: str):
    async with aiohttp.ClientSession() as session:
        system = {
            "model": "gpt-3.5-turbo-1106",
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 50,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "bestof": 1,
        }

        headers = {"Authorization": f"Bearer {key}"}
        async with session.post("https://api.openai.com/v1/completions", json=system, headers=headers) as resp:
            response = await resp.json()
            await ctx.reply(response)


bot.run(token)
