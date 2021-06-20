import discord
import os
import requests
import json
from discord.ext import commands
from keep_alive import keep_alive

bot = commands.Bot(command_prefix = "?")
intents = discord.Intents(messages=True, guilds=True, typing = False, presences = False)
nuk = discord.Client(intents = intents)
print('Logging in...')

def get_facts():
  resp_00 = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
  json_data = json.loads(resp_00.text)
  fact = json_data['text']
  return (fact)

def get_meaning(inWord):
  resp_01 = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en_US/{}'.format(str(inWord)))
  json_data01 = json.loads(resp_01.text)

  mnin = "\n".join([f"{i} {inWord}:\n {meaning['definitions'][0]['definition']}\n" for i, meaning in enumerate(json_data01[0]["meanings"])])

  return f"```{mnin}```"
  # for meaning in json_data01[0]["meanings"]:
  #   defn = meaning["definitions"][0]["definition"]
  # return defn
@nuk.event
async def on_ready():
  print('Logged in as {0.user}'.format(nuk))

@bot.command()
async def m(ctx, *, wrd):
  await ctx.send(f'{wrd}')
  mng = get_meaning(wrd)
  await ctx.send(mng)


@nuk.event
async def on_message(message):
  if message.author == nuk.user:
    return

  if message.content == 'gimmehelp':
    await message.channel.send("""
    \n```
    **TypoBot Help**\ngimmegreet : greets you
    gimmefact  : random facts
    gimmehelp  : help```
    """)
  elif message.content.startswith('gimmegreet'):
    await message.channel.send('Hello {0.author}'.format(message))
  elif message.content.startswith('(╯°□°）╯︵ ┻━┻'):
    await message.channel.send('┬─┬ ノ( ゜-゜ノ)')
  elif message.content == 'gimmefact':
    fact = get_facts()
    await message.channel.send(fact)
  elif message.content.startswith('gd'):
    wrr = message.content.replace('gd ', '')
    fl_wrr = wrr.replace(' ', '%20')
    mnng = get_meaning(fl_wrr)
    await message.channel.send(mnng)

  

keep_alive()
nuk.run(os.environ['TOKEN'])