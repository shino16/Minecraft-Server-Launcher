import discord
import os


APP_ID = '1314271667387895889'
PUBLIC_KEY = 'a0893ad1dcd97c3e47cc987079acdbc5c2b75f87f79be6f43ccf11de9dea4c1b'
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await tree.sync()
    print('Command tree synced')


@tree.command()
async def launch(ctx):
    print('Launching Minecraft server...')
    await ctx.response.send_message('（ここでサーバを起動する）')


@tree.command()
async def stop(ctx):
    print('Stopping Minecraft server...')
    await ctx.response.send_message('（ここでサーバを停止する）')


@tree.command()
async def restart(ctx):
    print('Restarting Minecraft server...')
    await ctx.response.send_message('（ここでサーバを再起動する）')


@tree.command()
async def status(ctx):
    print('Checking Minecraft server status...')
    await ctx.response.send_message('（ここでサーバの状態を確認する）')


@tree.command()
async def help(ctx):
    print('Showing help...')
    await ctx.response.send_message('（ここでヘルプを表示する）')


client.run(TOKEN)
