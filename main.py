import json
import asyncio
import discord
from discord_components import *
from discord.ext import commands
import requests
import time

token = 'OTU1MDQ3NDAxMTU1MTAwNzEy.Yjb_NA.YjiawLFlVOFwFhFtu1FvmzU5gLo'

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():

    print("========== started ==========")

def send_api(channel_id, activity):  #디스코드 rest_api 호출
    url = f'https://discord.com/api/v8/channels/{channel_id}/invites'
    headers = {
        'Content-Type' : 'application/json; chearset=utf-8',
        'Authorization' : 'Bot OTU1MDQ3NDAxMTU1MTAwNzEy.Yjb_NA.YjiawLFlVOFwFhFtu1FvmzU5gLo' # 토큰을 봇 토큰으로 바꿔주세요
    }

    body = {
        'max_age' : 3600, # 초대 링크 유효 기간이에요. 3600초 = 1시간
        'max_uses' : 1,
        'target_application_id' : activity,
        'target_type' : 2,
        'temporary' : False,
        'validate' : None
    }

    data = json.dumps(body, ensure_ascii=False, indent="\t")
    response = requests.post(url, headers=headers, data=data)

    return response.text.split('code": "')[1].split('"')[0] # 워치투게더 참가에 필요한 코드를 리턴해줘요. https://discord.com/invite/코드 형식으로 초대 링크가 이루어져 있어요

@client.command(name='방해금지')
async def dnd(ctx):
    await client.change_presence(status=discord.Status.dnd)
    await ctx.send('봇 상태를 방해금지로 변경했습니다.')

@client.command(name='온라인')
async def online(ctx):
    await client.change_presence(status=discord.Status.online)
    await ctx.send('봇 상태를 온라인으로 변경했습니다.')

@client.command()
async def youtube(ctx): # !youtube 를 사용자가 입력할 때
    if ctx.author.voice is None: # 사용자가 음성채널에 들어가 있지 않을 때
        embed = discord.Embed(title='먼저 음성채널에 입장해주세요.')
        await ctx.reply(embed=embed)
    else:
        age_time = round(time.time()) + 3600 # 유효기간을 Unixtime으로 바꿔주는 코드에요.
        channel_id = ctx.author.voice.channel.id # 사용자가 들어가 있는 음성 채널의 아이디를 가져옵니다.
        code = send_api(channel_id, '880218394199220334') # 위에서 받아온 채널의 아이디를 위의 rest_api 에 넣어서 코드를 가져와요.
        link = f'https://discord.com/invite/{code}' # https://discord.com/invite/코드 초대 링크의 완성본이에요. 해당 링크를 디스코드에 보내기만 해도 watch_together을(를) 쓸 수 있어요.
        embed = discord.Embed(title=f"watch_together 엑티비티가 실행되었습니다", description=f"아래의 버튼을 눌러 참가해주세요.\n링크가 <t:{age_time}:R>에 만료됨.") # 안내메세지 embed 부분입니다. 링크만 딱 보내도 작동은 되지만.. 필요한 정보를 보여주는게 그래도 보기 좋잖아요?
        embed.add_field(name='채널:', value=ctx.author.voice.channel.name) # 위와 마찬가지
        embed.add_field(name='초대코드:', value=f'`{code}`') # 위와 마찬가지
        embed.set_footer(text=f'{ctx.author.name} 님이 시작함') # 위와 마찬가지
        button_ac_invite = Button(label='엑티비티 참가하기', style=ButtonStyle.URL, url=link) # 그냥 링크만 보내면 보기 조잡스러우니 링크가 포함된 버튼을 만들었어요.
        prm = await ctx.send(embed=embed, components=[button_ac_invite]) # 그리고 위에서 만든 embed와 버튼을 보내줍시다

        await asyncio.sleep(3600) # 링크의 유효기간(한 시간)이 끝나면
        embed = discord.Embed(title="만료된 엑티비티입니다.", description="실행을 원하신다면 다시 요청해주세요.") # 링크가 만료됐다는 embed와
        button_ac_invite = Button(label='엑티비티 참가하기', style=ButtonStyle.URL, url=link, disabled=True) # 위의 링크가 포함된 버튼을 비활성화 시켜줍니다.
        await prm.edit(embed=embed, components=[button_ac_invite])



client.run(token)

