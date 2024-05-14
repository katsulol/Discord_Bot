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
async def credits(ctx: commands.Context):
    embed = discord.Embed(
        title="Model Credits",
        description="Here are the credits for the models used in this bot and their responsibilities:",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="1. Meta-Llama-3-8B-Instruct",
        value="[Meta-Llama](https://huggingface.co/meta-llama)\nThis is a Free Model that was used for Chat generation",
        inline=False
    )

    embed.add_field(
        name="2. Stable Diffusion XL Base 1.0",
        value="[Stability AI](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)\nThis is a Free Model which was used for Text to Image generation",
        inline=False
    )

    embed.set_footer(text="For more information, visit the provided links.")

    await ctx.send(embed=embed)


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
async def chat(ctx: commands.Context, *, prompt: str):
    headers = {"Authorization": f"Bearer {hf_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(metalama_url, headers=headers, json={"inputs": prompt}) as resp:
            response = await resp.json()

    generated_text = response[0]['generated_text']
    formatted_text = generated_text.replace('\n', '\n\n')


    embed = discord.Embed(
        title=prompt,
        description=generated_text,
        color=discord.Color.blue()
    )
    embed.set_author(name="Meta-Llama-3-8B-Instruct ", url="https://huggingface.co/meta-llama")
    embed.set_footer(text="Model Made by Meta-Llama")
    embed.set_image(url="https://images-ext-1.discordapp.net/external/GIQew_BPVtt8zPS_b_oEOaUty4Frxtx4zM0W6aIW334/https/i.ibb.co/2hZdxL5/image-2024-05-14-141552152.png?format=webp&quality=lossless&width=560&height=96")

    await ctx.reply(embed=embed)


@bot.command()
async def img(ctx: commands.Context, *, prompt: str):
    headers = {"Authorization": f"Bearer {hf_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(Stable_diffusion_URL, headers=headers, json={"inputs": prompt}) as resp:
            response = await resp.read()

    if response:
        file = discord.File(io.BytesIO(response), filename="generated_image.jpg")

        embed = discord.Embed(
            title="Generated Image",
            description=prompt,
            color=discord.Color.blue()
        )
        embed.set_author(name="stable-diffusion-xl-base-1.0", url="https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0")
        embed.set_image(url="attachment://generated_image.jpg")
        embed.set_footer(text = "Model Made by Stability AI")


        await ctx.reply(embed=embed, file=file)
    else:
        await ctx.reply("Failed to generate image.")

bot.run(token)
