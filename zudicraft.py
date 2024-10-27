# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
import random
import os

import dialog

class GreetingsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Ask questions to Zudicraft...",
        options=[
            discord.SelectOption(label="Who are you?"),
            discord.SelectOption(label="What are you doing here?"),
        ],
        custom_id="select_greetings",
    )
    async def select_callback(self, interaction, select):
        print(select)
        print(select.values)
        if select.values[0] == "Who are you?":
            await interaction.response.send_message(random.choice(dialog.who_are_you))
        elif select.values[0] == "What are you doing here?":
            await interaction.response.send_message(random.choice(dialog.what_are_you_doing_here))

# Bot initialization
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

# A command to send the persistent view
@bot.command()
async def test(ctx):
    view = GreetingsView()
    await ctx.send("Hello!", view=view)

# Add persistent views on bot startup
@bot.event
async def on_ready():
    # Re-attach the persistent view after bot restarts
    bot.add_view(GreetingsView())  # Reattach the view to listen to interactions
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    print(f'message: {message.content}')
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        print("mentioned zudi")
        if 'hello'.lower() in message.content.lower():
            print('Sending message')
            # await message.channel.send(random.choice(dialog.hello))
            view = GreetingsView()
            await message.channel.send(random.choice(dialog.hello), view=view)

bot.run(os.getenv('DISCORD_TOKEN'))
