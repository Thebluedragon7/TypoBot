import discord
import os
import requests
import json
from discord.ext import commands
from keep_alive import keep_alive
import praw



intents = discord.Intents(messages=True, guilds=True, typing = False, presences = False, members = True)
nuk = commands.Bot(command_prefix='.',case_insensitive=True, intents = intents)
print('Logging in...')

def get_facts():
  resp_00 = requests.get('https://uselessfacts.jsph.pl/random.json?language=en')
  json_data = json.loads(resp_00.text)
  fact = json_data['text']
  return (f'> {fact}')

def typohelp():
  return """
    >>> **__𝕋𝕪𝕡𝕠𝔹𝕠𝕥 ℍ𝕖𝕝𝕡__**```
  𝐁𝐚𝐬𝐢𝐜 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬
    gimmehelp  : help
    gimmegreet : greets you
  𝐆𝐞𝐧𝐞𝐫𝐚𝐥 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬
    gimmefact  : random facts
    gimmememe  : random memes
  𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬
    gd <word> : meaning of word (Dictionary)
    red : subreddit```
    """

def get_meaning(inWord):
  resp_01 = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en_US/{}'.format(str(inWord)))
  data01 = resp_01.json()
  defns = [
    meaning['definitions'][0]['definition']
    for meaning in data01[0]['meanings']
  ]
  if len(defns) == 1:
    return f">>> **__𝕋𝕪𝕡𝕠𝔹𝕠𝕥 𝔻𝕚𝕔𝕥𝕚𝕠𝕟𝕒𝕣𝕪__**\n\n**{inWord}**:\n _{defns[0]}_"
  
  mnin = '\n'.join([
        f'{i + 1} **{inWord}**:\n _{definition}_'
        for i, definition
        in enumerate(defns)
    ])
  return f">>> **__𝕋𝕪𝕡𝕠𝔹𝕠𝕥 𝔻𝕚𝕔𝕥𝕚𝕠𝕟𝕒𝕣𝕪__**\n\n{mnin}"

def red_get():
  reddit = praw.Reddit(client_id="9F7ooKfQmGGasg", client_secret="MOu78eIT5ly42iyHAms3s4UddlIfUg",user_agent="PythonCoder123333")
  submission = reddit.subreddit("CuteTraps").random()
  return submission.url



@nuk.event
async def on_ready():
  print('Logged in as {0.user}'.format(nuk))

@nuk.command()
async def mn(ctx, *, wrd):
  gword = wrd
  await ctx.wrd.delete()
  await ctx.send(gword)
  mng = get_meaning(gword)
  await ctx.send(mng)


@nuk.event
async def on_message(message):
  if message.author == nuk.user:
    return

  if message.content == 'gimmehelp':
    await message.channel.send(typohelp())
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
  elif message.content == 'red':
    red_sub = red_get()
    await message.channel.send(red_sub)

# @nuk.command()
# async def ct(self, ctx):
#   reddit = praw.Reddit(client_id="9F7ooKfQmGGasg", client_secret="MOu78eIT5ly42iyHAms3s4UddlIfUg",user_agent="PythonCoder123333")
#   submission = reddit.subreddit("CuteTraps").random()
#   await ctx.send(submission.url)


keep_alive()
nuk.run(os.environ['TOKEN'])