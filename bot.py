import discord
from discord.ext import commands
from dotenv import load_dotenv
import os, NaaGPT
from keep_alive import keep_alive
import interactions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.members = True
bot = interactions.Client(activity=discord.Game("Generate Responses"), status=discord.Status.do_not_disturb)

@interactions.listen()
async def on_startup():
  print(f"Logged in as {bot.user}")


@bot.event()
async def on_ready():
  print("Im ready!")

async def remove_old_slash_commands():
    try:
        await bot.synchronize_interactions(scopes=[1098675990806417518], delete_commands=True)
        print("Old slash commands removed successfully.")
    except discord.HTTPException as e:
        print(f"Failed to remove old slash commands: {e}")
      
def generate_response(prompt):
  response = NaaGPT.generate_response(prompt)
  return response

def generate_coding_response(prompt):
  response = NaaGPT.phind_message_response(prompt)
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
  
# 3) "ask" command
@interactions.slash_command(
    name="ask",
    description="Answer a prompt",
    scopes=[1098675990806417518]
)

@interactions.slash_option(
    name="prompt",
    description="Enter a prompt", 
    required=True, 
    opt_type=interactions.OptionType.STRING
)

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

# 2) "image" command
@interactions.slash_command(
    name="image",
    description="Enter image description",
    scopes=[1098675990806417518]
)

@interactions.slash_option(
    name="style",
    description="Enter image style", 
    required=True, 
    opt_type=interactions.OptionType.STRING,
    choices=[
      interactions.SlashCommandChoice(name='Imagine V4 Beta', value='IMAGINE_V4_Beta'),
      interactions.SlashCommandChoice(name='Realistic', value='REALISTIC'),
      interactions.SlashCommandChoice(name='Anime', value='ANIME_V2'),
      interactions.SlashCommandChoice(name='Disney', value='DISNEY'),
      interactions.SlashCommandChoice(name='Studio Ghibli', value='STUDIO_GHIBLI'),
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
      interactions.SlashCommandChoice(name='Imagine V4 creative', value='V4_CREATIVE'),
      interactions.SlashCommandChoice(name='Imagine V3', value='IMAGINE_V3'),
      interactions.SlashCommandChoice(name='Cosmic', value='COMIC_V2'),
      interactions.SlashCommandChoice(name='Logo', value='LOGO'),
      interactions.SlashCommandChoice(name='Pixel art', value='PIXEL_ART'),
      interactions.SlashCommandChoice(name='Interior', value='INTERIOR'),
      interactions.SlashCommandChoice(name='Mystical', value='MYSTICAL'),
      interactions.SlashCommandChoice(name='Super realism', value='SURREALISM'),
      interactions.SlashCommandChoice(name='Minecraft', value='MINECRAFT'),
      interactions.SlashCommandChoice(name='Dystopian', value='DYSTOPIAN')
    ]
)

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
    ]
)

@interactions.slash_option(
    name="description",
    description="Enter image description", 
    required=True, 
    opt_type=interactions.OptionType.STRING
)

async def image(ctx: interactions.SlashContext, style: str, ratio: str, description: str):
    await ctx.defer()
    filename = generate_image(style, ratio, description)
    await ctx.send(file=filename)

# 3) "Coding-help" command
@interactions.slash_command(
    name="coding-help",
    description="programming help desk",
    scopes=[1098675990806417518]
)

@interactions.slash_option(
    name="programming_prompt",
    description="Enter a programming prompt", 
    required=True, 
    opt_type=interactions.OptionType.STRING
)

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
        
keep_alive()
bot.start(TOKEN)