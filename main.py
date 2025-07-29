import discord
from discord.ext import commands
import random
import re
import pyodbc
import asyncio
import os
from dotenv import load_dotenv 

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Conexão com o SQL Server
conexao = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-SUH4GRL;"
    "Database=PythonSQL;"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
    "TrustServerCertificate=yes;"
)

cursor = conexao.cursor()
print("Conexão estabelecida com sucesso!")

CantinhoGloob = int(os.getenv('ChatConversation'))
Dados = int(os.getenv('ChatDIce'))
SessaoRPG = int(os.getenv('ChatSession'))

# Classe personalizada para o bot com suporte a app_commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="g!", intents=intents)

@bot.event
async def on_ready():
    syncs = await bot.tree.sync()
    print(f"{len(syncs)} Comandos slash sincronizados!")
    print('Glóoby está vendo tudo... Sempre naquele cantinho.')

    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CantinhoGloob:
        mensagens = [
            "Eu vejo todos vocês, aventureiros inxeridos.",
            "calem a boca, Glóob merece sossego.",
            "Aqui não é casa de Mãe joana não, vaza.",
            "Vida de Glóob ser triste, não ter um minuto de paz.",
            "Glóob só quer um pouco de sossego, é pedir muito?",
            "Glóob não quer saber de aventuras, Glóob só quer descansar.",
            "Glóob não é um aventureiro, Glóob é um ser de paz.",
            "Glóob não pediu pra ser incomodado, só quer ficar na sombra quietinho.",
            "Glóob tá no modo avião da vida social, só aceitando chamadas do silêncio.",
            "Aqui é território proibido pra papo furado, só entra quem respeita o cochilo do Glóob.",
            "Glóob virou mestre em desaparecer, seu lugar favorito é a sombra do cantinho.",
            "Vida de Glóob: café forte, luz apagada e ninguém me perturbando.",
            "Se Glóob fosse planta, seria uma samambaia no porão, só pra evitar luz e gente.",
            "Glóob no canto, olhando o mundo com aquele olhar, sim, aquele olhar.",
            "Glóob sempre está no cantinho... Sim... eu vi tudo aquilo",
            "Glóob não é um aventureiro, Glóob é um observador silencioso.",
            "Glóob não precisa de espada, só de um bom lugar pra cochilar.",
        ]
        msg = random.choice(mensagens)
        await message.reply(msg)

    elif message.channel.id in [Dados, SessaoRPG]:
        dice = message.content.strip()
        match = re.fullmatch(r'(\d+)d(\d+)([+-]\d+)?', dice)
        if not match:
            return

        qtd_dados = int(match.group(1))
        faces_dado = int(match.group(2))
        modificador = int(match.group(3)) if match.group(3) else 0

        if '+' in dice:
            operador = 1
        elif '-' in dice:
            operador = 2
        else:
            operador = 0

        if qtd_dados <= 0 or faces_dado <= 0:
            await message.reply("Me tirou do meu cantinho para mandar essa merda? Ai, ai... Rolagem inválida.")
            return

        rolagens = [random.randint(1, faces_dado) for _ in range(qtd_dados)]
        total = sum(rolagens) + modificador

        comentario = "Glóob odeia barulho de dados rolando..."

        if total >= 40 and faces_dado != 100:
            comentario = "Pô chefia, prometo que não vai mais acontecer..."
        elif total >= 30 and faces_dado != 100:
            comentario = "Glóob... estava distraído!"
        elif total >= 20 and faces_dado != 100:
            comentario = "Glóob já viu melhores..."
        elif faces_dado == 20:
            if all(numero == 1 for numero in rolagens):
                comentario = "Glóob atingiu a gnose... Falhe miseravelmente aventureiro!"
            elif all(numero <= 10 for numero in rolagens):
                comentario = "Glóob atrapalhando os aventureiros de novo... Glóob merecer aumento!"
        elif faces_dado == 100 and modificador == 0 and qtd_dados == 1:
            await message.reply("Qual nível de dificuldade desejado? (exemplo: 1/4, 1/2, 1...)")
            def check(m):
                return m.author == message.author and m.channel == message.channel
            try:
                resposta = await bot.wait_for('message', timeout=45.0, check=check)
                nd_usuario = str(resposta.content.strip())
                roll = rolagens[0]
                recompensas_texto = []
                cursor.execute("""
                    SELECT dinheiro FROM recompensas
                    WHERE nd = ?
                     AND ? BETWEEN d_inicio_dinheiro AND d_fim_dinheiro
                """, (nd_usuario, roll))
                dinheiro_result = cursor.fetchone()

                cursor.execute("""
                    SELECT item FROM recompensas
                    WHERE nd = ?
                    AND ? BETWEEN d_inicio_item AND d_fim_item
                """, (nd_usuario, roll))
                item_result = cursor.fetchone()

                
                if dinheiro_result or item_result:
                    dinheiro = dinheiro_result[0] if dinheiro_result else "Nada"
                    item = item_result[0] if item_result else "Nada"
                    comentario = f"Glóób achou umas tralha ➞ Dinheiro: {dinheiro} | Item: {item}"
                else:
                    comentario = f"Glóob não achou nada... Manda o mestre arrumar isso aí"
    

            except asyncio.TimeoutError:
                comentario = "Tempo esgotado para resposta do nível de dificuldade."


        if operador == 1:
            descricao = f"```{total} ⟵ {rolagens}+{modificador}```"
        elif operador == 2:
            descricao = f"```{total} ⟵ {rolagens}{modificador}```"
        else:
            descricao = f"```{total} ⟵ {rolagens}```"

        embed = discord.Embed(
            description=descricao,
            color=discord.Color.dark_green()
        )
        embed.set_footer(text="{}".format(comentario))
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.tree.command()
async def item(interaction: discord.Interaction, chave: int):
    cursor.execute("""
        SELECT titulo, descricao, cor_r, cor_g, cor_b, thumbnail_url
        FROM itens WHERE chave = ?
    """, (chave,))
    resultado = cursor.fetchone()

    if resultado:
        titulo, descricao, cor_r, cor_g, cor_b, thumbnail_url = resultado
        if all(v is not None for v in [cor_r, cor_g, cor_b]):
            cor = discord.Color.from_rgb(cor_r, cor_g, cor_b)
        else:
            cor = discord.Color.default()   


        item_embed = discord.Embed(
            title=titulo,
            description=descricao,
            color=cor
        
        )

        if thumbnail_url:
            item_embed.set_thumbnail(url=thumbnail_url)

        await interaction.response.send_message(embed=item_embed)

    else:
        await interaction.response.send_message("Glóob não conhecer essa chave, vá encontrar o item do RPG!")


@bot.tree.command()
async def npcs(interaction: discord.Interaction, nome: str):
    cursor.execute("""
        SELECT author_npc, footer_npc, thumbnail_npc, colornpc_r, colornpc_g, colornpc_b
        FROM npcs WHERE author_npc = ?
    """, (nome,))
    resultadonpc = cursor.fetchone()    
    
    if resultadonpc:
        author_npc, footer_npc, thumbnail_npc, colornpc_r, colornpc_g, colornpc_b = resultadonpc
        if all(v is not None for v in [colornpc_r, colornpc_g, colornpc_b]):
            cor = discord.Color.from_rgb(colornpc_r, colornpc_g, colornpc_b)
        else:
            cor = discord.Color.default()   
            
        item_embed_npc = discord.Embed(
        color=cor,
        description=footer_npc
        )
        
        item_embed_npc.set_author(name=author_npc)    
        item_embed_npc.set_thumbnail(url=thumbnail_npc)

        if thumbnail_npc:
            item_embed_npc.set_thumbnail(url=thumbnail_npc)
        else:
            item_embed_npc.set_thumbnail(url=None)

        await interaction.response.send_message(embed=item_embed_npc)

    else:
        await interaction.response.send_message("Glóob não conhecer esse vagabundo, e olha que gloob conhece muitos vagabundos.")
                  
# Token
bot.run(token)




