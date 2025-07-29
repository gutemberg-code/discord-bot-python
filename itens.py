import discord
import pyodbc
import os
from dotenv import load_dotenv
import time


load_dotenv()

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
print('---------------------------------')

while True:
    # Coleta de dados do usuário
    chave = int(input("Qual a chave do item? "))
    titulo = input("Qual o nome do item? ")
    descricao = input("O que o item é? Tem algo escrito nele? ")
    cor_r = int(input("Digite o valor de R (0-255): "))
    cor_g = int(input("Digite o valor de G (0-255): "))
    cor_b = int(input("Digite o valor de B (0-255): "))


    icon = input("O item vai ter um ícone? Mande a URL (ou deixe vazio): ")
    if icon.strip() == "":
        icon = None

    # Comando SQL com placeholders
    comando = """
        INSERT INTO itens 
        (chave, titulo, descricao, cor_r, cor_g, cor_b, thumbnail_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.execute(comando, (chave, titulo, descricao, cor_r, cor_g, cor_b, icon))
    conexao.commit()
    print("Item adicionado à tabela itens com sucesso!")
    print("-----------------------------------------------\n")
    time.sleep(2)
    os.system('cls')


