import os
import nextcord
import platform 
import configparser
from nextcord.ext import commands

contents = {}
joinnedUsers = []

class COLOR:
    BLUE = '\033[94m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    CHECK = '\033[92m✓ \033[0m'

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '\config.ini')

token = str(config['CREDENTIALS']['token'])
owner_id = str(config['CREDENTIALS']['owner_id'])

print(f'{COLOR.CHECK}Setting check.')

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix=' ', intents=intents, status='idle')

@client.event
async def on_ready():
    owner_name = await client.fetch_user(owner_id)
    print('--------------------------------------')
    print(f'Logged in as {COLOR.BLUE}{client.user.name}#{client.user.discriminator} {COLOR.RESET}({COLOR.BLUE}{client.user.id}{COLOR.RESET})')
    print(f"Owner: {COLOR.BLUE}{str(owner_name)[0:-2]}{COLOR.RESET} {COLOR.RESET}({COLOR.BLUE}{owner_id}{COLOR.RESET})")
    print(f'Currenly running nextcord {COLOR.BLUE}{nextcord.__version__}{COLOR.RESET} on python {COLOR.BLUE}{platform.python_version()}{COLOR.RESET}')
    print('--------------------------------------')

@client.slash_command(name="join", description="컨텐츠에 참여합니다.")
async def join(interaction: nextcord.Interaction,
               content_name: str = nextcord.SlashOption(
                    name = "content_name",
                    description="컨텐츠의 이름을 선택합니다.",
                    required=True),
               nickname: str = nextcord.SlashOption(
                    name = "nickname",
                    description="닉네임을 정합니다.",
                    required=True)
                ):
    if not (content_name in contents.keys()):
        embed = nextcord.Embed(title="없는 컨텐츠입니다. ❌", description="", color=0xff392b)
        await interaction.send(embed=embed, ephemeral=True)
        return;
    
    if nickname in contents[content_name]:
        embed = nextcord.Embed(title="이미 들어온 닉네임입니다. ❌", description="", color=0xff392b)
        await interaction.send(embed=embed, ephemeral=True)
        return;
    
    else:
        if interaction.user.id in joinnedUsers:
            embed = nextcord.Embed(title="이미 들어온 유저입니다. ❌", description="", color=0xff392b)
            await interaction.send(embed=embed, ephemeral=True)
            return;
        
        else:
            embed = nextcord.Embed(title="컨텐츠 가입을 성공하였습니다. ✅ " + nickname, description="", color=0x73ff40)
            await interaction.send(embed=embed, ephemeral=False)
            joinnedUsers.append(interaction.user.id)
            lst = list(contents[content_name])
            lst.append(nickname)
            contents[content_name] = lst
            
            print(f"{interaction.user.name}이 {nickname}(으)로 {content_name}에 로그인했습니다.")

@client.slash_command(name="create", description="컨텐츠를 만듭니다.")
async def create(interaction: nextcord.Interaction,
                 content_name: str = nextcord.SlashOption(
                    name = "content_name",
                    description="만들 컨텐츠의 이름을 정합니다.",
                    required=True)
                 ):
    if (interaction.user.guild_permissions.value == -1):
        embed = nextcord.Embed(title="컨텐츠 생성을 성공하였습니다. ✅ ", description=content_name, color=0x73ff40)
        embed.add_field(name="가입 방법", value=f"/join {content_name} [닉네임]을 명령어 채널에서 입력")
        await interaction.send(embed=embed, ephemeral=False)
        
        allowed_mentions = nextcord.AllowedMentions(everyone=True)
        
        await interaction.send("@everyone", allowed_mentions=allowed_mentions)
        
        contents[content_name] = []
    else:
        embed = nextcord.Embed(title="권한이 부족합니다. ❌", description="", color=0xff392b)
        await interaction.send(embed=embed, ephemeral=True)

@client.slash_command(name="stop", description="모집을 종료합니다.")
async def stop(interaction: nextcord.Interaction,
                content_name: str = nextcord.SlashOption(
                    name = "content_name",
                    description="모집을 종료할 컨텐츠의 이름을 선택합니다.",
                    required=True)
                ):
    if (interaction.user.guild_permissions.value == -1):
        if not (content_name in contents.keys()):
            embed = nextcord.Embed(title="없는 컨텐츠입니다. ❌", description="", color=0xff392b)
            await interaction.send(embed=embed, ephemeral=True)
            return;
        else:
            users = ""
            
            for i in range(len(contents[content_name])):
                users = users + contents[content_name][i] + "\n"
            
            embed = nextcord.Embed(title=str(content_name) + " 컨텐츠 모집을 종료합니다!", 
                                description="총 참여 인원 수 : " + str(len(contents[content_name])) + "\n```" + users + "```", 
                                color=0x73ff40)
            await interaction.send(embed=embed, ephemeral=False)
            
            del contents[content_name]
    else:
        embed = nextcord.Embed(title="권한이 부족합니다. ❌", description="", color=0xff392b)
        await interaction.send(embed=embed, ephemeral=True)
    
try:
    client.run(token)
except(nextcord.errors.LoginFailure):
    exit()
