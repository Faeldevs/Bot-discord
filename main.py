# main.py
import discord
from discord import app_commands
import os
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÃO INICIAL E CARREGAMENTO DAS VARIÁVEIS DE AMBIENTE ---
load_dotenv() # Carrega as variáveis do arquivo .env

# Carrega o token e o ID da guilda de forma segura do arquivo .env
TOKEN = os.getenv("DISCORD_TOKEN")
ID_DO_SERVIDOR = int(os.getenv("GUILD_ID"))

if not TOKEN or not ID_DO_SERVIDOR:
    print("ERRO: O Token do Discord ou o ID do Servidor não foram encontrados no arquivo .env")
    exit()

# --- 2. DEFINIÇÃO DA CLASSE DO CLIENTE (BOT) ---
class MeuBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # O 'tree' de comandos agora é um atributo da classe
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Bot {self.user} conectado e pronto!")
        # A sincronização agora é feita aqui, de forma mais limpa
        # e apenas para o servidor especificado.
        await self.tree.sync(guild=discord.Object(id=ID_DO_SERVIDOR))
        print("Comandos sincronizados com o servidor.")

# --- 3. INICIALIZAÇÃO DO BOT ---
# Define as "intenções" (permissões) básicas que o bot precisa
intents = discord.Intents.default()
bot = MeuBot(intents=intents)

# --- 4. DEFINIÇÃO DOS COMANDOS SLASH ---
# O decorador agora usa a 'tree' de dentro da instância do bot
@bot.tree.command(
    name='teste', 
    description='Testa se o bot está respondendo corretamente.'
)
async def comando_teste(interaction: discord.Interaction):
    """ Um comando de teste simples. """
    await interaction.response.send_message("Estou funcionando perfeitamente!", ephemeral=True)

# Exemplo de um novo comando com parâmetros para mostrar a capacidade de expansão
@bot.tree.command(
    name='ola',
    description='Mande um olá para um amigo.'
)
@app_commands.describe(usuario='O usuário para quem você quer dar oi')
async def comando_ola(interaction: discord.Interaction, usuario: discord.Member):
    """ Envia uma saudação para o membro mencionado. """
    await interaction.response.send_message(f"{interaction.user.mention} mandou um olá para {usuario.mention}!")

# --- 5. EXECUÇÃO DO BOT ---
# Usar 'if __name__ == "__main__":' é uma boa prática em Python
if __name__ == "__main__":
    bot.run(TOKEN)
