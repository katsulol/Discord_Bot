import discord
from discord.ext import commands
import aiohttp
from info import *
import io

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


@bot.command()
async def req2(ctx: commands.Context, *, prompt: str):
    headers = {"Authorization": f"Bearer {hf_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(distil_url, headers=headers, json={"inputs": prompt}) as resp:
            response = await resp.json()

    generated_text = response[0]['generated_text']
    formatted_text = generated_text.replace('\n', '\n\n')

    await ctx.reply(formatted_text)


@bot.command()
async def chat(ctx: commands.Context, *, prompt: str):
    headers = {"Authorization": f"Bearer {hf_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(metalama_url, headers=headers, json={"inputs": prompt}) as resp:
            response = await resp.json()

    generated_text = response[0]['generated_text']
    formatted_text = generated_text.replace('\n', '\n\n')

    await ctx.reply(formatted_text)


@bot.command()
async def img(ctx: commands.Context, *, prompt: str):
    headers = {"Authorization": f"Bearer {hf_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(Stable_diffusion_URL, headers=headers, json={"inputs": prompt}) as resp:
            response = await resp.read()

    if response:
        file = discord.File(io.BytesIO(response), filename="generated_image.jpg")
        await ctx.reply(file=file)
    else:
        await ctx.reply("Failed to generate image.")


bot.run(token)
