import os
import logging
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from discord.ext import commands
from responses import get_response
from responses import get_chuck_norris_joke
from responses import get_random_image
from responses import get_advice

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the token from the .env file
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Set up bot intents
intents: Intents = Intents.default()
intents.message_content = True  # NOQA

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


# Define a command to stop the bot
@bot.command(name='shutdown', help='Shuts down the bot')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.close()

@bot.command()
async def chucknorris(ctx):
    joke = get_chuck_norris_joke()
    await ctx.send(joke)

@bot.command()
async def randomimage(ctx):
    image_url = get_random_image()
    await ctx.send(image_url)

@bot.command()
async def advice(ctx):
    advice_text = get_advice()
    await ctx.send(advice_text)

@bot.event
async def on_ready() -> None:
    """Handle bot startup."""
    logger.info(f'{bot.user} is now running!')


@bot.event
async def on_message(message: Message) -> None:
    """Handle incoming messages."""
    if message.author == bot.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    logger.info(f'[{channel}] {username}: "{user_message}"')

    if user_message.startswith('!') or user_message.startswith('?'):
        await bot.process_commands(message)
    else:
        await send_message(message, user_message)


async def send_message(message: Message, user_message: str) -> None:
    """Send a response to a user's message."""
    if not user_message:
        logger.warning('Message was empty, intents might not be enabled properly.')
        return

    is_private = user_message.startswith('?')
    if is_private:
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        logger.error(f'Error sending message: {e}', exc_info=True)


def main() -> None:
    """Main entry point for the bot."""
    if TOKEN is None:
        logger.critical('Discord token is not set. Please set the DISCORD_TOKEN environment variable.')
        return
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
