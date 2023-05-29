import discord
import os, NaaGPT
import interactions
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
OWNER_ID = int(os.getenv('OWNER_ID'))

intents = discord.Intents.all()
intents.members = True
bot = interactions.Client(activity=discord.Game("Generate Responses"),
                          status=discord.Status.do_not_disturb)


@interactions.listen()
async def on_startup():
    print(f"Logged in as {bot.user}")


@bot.event()
async def on_ready():
    print("Im ready!")


def generate_response(prompt):
    response = NaaGPT.generate_response(prompt)
    return response


def generate_coding_response(prompt):
    response = NaaGPT.generate_coding_response(prompt)
    return response


def generate_image(style, ratio, description):
    image = NaaGPT.generate_image(style, ratio, description)
    return image


def response_split(response, response_max_length):
    response_chunks = []
    current_chunk = ""
    words = response.split(' ')
    for word in words:
        if len(current_chunk) + len(word) < response_max_length:
            current_chunk = current_chunk + word + ' '
        else:
            response_chunks.append(current_chunk.strip())
            current_chunk = word + ' '
    if current_chunk:
        response_chunks.append(current_chunk.strip())

    return response_chunks

'''
def response_split(response, response_max_length):
  lines = response.splitlines()
  response_chunks = []
  current_chunk = ""
  for line in lines:
    if len(current_chunk) + len(line) + 1 > response_max_length:
      response_chunks.append(current_chunk.strip())
      current_chunk = line
    else:
      if current_chunk:
        current_chunk += '\n'
        current_chunk += line
        
  if current_chunk:
    response_chunks.append(current_chunk.strip())

  return response_chunks
  '''

###########################################
# 1) "ask" command
@interactions.slash_command(name="ask",
                            description="I can help to answer any questions",
                            scopes=[GUILD_ID])

@interactions.slash_option(name="prompt",
                           description="Enter your prompt",
                           required=True,
                           opt_type=interactions.OptionType.STRING)

async def ask(ctx: interactions.SlashContext, prompt: str):
    await ctx.defer()
    response_max_size = 1900
    response = generate_response(prompt)
    if len(response) <= response_max_size:
        await ctx.respond(response)
    else:
        response_chunks = response_split(response, response_max_size)
        for chunk in response_chunks:
            await ctx.respond(chunk)

###########################################
# 2) "tts-ask" command
@interactions.slash_command(name="tts-ask",
                            description="I can help to answer any questions in text-to-speech",
                            scopes=[GUILD_ID])

@interactions.slash_option(name="prompt",
                           description="Enter your prompt",
                           required=True,
                           opt_type=interactions.OptionType.STRING)

async def tts_ask(ctx: interactions.SlashContext, prompt: str):
    await ctx.defer()
    response_max_size = 1900
    response = generate_response(prompt)
    if len(response) <= response_max_size:
        await ctx.respond(response, tts=True)
    else:
        response_chunks = response_split(response, response_max_size)
        for chunk in response_chunks:
            await ctx.respond(chunk, tts=True)


###########################################
# 3) "image" command
@interactions.slash_command(name="image",
                            description="I can generate PNG images you want",
                            scopes=[GUILD_ID])

@interactions.slash_option(
    name="style",
    description="Enter image style",
    required=True,
    opt_type=interactions.OptionType.STRING,
    choices=[
        interactions.SlashCommandChoice(name='Imagine V4 Beta',
                                        value='IMAGINE_V4_Beta'),
        interactions.SlashCommandChoice(name='Realistic', value='REALISTIC'),
        interactions.SlashCommandChoice(name='Anime', value='ANIME_V2'),
        interactions.SlashCommandChoice(name='Disney', value='DISNEY'),
        interactions.SlashCommandChoice(name='Studio Ghibli',
                                        value='STUDIO_GHIBLI'),
        interactions.SlashCommandChoice(name='Graffiti', value='GRAFFITI'),
        interactions.SlashCommandChoice(name='Medieval', value='MEDIEVAL'),
        interactions.SlashCommandChoice(name='Fantasy', value='FANTASY'),
        interactions.SlashCommandChoice(name='Neon', value='NEON'),
        interactions.SlashCommandChoice(name='Cyberpunk', value='CYBERPUNK'),
        interactions.SlashCommandChoice(name='Landscape', value='LANDSCAPE'),
        interactions.SlashCommandChoice(name='Japanese Art', value='JAPANESE_ART'),
        interactions.SlashCommandChoice(name='Steampunk', value='STEAMPUNK'),
        interactions.SlashCommandChoice(name='Sketch', value='SKETCH'),
        interactions.SlashCommandChoice(name='Comic Book', value='COMIC_BOOK'),
        interactions.SlashCommandChoice(name='Imagine V4 creative',
                                        value='V4_CREATIVE'),
        interactions.SlashCommandChoice(name='Imagine V3', value='IMAGINE_V3'),
        interactions.SlashCommandChoice(name='Cosmic', value='COMIC_V2'),
        interactions.SlashCommandChoice(name='Logo', value='LOGO'),
        interactions.SlashCommandChoice(name='Pixel art', value='PIXEL_ART'),
        interactions.SlashCommandChoice(name='Interior', value='INTERIOR'),
        interactions.SlashCommandChoice(name='Mystical', value='MYSTICAL'),
        interactions.SlashCommandChoice(name='Super realism', value='SURREALISM'),
        interactions.SlashCommandChoice(name='Minecraft', value='MINECRAFT'),
        interactions.SlashCommandChoice(name='Dystopian', value='DYSTOPIAN')
    ])

@interactions.slash_option(
    name="ratio",
    description="Enter image ratio",
    required=True,
    opt_type=interactions.OptionType.STRING,
    choices=[
        interactions.SlashCommandChoice(name='1x1', value='RATIO_1X1'),
        interactions.SlashCommandChoice(name='9x16', value='RATIO_9X16'),
        interactions.SlashCommandChoice(name='16x9', value='RATIO_16X9'),
        interactions.SlashCommandChoice(name='4x3', value='RATIO_4X3'),
        interactions.SlashCommandChoice(name='3x2', value='RATIO_3X2')
    ])

@interactions.slash_option(name="description",
                           description="Enter image description",
                           required=True,
                           opt_type=interactions.OptionType.STRING)

async def image(ctx: interactions.SlashContext, style: str, ratio: str,
                description: str):
    await ctx.defer()
    filename = generate_image(style, ratio, description)
    await ctx.send(file=filename)


###########################################
# 4) "Coding-help" command
@interactions.slash_command(
    name="coding-help",
    description="I can help to answer any programming questions",
    scopes=[GUILD_ID])

@interactions.slash_option(name="programming_prompt",
                           description="Enter your programming prompt",
                           required=True,
                           opt_type=interactions.OptionType.STRING)

async def coding_help(ctx: interactions.SlashContext, programming_prompt: str):
    await ctx.defer()
    response_max_size = 1900
    response = generate_coding_response(programming_prompt)
    if len(response) <= response_max_size:
        await ctx.respond(response)
    else:
        response_chunks = response_split(response, response_max_size)
        for chunk in response_chunks:
            await ctx.respond(chunk)


###########################################
# 5) "help" command
@interactions.slash_command(name="help",
                            description="display help menu",
                            scopes=[GUILD_ID])

async def help(ctx: interactions.SlashContext):
    await ctx.respond(
        '''```Commands list:\n\n/ask - chats or answers any quesitons\n\n/tts-ask - same as /ask + text-to-speech ability\n\n/image - generates images of different styles and ratios\n\n/coding-help - answers any coding and programming questions\n\n/help - displays commands list\n```'''
    )

keep_alive()
bot.start(TOKEN)
