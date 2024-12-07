import discord
import os
import urllib.request


APP_ID = '1314271667387895889'
PUBLIC_KEY = 'a0893ad1dcd97c3e47cc987079acdbc5c2b75f87f79be6f43ccf11de9dea4c1b'
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
BASE_URL = os.environ.get('AWS_BASE_URL')


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


async def show_help(channel):
    await channel.send('使い方')
    await channel.send('/start <target> | /stop <target> | /state <target>')
    await channel.send('target: be (統合版) | je (Java版) | debug (テスト用)')


async def open_url(ctx, target: str, action: str, command: str):
    try:
        if target in ['be', 'je', 'debug']:
            url = f'{BASE_URL}?target={target}&action={action}'
            print('GET', url)
            resp = urllib.request.urlopen(url)
            await ctx.response.send_message(f'`/{command} {target}` へのレスポンス：{resp.read().decode()}')
        else:
            await ctx.response.send_message('無効なターゲットです。')
            await show_help(ctx.channel)
    except Exception as e:
        await ctx.response.send_message(f'エラー：{e}')


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    await tree.sync()
    print('Command tree synced')


@tree.command()
async def start(ctx, target: str):
    print('/start')
    await open_url(ctx, target, 'start', 'start')


@tree.command()
async def stop(ctx, target: str):
    print('/stop')
    await open_url(ctx, target, 'stop', 'stop')


@tree.command()
async def status(ctx, target: str):
    print('/status', repr(target))
    await open_url(ctx, target, 'state', 'status')


@tree.command()
async def help(ctx):
    print('/help')
    ctx.response.send_message('ヘルプを表示します。')
    await show_help(ctx.channel)


client.run(TOKEN)
