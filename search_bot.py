import discord
import json
from googleapiclient.discovery import build


client = discord.Client()

api_key = "AIzaSyDm0QmM0ehTKZ3a5blP7tdIHAfrY8nuMRs"
cse_id = "002090988512210948953:3llemhwwasw"

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    # msg = 'Hello {0.author.mention}'.format(message)
    if message.author == client.user:
        return

    if message.content.startswith('!nav'):
        searchparams = message.content[4:]

        if searchparams:
            results = google_search(searchparams, api_key, cse_id, num=2)

            for result in results:
                print(result)
                answer = 'Title: ' + result['title'] + '\n' +\
                          'Answer: ' + result['snippet'] + '\n' +\
                          'Source: ' + result['link']
                result_embed = create_embed(result['snippet'], result['link'])
                print(answer)

            await client.send_message(message.channel, embed=result_embed)

        else:
            msg = "Message is empty... try again."
            await client.send_message(message.channel, msg)


@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('------')

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    print(res)
    return res['items']

def create_embed(result, source):
    embed = discord.Embed(title = 'Search Bot', description="Here's what I found...", color=0x00ff00)
    embed.add_field(name="Result", value=result, inline=False)
    embed.add_field(name="Source:", value=source, inline=False)
    return embed

client.run('NjE0MDcyNjc4NDM3MDkzMzk2.XWJrwA.ErWq72ngZs2BZWT_ic8m_auulK4')
