import discord
from discord.ext import commands
import pyodbc
import os
from dotenv import load_dotenv
import time

# Conexão com o SQL Server
conexao = pyodbc.connect(
    f"Driver={os.getenv('DB_DRIVER')};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
    f"Encrypt={os.getenv('DB_ENCRYPT')};"
    f"TrustServerCertificate={os.getenv('DB_TRUST_CERTIFICATE')};" 
)

cursor = conexao.cursor()
print("Conexão estabelecida com sucesso!")

while True:
    # Coleta de dados para o NPC
    author = input("Nome do autor do NPC: ")
    footer = input("Rodapé da embed do NPC: ")
    thumbnail = input("URL do thumbnail do NPC (ou deixe vazio): ").strip()
    if thumbnail == "":
        thumbnail = None

    print("Digite os valores RGB da cor da embed (ou deixe vazio para usar cor padrão do Discord).")
    entrada_r = input("R (0-255): ").strip()
    entrada_g = input("G (0-255): ").strip()
    entrada_b = input("B (0-255): ").strip()

    cor_r = int(entrada_r) if entrada_r != "" else None
    cor_g = int(entrada_g) if entrada_g != "" else None
    cor_b = int(entrada_b) if entrada_b != "" else None

    # Inserção no banco de dados
    comando = """
        INSERT INTO npcs (author_npc, footer_npc, thumbnail_npc, colornpc_r, colornpc_g, colornpc_b)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    cursor.execute(comando, (author, footer, thumbnail, cor_r, cor_g, cor_b))
    conexao.commit()

    print("NPC inserido com sucesso na tabela!\n")
    time.sleep(2)
    os.system('cls')

