import discord
import os
import urllib.request


TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
BASE_URL = os.environ.get('AWS_BASE_URL')


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


targets = {
    "統合版": "be",
    "Java版": "je",
    "debug": "debug",
}


async def show_help(channel):
    await channel.send("使い方")
    await channel.send("/start <target> | /stop <target> | /state <target>")
    await channel.send("target: be (統合版) | je (Java版) | debug (テスト用)")


async def open_url(
    interaction,
    target: str,
    action: str,
    command: str,
    delete_after: float | None = None,
):
    try:
        if target in ["be", "je", "debug"]:
            url = f"{BASE_URL}?target={target}&action={action}"
            print("GET", url)
            resp = urllib.request.urlopen(url)
            await interaction.response.send_message(
                f"`/{command} {target}` へのレスポンス：{resp.read().decode()}",
                delete_after=delete_after,
            )
        else:
            await interaction.response.send_message(
                "無効なターゲットです。", delete_after=delete_after
            )
            await show_help(interaction.channel)
    except Exception as e:
        await interaction.response.send_message(
            f"エラー：{e}", delete_after=delete_after
        )


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    await tree.sync()
    print("Command tree synced")


@tree.command()
async def start(interaction, target: str):
    print("/start")
    await open_url(interaction, target, "start", "start")


@tree.command()
async def stop(interaction, target: str):
    print("/stop")
    await open_url(interaction, target, "stop", "stop")


@tree.command()
async def status(interaction, target: str):
    print("/status", repr(target))
    await open_url(interaction, target, "state", "status")


@tree.command()
async def help(interaction):
    print("/help")
    interaction.response.send_message("ヘルプを表示します。")
    await show_help(interaction.channel)


class TargetSelection(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="統合版"),
            discord.SelectOption(label="Java版"),
            discord.SelectOption(label="debug"),
        ]
        super().__init__(placeholder="ターゲットを変更", options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"ターゲット：{self.values[0]}")
        self.placeholder = self.values[0]


class ControlButton(discord.ui.Button):
    def __init__(self, label, command):
        super().__init__(label=label)
        self.command = command

    async def callback(self, interaction):
        prefix = "ターゲット："
        target_ja = interaction.message.content[len(prefix) :]
        target = targets.get(target_ja)
        print(f"target: {target}, command: {self.command}")
        await open_url(interaction, target, self.command, self.command, delete_after=3)


@tree.command()
async def dashboard(interaction):
    view = discord.ui.View()
    view.add_item(TargetSelection())
    view.add_item(ControlButton(label="開始", command="start"))
    view.add_item(ControlButton(label="停止", command="stop"))
    view.add_item(ControlButton(label="確認", command="state"))
    await interaction.response.send_message(content="ターゲット：統合版", view=view)


client.run(TOKEN)
