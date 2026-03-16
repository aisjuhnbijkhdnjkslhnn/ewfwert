# ╔════════════════════════════════════════════════════════════════╗
# ║   ULTRA MEGA PACOTE FINAL - PARTE 1 (COLOQUE PRIMEIRO)        ║
# ╚════════════════════════════════════════════════════════════════╝

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
import random

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ═══════════════════════════════════════════════════════════════════
# BANCO DE DADOS
# ═══════════════════════════════════════════════════════════════════

class DB:
    def __init__(self):
        self.db = 'governo_br.db'
        self.criar_tabelas()

    def conexao(self):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        return conn

    def criar_tabelas(self):
        conn = self.conexao()
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS personagens (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, nome TEXT, data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ativo BOOLEAN DEFAULT 1)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS filiacao (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, partido TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS prestige (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, pontos INTEGER DEFAULT 0, nivel TEXT DEFAULT 'Ativista')''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS aprovacao (id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE, taxa REAL DEFAULT 50.0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS cargos (id INTEGER PRIMARY KEY, user_id INTEGER, cargo TEXT, tipo TEXT, ativo BOOLEAN DEFAULT 1)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS eleicoes (id INTEGER PRIMARY KEY, cargo TEXT, candidato_id INTEGER, votos INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS leis (id INTEGER PRIMARY KEY, autor_id INTEGER, titulo TEXT, status TEXT DEFAULT 'discussao', votos_favor INTEGER DEFAULT 0, votos_contra INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS crises (id INTEGER PRIMARY KEY, servidor_id INTEGER, titulo TEXT, descricao TEXT, impacto REAL, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ativa BOOLEAN DEFAULT 1)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tweets (id INTEGER PRIMARY KEY, autor_id INTEGER, conteudo TEXT, likes INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS trending (id INTEGER PRIMARY KEY, hashtag TEXT UNIQUE, mencoes INTEGER DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS casamento (id INTEGER PRIMARY KEY, politico1_id INTEGER, politico2_id INTEGER, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS filhos (id INTEGER PRIMARY KEY, pai_id INTEGER, mae_id INTEGER, nome TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS morte (id INTEGER PRIMARY KEY, politico_id INTEGER, causa TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, funeral BOOLEAN DEFAULT 0)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS fake_news (id INTEGER PRIMARY KEY, criador_id INTEGER, noticia TEXT, viral INTEGER DEFAULT 0, descoberta BOOLEAN DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS escandalo (id INTEGER PRIMARY KEY, alvo_id INTEGER, tipo TEXT, descricao TEXT, views INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS debate (id INTEGER PRIMARY KEY, cand1_id INTEGER, cand2_id INTEGER, tema TEXT, vencedor_id INTEGER, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS revolucao (id INTEGER PRIMARY KEY, servidor_id INTEGER, lider_id INTEGER, motivo TEXT, raiva_povo REAL DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ativa BOOLEAN DEFAULT 1)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS livros (id INTEGER PRIMARY KEY, autor_id INTEGER, titulo TEXT, conteudo TEXT, vendas INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS palestras (id INTEGER PRIMARY KEY, palestrante_id INTEGER, tema TEXT, audiencia INTEGER DEFAULT 0, cache INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS noticias_ia (id INTEGER PRIMARY KEY, manchete TEXT, conteudo TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS analise_ia (id INTEGER PRIMARY KEY, analise TEXT, tendencia TEXT, predicao TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

        conn.commit()
        conn.close()

    def obter_personagem(self, user_id):
        conn = self.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM personagens WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def criar_personagem(self, user_id, nome):
        conn = self.conexao()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO personagens (user_id, nome) VALUES (?, ?)', (user_id, nome))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def obter_prestige(self, user_id):
        conn = self.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM prestige WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute('INSERT INTO prestige (user_id) VALUES (?)', (user_id,))
            conn.commit()
            cursor.execute('SELECT * FROM prestige WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
        conn.close()
        return result

    def adicionar_prestige(self, user_id, pontos):
        conn = self.conexao()
        cursor = conn.cursor()
        self.obter_prestige(user_id)
        cursor.execute('UPDATE prestige SET pontos = pontos + ? WHERE user_id = ?', (pontos, user_id))
        conn.commit()
        conn.close()

    def obter_aprovacao(self, servidor_id):
        conn = self.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM aprovacao WHERE servidor_id = ?', (servidor_id,))
        result = cursor.fetchone()
        if not result:
            cursor.execute('INSERT INTO aprovacao (servidor_id) VALUES (?)', (servidor_id,))
            conn.commit()
            cursor.execute('SELECT * FROM aprovacao WHERE servidor_id = ?', (servidor_id,))
            result = cursor.fetchone()
        conn.close()
        return result

    def alterar_aprovacao(self, servidor_id, delta):
        conn = self.conexao()
        cursor = conn.cursor()
        self.obter_aprovacao(servidor_id)
        cursor.execute('UPDATE aprovacao SET taxa = MIN(100, MAX(0, taxa + ?)) WHERE servidor_id = ?', (delta, servidor_id))
        conn.commit()
        conn.close()

    def obter_filiacao(self, user_id):
        conn = self.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM filiacao WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def filiar_partido(self, user_id, partido):
        conn = self.conexao()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT OR REPLACE INTO filiacao (user_id, partido) VALUES (?, ?)', (user_id, partido))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

db = DB()

# ═══════════════════════════════════════════════════════════════════
# IA AUTOMÁTICA
# ═══════════════════════════════════════════════════════════════════

class IA:
    @staticmethod
    def gerar_manchete():
        verbos = ['ESCÂNDALO', 'CRISE', 'REVELAÇÃO', 'BOMBA', 'CHOQUE']
        temas = ['ministro', 'presidente', 'congresso', 'economia', 'política']
        return f"{random.choice(verbos)}: {random.choice(temas).upper()} em caos!"

    @staticmethod
    def gerar_analise():
        analises = [
            "Cenário político TENSO! Governo em risco extremo.",
            "APROVAÇÃO cai dramaticamente!",
            "COLIGAÇÃO ameaça quebrar!",
            "STF ameaça INTERVIR na política!",
            "OPOSIÇÃO ganha força massiva!"
        ]
        return random.choice(analises)

    @staticmethod
    def gerar_tendencia():
        return random.choice([
            "📈 Aprovação cresce (+5%)",
            "📉 Influência cai (-3%)",
            "🔴 Risco político muito alto",
            "🟢 Estabilidade retorna",
            "⚠️ Crise iminente",
            "✨ Novo líder emerge",
            "💥 Drama político aumenta"
        ])

    @staticmethod
    def gerar_predicao():
        return random.choice([
            "PRÓXIMOS DIAS: Revelação de corrupção",
            "PRÓXIMAS SEMANAS: Eleição interna divisiva",
            "MÊS QUE VEM: Crise econômica",
            "CURTO PRAZO: Coligação pode quebrar",
            "RISCO IMINENTE: Golpe não é impossível"
        ])

    @staticmethod
    def gerar_quote():
        quotes = [
            "A democracia é imperfeita, mas é o melhor sistema que temos.",
            "O poder não muda um homem, revela quem ele realmente é.",
            "A coragem política é mais rara que a coragem militar.",
            "Um país que não protege sua democracia merece perder.",
            "A história julga os governantes por seus atos, não palavras."
        ]
        return random.choice(quotes)

# ═══════════════════════════════════════════════════════════════════
# TASKS AUTOMÁTICAS
# ═══════════════════════════════════════════════════════════════════

@tasks.loop(hours=24)
async def gerar_boletim_diario():
    try:
        manchete = IA.gerar_manchete()
        analise = IA.gerar_analise()
        tendencia = IA.gerar_tendencia()
        predicao = IA.gerar_predicao()

        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO noticias_ia (manchete, conteudo) VALUES (?, ?)', (manchete, f"{analise}\n{tendencia}\n{predicao}"))
        conn.commit()
        conn.close()
        print("✅ Boletim diário gerado!")
    except Exception as e:
        print(f"❌ Erro: {e}")

@gerar_boletim_diario.before_loop
async def before_boletim():
    await bot.wait_until_ready()

@tasks.loop(hours=6)
async def atualizar_trends():
    try:
        hashtags = ['#PoliticaBrasil', '#Governo', '#Eleições', '#Congresso', '#Democracia', '#Reforma', '#Justiça']
        conn = db.conexao()
        cursor = conn.cursor()
        for hashtag in hashtags:
            mencoes = random.randint(1000, 100000)
            cursor.execute('INSERT OR REPLACE INTO trending (hashtag, mencoes) VALUES (?, ?)', (hashtag, mencoes))
        conn.commit()
        conn.close()
        print("✅ Trends atualizados!")
    except Exception as e:
        print(f"❌ Erro: {e}")

@atualizar_trends.before_loop
async def before_trends():
    await bot.wait_until_ready()

# ═══════════════════════════════════════════════════════════════════
# EVENTO - BOT PRONTO
# ═══════════════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    print(f'\n{"="*100}')
    print(f'  🇧🇷 ULTRA MEGA PACOTE - BOT CONECTADO!')
    print(f'  {bot.user} pronto para rodar!')
    print(f'  250+ Comandos | 80+ Tabelas | IA Automática')
    print(f'  Twitter Político | Filhos & Herança | Morte & Legado')
    print(f'  Fake News | Escândalos Virais | Debates Presidenciais')
    print(f'{"="*100}\n')
    
    if not gerar_boletim_diario.is_running():
        gerar_boletim_diario.start()
    if not atualizar_trends.is_running():
        atualizar_trends.start()
    
    await bot.change_presence(activity=discord.Game(name="ULTRA MEGA | !megaSistema"))
    # ═══════════════════════════════════════════════════════════════════
# COMANDOS - BÁSICOS
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='criar', help='Cria seu personagem')
async def criar_personagem_cmd(ctx, *, nome: str):
    try:
        if db.criar_personagem(ctx.author.id, nome):
            embed = discord.Embed(title="✅ PERSONAGEM CRIADO", description=f"**{nome}** entrou na política!", color=discord.Color.green())
            embed.add_field(name="👤 Nome", value=nome, inline=True)
            embed.add_field(name="👤 Discord", value=ctx.author.mention, inline=True)
            db.adicionar_prestige(ctx.author.id, 100)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Você já tem um personagem!")
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='filiar', help='Filiar a um partido')
async def filiar_cmd(ctx, *, partido: str):
    try:
        if db.filiar_partido(ctx.author.id, partido):
            db.adicionar_prestige(ctx.author.id, 50)
            embed = discord.Embed(title="✅ FILIADO", description=f"Você se filiou ao **{partido}**", color=discord.Color.green())
            embed.add_field(name="🎯 Partido", value=partido, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Erro ao filiar!")
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='meuPrestige', help='Ver seu prestige')
async def meu_prestige(ctx):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        embed = discord.Embed(title="⭐ MEU PRESTIGE", color=discord.Color.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed.add_field(name="⭐ Pontos", value=prestige['pontos'], inline=True)
        embed.add_field(name="📊 Nível", value=prestige['nivel'], inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='aprovacao', help='Ver aprovação do governo')
async def aprovacao_cmd(ctx):
    try:
        aprovacao = db.obter_aprovacao(ctx.guild.id)
        barra = "█" * int(aprovacao['taxa'] / 5) + "░" * (20 - int(aprovacao['taxa'] / 5))
        embed = discord.Embed(title="📊 APROVAÇÃO DO GOVERNO", color=discord.Color.gold())
        embed.add_field(name="Aprovação", value=f"{barra}\n{aprovacao['taxa']:.1f}%", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='noticias', help='Ver notícias geradas por IA')
async def noticias_cmd(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM noticias_ia ORDER BY rowid DESC LIMIT 3')
        noticias = cursor.fetchall()
        conn.close()
        
        if not noticias:
            await ctx.send("❌ Nenhuma notícia gerada ainda")
            return
        
        embed = discord.Embed(title="📰 NOTÍCIAS GERADAS POR IA", color=discord.Color.blue())
        for noticia in noticias:
            embed.add_field(name=f"📰 {noticia['manchete']}", value=noticia['conteudo'][:300], inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='trending', help='Ver trending topics')
async def trending_cmd(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM trending ORDER BY mencoes DESC LIMIT 10')
        trends = cursor.fetchall()
        conn.close()
        
        if not trends:
            await ctx.send("❌ Nenhum trending topic")
            return
        
        embed = discord.Embed(title="🔥 TRENDING TOPICS", color=discord.Color.orange())
        for i, trend in enumerate(trends, 1):
            medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            embed.add_field(name=f"{medalha} {trend['hashtag']}", value=f"{trend['mencoes']:,} menções", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='tweetar', help='Postar um tweet')
async def tweetar_cmd(ctx, *, conteudo: str):
    try:
        if len(conteudo) > 280:
            await ctx.send("❌ Tweet muito longo! Máximo 280 caracteres")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tweets (autor_id, conteudo) VALUES (?, ?)', (ctx.author.id, conteudo))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="📱 NOVO TWEET", description=conteudo, color=discord.Color.blue())
        embed.add_field(name="👤 Autor", value=ctx.author.name, inline=True)
        embed.add_field(name="❤️ Likes", value="0", inline=True)
        db.adicionar_prestige(ctx.author.id, 5)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='casar', help='Casar dois políticos')
async def casar_cmd(ctx, politico1: discord.User, politico2: discord.User):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO casamento (politico1_id, politico2_id) VALUES (?, ?)', (politico1.id, politico2.id))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="💒 CASAMENTO POLÍTICO", description="Dois corações se unem pela política!", color=discord.Color.magenta())
        embed.add_field(name="💑 Noivos", value=f"{politico1.mention} 💒 {politico2.mention}", inline=False)
        embed.add_field(name="📅 Data", value=datetime.now().strftime('%d/%m/%Y'), inline=False)
        db.adicionar_prestige(politico1.id, 50)
        db.adicionar_prestige(politico2.id, 50)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='filho', help='Registrar nascimento de filho')
async def filho_cmd(ctx, pai: discord.User, mae: discord.User, *, nome: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO filhos (pai_id, mae_id, nome) VALUES (?, ?, ?)', (pai.id, mae.id, nome))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="👶 NASCIMENTO POLÍTICO", description=f"Bem-vindo(a), **{nome}**!", color=discord.Color.green())
        embed.add_field(name="👨 Pai", value=pai.mention, inline=True)
        embed.add_field(name="👩 Mãe", value=mae.mention, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='morte', help='Registrar morte de político (Admin)')
@commands.has_permissions(administrator=True)
async def morte_cmd(ctx, politico: discord.User, *, causa: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO morte (politico_id, causa, funeral) VALUES (?, ?, 1)', (politico.id, causa))
        conn.commit()
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, -10)
        embed = discord.Embed(title="🕊️ FALECIMENTO", description=f"A nação chora a partida de **{politico.name}**", color=discord.Color.dark_grey())
        embed.add_field(name="👤 Falecido", value=politico.mention, inline=True)
        embed.add_field(name="⚰️ Causa", value=causa, inline=True)
        embed.add_field(name="🏛️ Funeral", value="Estado", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='fakenews', help='Criar fake news')
async def fake_news_cmd(ctx, *, noticia: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 300:
            await ctx.send("❌ Você precisa de 300+ prestige para criar fake news!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        viral = random.randint(1000, 50000)
        cursor.execute('INSERT INTO fake_news (criador_id, noticia, viral) VALUES (?, ?, ?)', (ctx.author.id, noticia, viral))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, -50)
        db.alterar_aprovacao(ctx.guild.id, -5)
        embed = discord.Embed(title="📰 FAKE NEWS CRIADA", description=noticia, color=discord.Color.red())
        embed.add_field(name="👤 Criador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📊 Viralidade", value=f"{viral:,}", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='escandalo', help='Criar escândalo viral')
async def escandalo_cmd(ctx, alvo: discord.User, tipo: str, *, descricao: str):
    try:
        tipos_validos = ['video', 'audio', 'foto', 'meme']
        if tipo.lower() not in tipos_validos:
            await ctx.send(f"❌ Tipo inválido! Use: {', '.join(tipos_validos)}")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        views = random.randint(100000, 10000000)
        cursor.execute('INSERT INTO escandalo (alvo_id, tipo, descricao, views) VALUES (?, ?, ?, ?)', (alvo.id, tipo.lower(), descricao, views))
        conn.commit()
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, -15)
        embed = discord.Embed(title="💥 ESCÂNDALO VIRAL", description=f"**{alvo.name}** está em ESCÂNDALO!", color=discord.Color.red())
        embed.add_field(name="📹 Tipo", value=tipo.upper(), inline=True)
        embed.add_field(name="👀 Views", value=f"{views:,}", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='debate', help='Criar debate presidencial')
async def debate_cmd(ctx, cand1: discord.User, cand2: discord.User, *, tema: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO debate (cand1_id, cand2_id, tema) VALUES (?, ?, ?)', (cand1.id, cand2.id, tema))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="🎤 DEBATE PRESIDENCIAL", description=tema, color=discord.Color.blue())
        embed.add_field(name="🎤 Candidato 1", value=cand1.mention, inline=True)
        embed.add_field(name="🎤 Candidato 2", value=cand2.mention, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='livro', help='Escrever livro de memórias')
async def livro_cmd(ctx, *, info: str):
    try:
        partes = info.split('|')
        if len(partes) < 2:
            await ctx.send("❌ Formato: `!livro Título | Conteúdo`")
            return
        
        titulo = partes[0].strip()
        conteudo = partes[1].strip()
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livros (autor_id, titulo, conteudo) VALUES (?, ?, ?)', (ctx.author.id, titulo, conteudo))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, 100)
        embed = discord.Embed(title="📚 LIVRO PUBLICADO", description=f"**{titulo}**", color=discord.Color.blue())
        embed.add_field(name="👤 Autor", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='palestra', help='Fazer uma palestra política')
async def palestra_cmd(ctx, audiencia: int, *, tema: str):
    try:
        cache = audiencia * 100
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO palestras (palestrante_id, tema, audiencia, cache) VALUES (?, ?, ?, ?)', (ctx.author.id, tema, audiencia, cache))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, 50)
        embed = discord.Embed(title="🎤 PALESTRA REALIZADA", description=tema, color=discord.Color.green())
        embed.add_field(name="👤 Palestrante", value=ctx.author.mention, inline=True)
        embed.add_field(name="👥 Audiência", value=f"{audiencia:,} pessoas", inline=True)
        embed.add_field(name="💰 Cachê", value=f"R$ {cache:,}", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='megaSistema', help='Info do ULTRA MEGA SISTEMA')
async def mega_sistema_cmd(ctx):
    try:
        embed = discord.Embed(title="🇧🇷 ULTRA MEGA PACOTE FINAL DEFINITIVO", description="O Sistema de Governo RP Mais Completo do Discord", color=discord.Color.gold())
        embed.add_field(name="✅ IMPLEMENTADO", value="250+ COMANDOS\n80+ TABELAS\n✅ IA Automática\n✅ Twitter Político\n✅ Filhos & Herança\n✅ Morte & Legado\n✅ Fake News\n✅ Escândalos Virais\n✅ Debates Presidenciais\n✅ Livros & Palestras\n+ 200 comandos épicos!", inline=False)
        embed.set_footer(text="🇧🇷 O SISTEMA MAIS ÉPICO DO DISCORD!")
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='ajuda', help='Ver comandos disponíveis')
async def ajuda_cmd(ctx):
    try:
        embed = discord.Embed(title="📖 AJUDA - ULTRA MEGA PACOTE", description="Sistema Completo de Governo RP Brasil", color=discord.Color.gold())
        embed.add_field(name="🚀 COMEÇAR", value="`!criar [nome]` - Criar personagem\n`!filiar [partido]` - Filiar\n`!megaSistema` - Info completa", inline=False)
        embed.add_field(name="📊 INFO", value="`!meuPrestige` - Seu prestige\n`!aprovacao` - Aprovação\n`!noticias` - Notícias IA\n`!trending` - Trends", inline=False)
        embed.add_field(name="📱 TWITTER", value="`!tweetar [texto]` - Postar tweet\n`!trending` - Ver trends", inline=False)
        embed.add_field(name="💒 FAMÍLIA", value="`!casar [@user1] [@user2]` - Casar\n`!filho [@pai] [@mae] [nome]` - Filho\n`!morte [@user] [causa]` - Morte", inline=False)
        embed.add_field(name="💥 DRAMA", value="`!fakenews [notícia]` - Fake news\n`!escandalo [@user] [tipo] [desc]` - Escândalo\n`!debate [@cand1] [@cand2] [tema]` - Debate", inline=False)
        embed.add_field(name="📚 LEGADO", value="`!livro [Título] | [Conteúdo]` - Livro\n`!palestra [audiência] [tema]` - Palestra", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# RODAR BOT
# ═══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    TOKEN = os.getenv('TOKEN')
    if not TOKEN:
        print("❌ TOKEN não encontrado em .env!")
    else:
        print("🚀 INICIANDO ULTRA MEGA PACOTE...")
        bot.run(TOKEN)
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - CPI E INVESTIGAÇÕES
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='abrirCPI', help='Abre uma CPI (Admin)')
@commands.has_permissions(administrator=True)
async def abrir_cpi(ctx, investigado: discord.User, *, titulo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cpi (
            id INTEGER PRIMARY KEY, titulo TEXT, investigado_id INTEGER, 
            presidente_id INTEGER, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ativa BOOLEAN DEFAULT 1
        )''')
        cursor.execute('INSERT INTO cpi (titulo, investigado_id, presidente_id) VALUES (?, ?, ?)', 
                      (titulo, investigado.id, ctx.author.id))
        conn.commit()
        cpi_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="⚖️ CPI ABERTA", description=titulo, color=discord.Color.red())
        embed.add_field(name="🎯 Investigado", value=investigado.mention, inline=True)
        embed.add_field(name="👤 Presidente", value=ctx.author.mention, inline=True)
        embed.add_field(name="ID", value=cpi_id, inline=True)
        db.alterar_aprovacao(ctx.guild.id, -20)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='depor', help='Depõe em uma CPI')
async def depor_cpi(ctx, cpi_id: int, *, depoimento: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS depoimentos_cpi (
            id INTEGER PRIMARY KEY, cpi_id INTEGER, depoente_id INTEGER, 
            conteudo TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO depoimentos_cpi (cpi_id, depoente_id, conteudo) VALUES (?, ?, ?)', 
                      (cpi_id, ctx.author.id, depoimento))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="✅ DEPOIMENTO REGISTRADO", description=f"CPI #{cpi_id}", color=discord.Color.green())
        embed.add_field(name="👤 Depoente", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Depoimento", value=depoimento[:200], inline=False)
        db.adicionar_prestige(ctx.author.id, 50)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - ELEIÇÃO COM 2 TURNOS
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='abrirEleicao2T', help='Abre eleição 2 turnos (Admin)')
@commands.has_permissions(administrator=True)
async def abrir_eleicao_2t(ctx, cargo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS eleicoes_2t (
            id INTEGER PRIMARY KEY, cargo TEXT, turno INTEGER, 
            status TEXT DEFAULT 'aberta', data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO eleicoes_2t (cargo, turno) VALUES (?, 1)', (cargo,))
        conn.commit()
        eleicao_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="🗳️ ELEIÇÃO ABERTA - PRIMEIRO TURNO", description=f"Cargo: **{cargo.upper()}**", color=discord.Color.blue())
        embed.add_field(name="🗳️ Tipo", value="Primeiro turno", inline=True)
        embed.add_field(name="ID", value=eleicao_id, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='votar2T', help='Vota em eleição 2 turnos')
async def votar_2t(ctx, eleicao_id: int, candidato: discord.User):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS votos_2t (
            id INTEGER PRIMARY KEY, eleicao_id INTEGER, votante_id INTEGER, 
            candidato_id INTEGER, UNIQUE(eleicao_id, votante_id)
        )''')
        try:
            cursor.execute('INSERT INTO votos_2t (eleicao_id, votante_id, candidato_id) VALUES (?, ?, ?)', 
                          (eleicao_id, ctx.author.id, candidato.id))
            conn.commit()
            
            embed = discord.Embed(title="✅ VOTO REGISTRADO", description=f"Eleição #{eleicao_id}", color=discord.Color.green())
            embed.add_field(name="🗳️ Voto em", value=candidato.mention, inline=False)
            db.adicionar_prestige(ctx.author.id, 10)
            await ctx.send(embed=embed)
        except:
            await ctx.send("❌ Você já votou nesta eleição!")
        conn.close()
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - PODER POLÍTICO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='poder', help='Mostra seu poder político')
async def meu_poder(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS poder_politico (
            id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, 
            poder_executivo REAL DEFAULT 0, poder_legislativo REAL DEFAULT 0,
            poder_judicial REAL DEFAULT 0, poder_mediatico REAL DEFAULT 0,
            poder_militar REAL DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM poder_politico WHERE user_id = ?', (ctx.author.id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            cursor.execute('INSERT INTO poder_politico (user_id) VALUES (?)', (ctx.author.id,))
            conn.commit()
            cursor.execute('SELECT * FROM poder_politico WHERE user_id = ?', (ctx.author.id,))
            resultado = cursor.fetchone()
        
        conn.close()
        
        exec_bar = "█" * int(resultado['poder_executivo'] / 10) + "░" * (10 - int(resultado['poder_executivo'] / 10))
        leg_bar = "█" * int(resultado['poder_legislativo'] / 10) + "░" * (10 - int(resultado['poder_legislativo'] / 10))
        jud_bar = "█" * int(resultado['poder_judicial'] / 10) + "░" * (10 - int(resultado['poder_judicial'] / 10))
        med_bar = "█" * int(resultado['poder_mediatico'] / 10) + "░" * (10 - int(resultado['poder_mediatico'] / 10))
        mil_bar = "█" * int(resultado['poder_militar'] / 10) + "░" * (10 - int(resultado['poder_militar'] / 10))
        
        embed = discord.Embed(title="💪 MEU PODER POLÍTICO", color=discord.Color.purple())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed.add_field(name="📊 PODER", value=f"Executivo:    {exec_bar} {resultado['poder_executivo']:.0f}%\nLegislativo:  {leg_bar} {resultado['poder_legislativo']:.0f}%\nJudicial:     {jud_bar} {resultado['poder_judicial']:.0f}%\nMidiático:    {med_bar} {resultado['poder_mediatico']:.0f}%\nMilitar:      {mil_bar} {resultado['poder_militar']:.0f}%", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - CARISMA
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='meuCarisma', help='Mostra seu carisma')
async def meu_carisma(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS carisma (
            id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, 
            carisma INTEGER DEFAULT 50, popularidade INTEGER DEFAULT 50,
            fandom INTEGER DEFAULT 0, haters INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM carisma WHERE user_id = ?', (ctx.author.id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            cursor.execute('INSERT INTO carisma (user_id) VALUES (?)', (ctx.author.id,))
            conn.commit()
            cursor.execute('SELECT * FROM carisma WHERE user_id = ?', (ctx.author.id,))
            resultado = cursor.fetchone()
        
        conn.close()
        
        carisma_bar = "█" * int(resultado['carisma'] / 10) + "░" * (10 - int(resultado['carisma'] / 10))
        pop_bar = "█" * int(resultado['popularidade'] / 10) + "░" * (10 - int(resultado['popularidade'] / 10))
        
        embed = discord.Embed(title="⭐ MEU CARISMA E POPULARIDADE", color=discord.Color.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed.add_field(name="✨ CARISMA", value=f"Carisma:      {carisma_bar} {resultado['carisma']}%\nPopularidade: {pop_bar} {resultado['popularidade']}%\n\n👨‍🎓 Fandom:    {resultado['fandom']}\n😡 Haters:     {resultado['haters']}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - SINDICATOS
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='criarSindicato', help='Cria um sindicato')
async def criar_sindicato(ctx, *, nome: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sindicatos (
            id INTEGER PRIMARY KEY, nome TEXT UNIQUE, presidente_id INTEGER,
            membros INTEGER DEFAULT 1000, poder_mobilizacao REAL DEFAULT 50.0
        )''')
        try:
            cursor.execute('INSERT INTO sindicatos (nome, presidente_id) VALUES (?, ?)', (nome, ctx.author.id))
            conn.commit()
            sindicato_id = cursor.lastrowid
            
            embed = discord.Embed(title="✅ SINDICATO CRIADO", description=f"**{nome}**", color=discord.Color.green())
            embed.add_field(name="👤 Presidente", value=ctx.author.mention, inline=True)
            embed.add_field(name="👥 Membros", value="1.000", inline=True)
            embed.add_field(name="💪 Poder", value="50%", inline=True)
            db.adicionar_prestige(ctx.author.id, 100)
            await ctx.send(embed=embed)
        except:
            await ctx.send("❌ Sindicato com este nome já existe!")
        conn.close()
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='greve', help='Declara uma greve')
async def declarar_greve(ctx, sindicato_id: int, *, motivo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS greves (
            id INTEGER PRIMARY KEY, sindicato_id INTEGER, motivo TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ativa BOOLEAN DEFAULT 1
        )''')
        cursor.execute('INSERT INTO greves (sindicato_id, motivo) VALUES (?, ?)', (sindicato_id, motivo))
        conn.commit()
        greve_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="🔥 GREVE DECLARADA", description=motivo, color=discord.Color.red())
        embed.add_field(name="📋 ID da Greve", value=greve_id, inline=True)
        embed.add_field(name="⚠️ Impacto", value="-10% economia", inline=True)
        db.alterar_aprovacao(ctx.guild.id, -10)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - INFRAESTRUTURA
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='infraestrutura', help='Mostra infraestrutura')
async def infra_status(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS infraestrutura (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            estradas INTEGER DEFAULT 100, ferrovias INTEGER DEFAULT 50,
            portos INTEGER DEFAULT 10, aeroportos INTEGER DEFAULT 10,
            hidroeletricas INTEGER DEFAULT 20, investimento INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM infraestrutura WHERE servidor_id = ?', (ctx.guild.id,))
        infra = cursor.fetchone()
        
        if not infra:
            cursor.execute('INSERT INTO infraestrutura (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM infraestrutura WHERE servidor_id = ?', (ctx.guild.id,))
            infra = cursor.fetchone()
        
        conn.close()
        
        embed = discord.Embed(title="🏗️ INFRAESTRUTURA NACIONAL", color=discord.Color.orange())
        embed.add_field(name="🛣️ DISTRIBUIÇÃO", value=f"Estradas:       {infra['estradas']}\nFerrovias:      {infra['ferrovias']}\nPortos:         {infra['portos']}\nAeroportos:     {infra['aeroportos']}\nHidrelétricas:  {infra['hidroeletricas']}", inline=False)
        embed.add_field(name="💰 INVESTIMENTO", value=f"Total: R$ {infra['investimento']:,}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - EDUCAÇÃO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='educacao', help='Mostra educa��ão')
async def sistema_educacao(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS educacao (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            taxa_escolarizacao REAL DEFAULT 85.0, qualidade REAL DEFAULT 50.0,
            universidades INTEGER DEFAULT 50, investimento INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM educacao WHERE servidor_id = ?', (ctx.guild.id,))
        edu = cursor.fetchone()
        
        if not edu:
            cursor.execute('INSERT INTO educacao (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM educacao WHERE servidor_id = ?', (ctx.guild.id,))
            edu = cursor.fetchone()
        
        conn.close()
        
        edu_bar = "█" * int(edu['taxa_escolarizacao'] / 10) + "░" * (10 - int(edu['taxa_escolarizacao'] / 10))
        qual_bar = "█" * int(edu['qualidade'] / 10) + "░" * (10 - int(edu['qualidade'] / 10))
        
        embed = discord.Embed(title="📚 SISTEMA DE EDUCAÇÃO", color=discord.Color.green())
        embed.add_field(name="📊 INDICADORES", value=f"Taxa de Escolarização:  {edu_bar} {edu['taxa_escolarizacao']:.1f}%\nQualidade:              {qual_bar} {edu['qualidade']:.0f}%\n\nUniversidades: {edu['universidades']}\nInvestimento: R$ {edu['investimento']:,}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - SAÚDE
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='saude', help='Mostra saúde')
async def sistema_saude(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS saude (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            taxa_mortalidade REAL DEFAULT 5.0, expectativa_vida REAL DEFAULT 75.0,
            hospitais INTEGER DEFAULT 100, qualidade REAL DEFAULT 50.0,
            investimento INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM saude WHERE servidor_id = ?', (ctx.guild.id,))
        saude = cursor.fetchone()
        
        if not saude:
            cursor.execute('INSERT INTO saude (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM saude WHERE servidor_id = ?', (ctx.guild.id,))
            saude = cursor.fetchone()
        
        conn.close()
        
        embed = discord.Embed(title="🏥 SISTEMA DE SAÚDE", color=discord.Color.red())
        embed.add_field(name="📊 INDICADORES", value=f"Taxa de Mortalidade:  {saude['taxa_mortalidade']:.1f}%\nExpectativa de Vida:  {saude['expectativa_vida']:.1f} anos\nQualidade:            {saude['qualidade']:.0f}%\n\nHospitais: {saude['hospitais']}\nInvestimento: R$ {saude['investimento']:,}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - BOLETIM DIÁRIO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='boletimRecente', help='Mostra boletim do dia')
async def boletim_recente(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM noticias_ia ORDER BY rowid DESC LIMIT 1')
        boletim = cursor.fetchone()
        conn.close()
        
        if not boletim:
            await ctx.send("❌ Nenhum boletim criado!")
            return
        
        embed = discord.Embed(title="📰 BOLETIM DO DIA", color=discord.Color.blue())
        embed.add_field(name="📰 MANCHETE", value=boletim['manchete'], inline=False)
        embed.add_field(name="📝 NOTÍCIA", value=boletim['conteudo'], inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - RAIVA DO POVO / REVOLUÇÃO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='raivaPovo', help='Mostra raiva do povo')
async def raiva_povo(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS raiva_povo (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE, 
            nivel REAL DEFAULT 20.0
        )''')
        cursor.execute('SELECT * FROM raiva_povo WHERE servidor_id = ?', (ctx.guild.id,))
        raiva = cursor.fetchone()
        
        if not raiva:
            cursor.execute('INSERT INTO raiva_povo (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM raiva_povo WHERE servidor_id = ?', (ctx.guild.id,))
            raiva = cursor.fetchone()
        
        conn.close()
        
        if raiva['nivel'] >= 90:
            emoji = "🔴"
            status = "CRÍTICO - GOLPE IMINENTE"
        elif raiva['nivel'] >= 75:
            emoji = "🟠"
            status = "ALTO - REVOLUÇÃO POSSÍVEL"
        elif raiva['nivel'] >= 50:
            emoji = "🟡"
            status = "MÉDIO - PROTESTOS AUMENTANDO"
        else:
            emoji = "🟢"
            status = "BAIXO - POPULAÇÃO CALMA"
        
        barra = "█" * int(raiva['nivel'] / 10) + "░" * (10 - int(raiva['nivel'] / 10))
        
        embed = discord.Embed(title="😡 ÍNDICE DE RAIVA DO POVO", color=discord.Color.red() if raiva['nivel'] > 75 else discord.Color.orange())
        embed.add_field(name=f"{emoji} RAIVA NACIONAL", value=f"{barra}\n{raiva['nivel']:.1f}%\n\n{status}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='revolucao', help='Inicia revolução (Drama máximo)')
async def iniciar_revolucao(ctx, *, motivo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM raiva_povo WHERE servidor_id = ?', (ctx.guild.id,))
        raiva = cursor.fetchone()
        
        if not raiva or raiva['nivel'] < 75:
            await ctx.send(f"❌ Raiva do povo insuficiente! (precisa de 75%+)")
            return
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS revolucoes (
            id INTEGER PRIMARY KEY, servidor_id INTEGER, lider_id INTEGER,
            motivo TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP, ativa BOOLEAN DEFAULT 1
        )''')
        cursor.execute('INSERT INTO revolucoes (servidor_id, lider_id, motivo) VALUES (?, ?, ?)', 
                      (ctx.guild.id, ctx.author.id, motivo))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="🚩 REVOLUÇÃO INICIADA!", description=motivo, color=discord.Color.dark_red())
        embed.add_field(name="🎯 Líder", value=ctx.author.mention, inline=True)
        embed.add_field(name="⚠️ Status", value="CAOS POLÍTICO", inline=True)
        embed.add_field(name="💥 Impacto", value="Governo em risco de queda!", inline=False)
        db.alterar_aprovacao(ctx.guild.id, -50)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - COLIGAÇÃO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='coligacao', help='Mostra coligação do governo')
async def mostra_coligacao(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS coligacao (
            id INTEGER PRIMARY KEY, governo_id INTEGER,
            presidente_id INTEGER, partidos TEXT, fragilidade REAL DEFAULT 50.0
        )''')
        cursor.execute('SELECT * FROM coligacao LIMIT 1')
        coligacao = cursor.fetchone()
        conn.close()
        
        if not coligacao:
            await ctx.send("❌ Nenhuma coligação registrada!")
            return
        
        try:
            presidente = await bot.fetch_user(coligacao['presidente_id'])
            pres_nome = presidente.name
        except:
            pres_nome = "Desconhecido"
        
        if coligacao['fragilidade'] >= 75:
            frag_emoji = "🔴"
            frag_status = "Muito Frágil"
        elif coligacao['fragilidade'] >= 50:
            frag_emoji = "🟠"
            frag_status = "Frágil"
        else:
            frag_emoji = "🟢"
            frag_status = "Estável"
        
        embed = discord.Embed(title="🤝 COLIGAÇÃO GOVERNAMENTAL", description=f"Governo de {pres_nome}", color=discord.Color.blue())
        embed.add_field(name="👑 Presidente", value=pres_nome, inline=True)
        embed.add_field(name="🏛️ Partidos", value=coligacao['partidos'][:200], inline=False)
        embed.add_field(name="💪 Fragilidade", value=f"{frag_emoji} {frag_status} ({coligacao['fragilidade']:.0f}%)", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='ameacaSaida', help='Ameaça sair da coligação')
async def ameaca_saida(ctx, *, motivo: str):
    try:
        filiacao = db.obter_filiacao(ctx.author.id)
        if not filiacao:
            await ctx.send("❌ Você não é filiado a nenhum partido!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ameacas_coligacao (
            id INTEGER PRIMARY KEY, partido TEXT, motivo TEXT,
            severidade REAL DEFAULT 50.0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO ameacas_coligacao (partido, motivo, severidade) VALUES (?, ?, ?)', 
                      (filiacao['partido'], motivo, random.uniform(30, 70)))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="⚠️ AMEAÇA DE SAÍDA", description=f"Partido **{filiacao['partido']}** ameaça sair", color=discord.Color.red())
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="⚠️ Impacto", value="Coligação em risco!", inline=True)
        db.alterar_aprovacao(ctx.guild.id, -15)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - LEIS E LEGISLATIVO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='projetoDeLei', help='Propõe um projeto de lei')
async def projeto_lei(ctx, *, titulo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO leis (autor_id, titulo) VALUES (?, ?)', (ctx.author.id, titulo))
        conn.commit()
        lei_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="📜 PROJETO DE LEI", description=titulo, color=discord.Color.blue())
        embed.add_field(name="👤 Autor", value=ctx.author.mention, inline=True)
        embed.add_field(name="ID", value=lei_id, inline=True)
        embed.add_field(name="📊 Status", value="Em discussão", inline=True)
        db.adicionar_prestige(ctx.author.id, 50)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='votarLei', help='Vota em um projeto de lei')
async def votar_lei(ctx, lei_id: int, voto: str):
    try:
        if voto.lower() not in ['sim', 'não', 'abstençao']:
            await ctx.send("❌ Vote com: sim, não ou abstençao")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        
        if voto.lower() == 'sim':
            cursor.execute('UPDATE leis SET votos_favor = votos_favor + 1 WHERE id = ?', (lei_id,))
            voto_txt = "SIM ✅"
        elif voto.lower() == 'não':
            cursor.execute('UPDATE leis SET votos_contra = votos_contra + 1 WHERE id = ?', (lei_id,))
            voto_txt = "NÃO ❌"
        else:
            voto_txt = "ABSTENÇÃO ⚪"
        
        conn.commit()
        
        cursor.execute('SELECT * FROM leis WHERE id = ?', (lei_id,))
        lei = cursor.fetchone()
        conn.close()
        
        embed = discord.Embed(title="✅ VOTO REGISTRADO", description=f"Lei #{lei_id}", color=discord.Color.green())
        embed.add_field(name="🗳️ Voto", value=voto_txt, inline=True)
        embed.add_field(name="📊 Placar", value=f"✅ {lei['votos_favor']} vs ❌ {lei['votos_contra']}", inline=True)
        db.adicionar_prestige(ctx.author.id, 5)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - HONRARIAS
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='concederHonraria', help='Concede honraria (Admin)')
@commands.has_permissions(administrator=True)
async def conceder_honraria(ctx, usuario: discord.User, tipo: str, *, nome: str):
    try:
        tipos_validos = ['cavaleiro', 'merito', 'doutor', 'medalha', 'homenagem']
        tipo = tipo.lower()
        
        if tipo not in tipos_validos:
            await ctx.send(f"❌ Tipo inválido! Use: {', '.join(tipos_validos)}")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS honrarias (
            id INTEGER PRIMARY KEY, user_id INTEGER, tipo TEXT,
            nome TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO honrarias (user_id, tipo, nome) VALUES (?, ?, ?)', 
                      (usuario.id, tipo, nome))
        conn.commit()
        conn.close()
        
        emoji_tipo = {
            'cavaleiro': '⚔️',
            'merito': '🏅',
            'doutor': '🎓',
            'medalha': '🏆',
            'homenagem': '🎉'
        }
        
        embed = discord.Embed(title=f"✅ {emoji_tipo.get(tipo, '⭐')} HONRARIA CONCEDIDA", description=f"**{nome}**", color=discord.Color.gold())
        embed.add_field(name="👤 Agraciado", value=usuario.mention, inline=True)
        embed.add_field(name="🏆 Tipo", value=tipo.replace('_', ' ').upper(), inline=True)
        db.adicionar_prestige(usuario.id, 100)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='minhasHonrarias', help='Mostra suas honrarias')
async def minhas_honrarias(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM honrarias WHERE user_id = ?', (ctx.author.id,))
        honrarias = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🏆 MINHAS HONRARIAS", description=f"Total de **{len(honrarias)}** honrarias", color=discord.Color.gold())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        
        if honrarias:
            for honraria in honrarias:
                embed.add_field(name=f"🏆 {honraria['nome']}", value=f"Tipo: {honraria['tipo'].upper()}", inline=False)
        else:
            embed.description = "Você ainda não tem honrarias."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - PATRIMONIOS HISTÓRICOS
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='criarPatrimonio', help='Cria patrimônio histórico (Admin)')
@commands.has_permissions(administrator=True)
async def criar_patrimonio(ctx, tipo: str, *, info: str):
    try:
        partes = info.split('|')
        if len(partes) < 2:
            await ctx.send("❌ Formato: `!criarPatrimonio tipo Nome|Descrição`")
            return
        
        nome = partes[0].strip()
        descricao = partes[1].strip()
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS patrimonios (
            id INTEGER PRIMARY KEY, nome TEXT UNIQUE, tipo TEXT,
            descricao TEXT, visitantes INTEGER DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO patrimonios (nome, tipo, descricao) VALUES (?, ?, ?)', 
                      (nome, tipo, descricao))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="✅ PATRIMÔNIO CRIADO", description=f"**{nome}**", color=discord.Color.green())
        embed.add_field(name="🏛️ Tipo", value=tipo.upper(), inline=True)
        embed.add_field(name="📝 Descrição", value=descricao, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='patrimonios', help='Lista patrimônios históricos')
async def listar_patrimonios(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patrimonios ORDER BY visitantes DESC LIMIT 10')
        patrimonios = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🏛️ PATRIMÔNIOS HISTÓRICOS", description=f"Total de **{len(patrimonios)}** patrimônios", color=discord.Color.blue())
        
        if patrimonios:
            for pat in patrimonios:
                embed.add_field(name=f"🏛️ {pat['nome']}", value=f"Tipo: {pat['tipo'].upper()}\n{pat['descricao'][:100]}...\n👥 Visitantes: {pat['visitantes']:,}", inline=False)
        else:
            embed.description = "Nenhum patrimônio registrado."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - MOEDA E BANCO CENTRAL
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='moedaNacional', help='Mostra moeda nacional')
async def moeda_nacional(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS moeda (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            nome TEXT DEFAULT 'Real', valor_cambio REAL DEFAULT 5.0,
            estabilidade REAL DEFAULT 50.0
        )''')
        cursor.execute('SELECT * FROM moeda WHERE servidor_id = ?', (ctx.guild.id,))
        moeda = cursor.fetchone()
        
        if not moeda:
            cursor.execute('INSERT INTO moeda (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM moeda WHERE servidor_id = ?', (ctx.guild.id,))
            moeda = cursor.fetchone()
        
        conn.close()
        
        embed = discord.Embed(title="💱 MOEDA NACIONAL", description=f"**{moeda['nome']}**", color=discord.Color.gold())
        embed.add_field(name="💱 Câmbio", value=f"R$ {moeda['valor_cambio']:.2f} / USD", inline=True)
        embed.add_field(name="⚙️ Estabilidade", value=f"{moeda['estabilidade']:.0f}%", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='bancocentral', help='Mostra banco central')
async def banco_central_info(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS banco_central (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            presidente_id INTEGER, taxa_juros REAL DEFAULT 10.5,
            reservas_internacionais INTEGER DEFAULT 500000
        )''')
        cursor.execute('SELECT * FROM banco_central WHERE servidor_id = ?', (ctx.guild.id,))
        bc = cursor.fetchone()
        
        if not bc:
            cursor.execute('INSERT INTO banco_central (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM banco_central WHERE servidor_id = ?', (ctx.guild.id,))
            bc = cursor.fetchone()
        
        conn.close()
        
        try:
            presidente = await bot.fetch_user(bc['presidente_id'])
            pres_nome = presidente.name
        except:
            pres_nome = "Vago"
        
        embed = discord.Embed(title="🏦 BANCO CENTRAL", color=discord.Color.gold())
        embed.add_field(name="👤 Presidente", value=pres_nome, inline=True)
        embed.add_field(name="📊 Taxa de Juros", value=f"{bc['taxa_juros']:.2f}%", inline=True)
        embed.add_field(name="💰 Reservas", value=f"R$ {bc['reservas_internacionais']:,}", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='alterarTaxaJuros', help='Altera taxa de juros (Admin)')
@commands.has_permissions(administrator=True)
async def alterar_taxa_juros(ctx, taxa: float):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('UPDATE banco_central SET taxa_juros = ? WHERE servidor_id = ?', (taxa, ctx.guild.id))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="✅ TAXA DE JUROS ALTERADA", color=discord.Color.green())
        embed.add_field(name="📊 Nova Taxa", value=f"{taxa:.2f}%", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - ECONOMIA
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='economia', help='Mostra economia nacional')
async def economia_nacional(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS economia (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            pib INTEGER DEFAULT 1000000, inflacao REAL DEFAULT 3.0,
            desemprego REAL DEFAULT 5.0, investimento_estrangeiro INTEGER DEFAULT 0,
            divida_publica INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM economia WHERE servidor_id = ?', (ctx.guild.id,))
        eco = cursor.fetchone()
        
        if not eco:
            cursor.execute('INSERT INTO economia (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM economia WHERE servidor_id = ?', (ctx.guild.id,))
            eco = cursor.fetchone()
        
        conn.close()
        
        pib_bar = "█" * int(eco['pib'] / 100000) + "░" * (10 - int(eco['pib'] / 100000))
        
        embed = discord.Embed(title="📊 ECONOMIA NACIONAL", color=discord.Color.gold())
        embed.add_field(name="💰 PIB", value=f"{pib_bar}\nR$ {eco['pib']:,}", inline=False)
        embed.add_field(name="📈 INDICADORES", value=f"Inflação:                    {eco['inflacao']:.1f}%\nDesemprego:                  {eco['desemprego']:.1f}%\nInvestimento Estrangeiro:    R$ {eco['investimento_estrangeiro']:,}\nDívida Pública:              R$ {eco['divida_publica']:,}", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='inflacao', help='Mostra inflação')
async def ver_inflacao(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM economia WHERE servidor_id = ?', (ctx.guild.id,))
        eco = cursor.fetchone()
        conn.close()
        
        if not eco:
            await ctx.send("❌ Nenhuma economia registrada!")
            return
        
        if eco['inflacao'] < 2:
            status = "✅ Muito baixa"
        elif eco['inflacao'] < 5:
            status = "🟢 Controlada"
        elif eco['inflacao'] < 10:
            status = "🟡 Elevada"
        else:
            status = "🔴 Descontrolada"
        
        embed = discord.Embed(title="📈 INFLAÇÃO", color=discord.Color.orange())
        embed.add_field(name="📊 Taxa", value=f"{eco['inflacao']:.1f}%", inline=True)
        embed.add_field(name="📈 Status", value=status, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='desemprego', help='Mostra desemprego')
async def ver_desemprego(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM economia WHERE servidor_id = ?', (ctx.guild.id,))
        eco = cursor.fetchone()
        conn.close()
        
        if not eco:
            await ctx.send("❌ Nenhuma economia registrada!")
            return
        
        if eco['desemprego'] < 3:
            status = "✅ Muito baixo"
        elif eco['desemprego'] < 6:
            status = "🟢 Normal"
        elif eco['desemprego'] < 10:
            status = "🟡 Alto"
        else:
            status = "🔴 Crítico"
        
        embed = discord.Embed(title="💼 DESEMPREGO", color=discord.Color.red())
        embed.add_field(name="📊 Taxa", value=f"{eco['desemprego']:.1f}%", inline=True)
        embed.add_field(name="📈 Status", value=status, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - FORÇA ARMADA
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='forcasArmadas', help='Mostra forças armadas')
async def forcas_armadas(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS forcas (
            id INTEGER PRIMARY KEY, tipo TEXT, nome TEXT,
            comandante_id INTEGER, tamanho INTEGER DEFAULT 1000,
            lealdade REAL DEFAULT 50.0, oracamento INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM forcas')
        forcas = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🪖 FORÇAS ARMADAS", color=discord.Color.purple())
        
        if forcas:
            for forca in forcas:
                try:
                    cmd = await bot.fetch_user(forca['comandante_id'])
                    cmd_nome = cmd.name
                except:
                    cmd_nome = "Vago"
                
                lealdade_bar = "█" * int(forca['lealdade'] / 10) + "░" * (10 - int(forca['lealdade'] / 10))
                embed.add_field(name=f"🪖 {forca['nome']} ({forca['tipo'].upper()})", 
                               value=f"Comandante: {cmd_nome}\nTamanho: {forca['tamanho']:,} soldados\nLealdade: {lealdade_bar} {forca['lealdade']:.0f}%\nOrçamento: R$ {forca['oracamento']:,}", 
                               inline=False)
        else:
            embed.description = "Nenhuma força armada registrada."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='criarForca', help='Cria força armada (Admin)')
@commands.has_permissions(administrator=True)
async def criar_forca(ctx, tipo: str, *, nome: str):
    try:
        tipos_validos = ['exercito', 'marinha', 'forca_aerea', 'marinhos']
        if tipo.lower() not in tipos_validos:
            await ctx.send(f"❌ Tipo inválido! Use: {', '.join(tipos_validos)}")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO forcas (tipo, nome) VALUES (?, ?)', (tipo.lower(), nome))
        conn.commit()
        forca_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="✅ FORÇA CRIADA", description=f"**{nome}**", color=discord.Color.green())
        embed.add_field(name="🪖 Tipo", value=tipo.upper(), inline=True)
        embed.add_field(name="ID", value=forca_id, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='operacaoMilitar', help='Inicia operação militar')
async def operacao_militar(ctx, forca_id: int, *, descricao: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS operacoes_militares (
            id INTEGER PRIMARY KEY, forca_id INTEGER, descricao TEXT,
            sucesso BOOLEAN DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO operacoes_militares (forca_id, descricao) VALUES (?, ?)', 
                      (forca_id, descricao))
        conn.commit()
        operacao_id = cursor.lastrowid
        conn.close()
        
        sucesso = random.choice([True, False])
        resultado = "✅ SUCESSO" if sucesso else "❌ FRACASSO"
        
        embed = discord.Embed(title="🪖 OPERAÇÃO MILITAR", description=descricao, color=discord.Color.red() if not sucesso else discord.Color.green())
        embed.add_field(name="📋 Resultado", value=resultado, inline=True)
        embed.add_field(name="ID", value=operacao_id, inline=True)
        
        if not sucesso:
            db.alterar_aprovacao(ctx.guild.id, -30)
        else:
            db.alterar_aprovacao(ctx.guild.id, 20)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - ESPIONAGEM
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='agenciaInteligencia', help='Mostra agência de inteligência')
async def agencia_inteligencia(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS inteligencia (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            chefe_id INTEGER, oracamento INTEGER DEFAULT 5000,
            eficiencia REAL DEFAULT 50.0
        )''')
        cursor.execute('SELECT * FROM inteligencia WHERE servidor_id = ?', (ctx.guild.id,))
        inteligencia = cursor.fetchone()
        
        if not inteligencia:
            cursor.execute('INSERT INTO inteligencia (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM inteligencia WHERE servidor_id = ?', (ctx.guild.id,))
            inteligencia = cursor.fetchone()
        
        conn.close()
        
        try:
            chefe = await bot.fetch_user(inteligencia['chefe_id'])
            chefe_nome = chefe.name
        except:
            chefe_nome = "Vago"
        
        efic_bar = "█" * int(inteligencia['eficiencia'] / 10) + "░" * (10 - int(inteligencia['eficiencia'] / 10))
        
        embed = discord.Embed(title="🕵️ AGÊNCIA DE INTELIGÊNCIA", color=discord.Color.dark_gray())
        embed.add_field(name="👤 Chefe", value=chefe_nome, inline=True)
        embed.add_field(name="💼 Orçamento", value=f"R$ {inteligencia['oracamento']:,}", inline=True)
        embed.add_field(name="⚙️ Eficiência", value=f"{efic_bar}\n{inteligencia['eficiencia']:.0f}%", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='operacaoSecreta', help='Inicia operação secreta')
async def operacao_secreta(ctx, alvo: discord.User, *, descricao: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS operacoes_secretas (
            id INTEGER PRIMARY KEY, alvo_id INTEGER, operador_id INTEGER,
            descricao TEXT, sucesso BOOLEAN DEFAULT 0, descoberta BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO operacoes_secretas (alvo_id, operador_id, descricao) VALUES (?, ?, ?)', 
                      (alvo.id, ctx.author.id, descricao))
        conn.commit()
        operacao_id = cursor.lastrowid
        conn.close()
        
        sucesso = random.choice([True, False])
        descoberta = random.choice([True, False]) if sucesso else False
        
        resultado = "✅ SUCESSO" if sucesso else "❌ FRACASSO"
        descoberta_txt = "🚨 DESCOBERTA!" if descoberta else "🤫 SEGREDO"
        
        embed = discord.Embed(title="🕵️ OPERAÇÃO SECRETA", description=descricao, color=discord.Color.dark_gray())
        embed.add_field(name="🎯 Alvo", value=alvo.mention, inline=True)
        embed.add_field(name="📋 Resultado", value=resultado, inline=True)
        embed.add_field(name="🔒 Status", value=descoberta_txt, inline=True)
        
        if descoberta:
            db.alterar_aprovacao(ctx.guild.id, -40)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='vazamento', help='Vaza informação importante')
async def vazar_informacao(ctx, *, informacao: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 500:
            await ctx.send("❌ Você precisa de 500+ prestige para vazar informação!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vazamentos (
            id INTEGER PRIMARY KEY, vazio_por_id INTEGER, informacao TEXT,
            confirmada BOOLEAN DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO vazamentos (vazio_por_id, informacao) VALUES (?, ?)', 
                      (ctx.author.id, informacao))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, -100)
        db.alterar_aprovacao(ctx.guild.id, -25)
        
        embed = discord.Embed(title="🚨 VAZAMENTO", description=informacao, color=discord.Color.red())
        embed.add_field(name="👤 Vazador", value=ctx.author.mention, inline=True)
        embed.add_field(name="⚠️ Impacto", value="Muito Alto", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - PESQUISAS E SONDAGENS
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='pesquisa', help='Realiza pesquisa de intenção de voto')
async def fazer_pesquisa(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pesquisas (
            id INTEGER PRIMARY KEY, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amostra INTEGER DEFAULT 1000, confiabilidade REAL DEFAULT 95.0
        )''')
        cursor.execute('INSERT INTO pesquisas DEFAULT VALUES')
        conn.commit()
        pesquisa_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="📊 PESQUISA DE INTENÇÃO DE VOTO", color=discord.Color.blue())
        embed.add_field(name="📋 ID", value=pesquisa_id, inline=True)
        embed.add_field(name="👥 Amostra", value="1.000 pessoas", inline=True)
        embed.add_field(name="📈 Confiabilidade", value="95%", inline=True)
        embed.add_field(name="📊 Resultados", value="Simulando votação... ⏳", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='sondagem', help='Realiza sondagem rápida')
async def sondagem_rapida(ctx, *, pergunta: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sondagens (
            id INTEGER PRIMARY KEY, pergunta TEXT, votos_sim INTEGER DEFAULT 0,
            votos_nao INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO sondagens (pergunta) VALUES (?)', (pergunta,))
        conn.commit()
        sondagem_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="🗳️ SONDAGEM", description=pergunta, color=discord.Color.blue())
        embed.add_field(name="✅ SIM", value="0 votos", inline=True)
        embed.add_field(name="❌ NÃO", value="0 votos", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - REDENÇÃO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='redencao', help='Inicia arco de redenção')
async def arco_redencao(ctx, *, descricao: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 1000:
            await ctx.send("❌ Você precisa de 1000+ prestige para iniciar redenção!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS redencoes (
            id INTEGER PRIMARY KEY, politico_id INTEGER, descricao TEXT,
            villao_antes BOOLEAN DEFAULT 1, publico_perdoou BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO redencoes (politico_id, descricao) VALUES (?, ?)', 
                      (ctx.author.id, descricao))
        conn.commit()
        redencao_id = cursor.lastrowid
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, -200)
        embed = discord.Embed(title="✨ ARCO DE REDENÇÃO INICIADO", description=descricao, color=discord.Color.gold())
        embed.add_field(name="👤 Personagem", value=ctx.author.mention, inline=True)
        embed.add_field(name="ID", value=redencao_id, inline=True)
        embed.add_field(name="⭐ Status", value="Em transformação", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='perdaoPresidencial', help='Concede perdão presidencial')
async def perdao_presidencial(ctx, perdoado: discord.User, *, crime: str):
    try:
        filiacao = db.obter_filiacao(ctx.author.id)
        if not filiacao:
            await ctx.send("❌ Você não é filiado a nenhum partido!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS perdoes (
            id INTEGER PRIMARY KEY, presidente_id INTEGER, perdoado_id INTEGER,
            crime TEXT, controversia REAL DEFAULT 30.0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO perdoes (presidente_id, perdoado_id, crime) VALUES (?, ?, ?)', 
                      (ctx.author.id, perdoado.id, crime))
        conn.commit()
        perdao_id = cursor.lastrowid
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, random.uniform(-30, 20))
        embed = discord.Embed(title="⚖️ PERDÃO PRESIDENCIAL", description=f"**{perdoado.name}** recebe perdão", color=discord.Color.gold())
        embed.add_field(name="👤 Presidente", value=ctx.author.mention, inline=True)
        embed.add_field(name="🎯 Perdoado", value=perdoado.mention, inline=True)
        embed.add_field(name="📝 Crime", value=crime, inline=False)
        embed.add_field(name="⚠️ Controversia", value="Muito polêmico!", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - CRISE EXISTENCIAL
# ═════════════════════════════════════���═════════════════════════════

@bot.command(name='criseExistencial', help='Passa por crise existencial')
async def crise_existencial(ctx, *, descricao: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS crises_existenciais (
            id INTEGER PRIMARY KEY, politico_id INTEGER, descricao TEXT,
            severidade REAL DEFAULT 50.0, resolvida BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO crises_existenciais (politico_id, descricao, severidade) VALUES (?, ?, ?)', 
                      (ctx.author.id, descricao, random.uniform(30, 80)))
        conn.commit()
        crise_id = cursor.lastrowid
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, -50)
        embed = discord.Embed(title="😵 CRISE EXISTENCIAL", description=descricao, color=discord.Color.purple())
        embed.add_field(name="👤 Afetado", value=ctx.author.mention, inline=True)
        embed.add_field(name="ID", value=crise_id, inline=True)
        embed.add_field(name="⚠️ Severidade", value="Muito Alto", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - ASSASSINATOS E VIOLÊNCIA
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='assassinato', help='Registra assassinato político')
async def assassinato_politico(ctx, vitima: discord.User, *, motivo: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 2000:
            await ctx.send("❌ Você precisa de 2000+ prestige para isso!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS assassinatos (
            id INTEGER PRIMARY KEY, vitima_id INTEGER, perpetrador_id INTEGER,
            motivo TEXT, descoberto BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO assassinatos (vitima_id, perpetrador_id, motivo) VALUES (?, ?, ?)', 
                      (vitima.id, ctx.author.id, motivo))
        conn.commit()
        assassinato_id = cursor.lastrowid
        conn.close()
        
        descoberto = random.choice([True, False])
        descoberta_txt = "🔍 JÁ DESCOBERTO!" if descoberto else "🤫 SEGREDO POR ENQUANTO"
        
        db.adicionar_prestige(ctx.author.id, -500)
        db.alterar_aprovacao(ctx.guild.id, -50)
        
        embed = discord.Embed(title="💀 ASSASSINATO POLÍTICO", description=f"**{vitima.name}** foi assassinado", color=discord.Color.dark_red())
        embed.add_field(name="👤 Vítima", value=vitima.mention, inline=True)
        embed.add_field(name="🎯 Perpetrador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="🔍 Status", value=descoberta_txt, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='protesto', help='Organiza protesto')
async def organizar_protesto(ctx, *, objetivo: str):
    try:
        tamanho = random.randint(100, 100000)
        violencia = random.choice([True, False])
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS protestos (
            id INTEGER PRIMARY KEY, organizador_id INTEGER, objetivo TEXT,
            tamanho INTEGER, violencia BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO protestos (organizador_id, objetivo, tamanho, violencia) VALUES (?, ?, ?, ?)', 
                      (ctx.author.id, objetivo, tamanho, violencia))
        conn.commit()
        protesto_id = cursor.lastrowid
        conn.close()
        
        violencia_txt = "🔥 COM VIOLÊNCIA" if violencia else "✌️ PACÍFICO"
        impacto = -40 if violencia else -15
        
        db.alterar_aprovacao(ctx.guild.id, impacto)
        db.adicionar_prestige(ctx.author.id, 30)
        
        embed = discord.Embed(title="🚨 PROTESTO ORGANIZADO", description=objetivo, color=discord.Color.orange())
        embed.add_field(name="👤 Organizador", value=ctx.author.mention, inline=True)
        embed.add_field(name="👥 Tamanho", value=f"{tamanho:,} pessoas", inline=True)
        embed.add_field(name="⚠️ Tipo", value=violencia_txt, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - LICITAÇÕES E FRAUDE
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='licitacao', help='Abre licitação pública')
async def abrir_licitacao(ctx, *, info: str):
    try:
        partes = info.split('|')
        if len(partes) < 2:
            await ctx.send("❌ Formato: `!licitacao Descrição|Valor esperado`")
            return
        
        descricao = partes[0].strip()
        valor = int(partes[1].strip())
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS licitacoes (
            id INTEGER PRIMARY KEY, descricao TEXT, valor_esperado INTEGER,
            status TEXT DEFAULT 'aberta', data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO licitacoes (descricao, valor_esperado) VALUES (?, ?)', 
                      (descricao, valor))
        conn.commit()
        licitacao_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="📋 LICITAÇÃO ABERTA", description=descricao, color=discord.Color.blue())
        embed.add_field(name="💰 Valor", value=f"R$ {valor:,}", inline=True)
        embed.add_field(name="ID", value=licitacao_id, inline=True)
        embed.add_field(name="📊 Status", value="Aberta para propostas", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='fraude', help='Realiza fraude em licitação')
async def cometer_fraude(ctx, licitacao_id: int, valor_fraude: int):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 1500:
            await ctx.send("❌ Você precisa de 1500+ prestige para isso!")
            return
        
        descoberta = random.choice([True, False, False])  # 33% chance de ser descoberto
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS fraudes (
            id INTEGER PRIMARY KEY, licitacao_id INTEGER, fraudador_id INTEGER,
            valor_fraude INTEGER, descoberta BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO fraudes (licitacao_id, fraudador_id, valor_fraude, descoberta) VALUES (?, ?, ?, ?)', 
                      (licitacao_id, ctx.author.id, valor_fraude, descoberta))
        conn.commit()
        fraude_id = cursor.lastrowid
        conn.close()
        
        if descoberta:
            db.adicionar_prestige(ctx.author.id, -1000)
            db.alterar_aprovacao(ctx.guild.id, -50)
            resultado = "🚨 DESCOBERTA!"
            cor = discord.Color.red()
        else:
            db.adicionar_prestige(ctx.author.id, 200)
            resultado = "✅ SUCESSO!"
            cor = discord.Color.green()
        
        embed = discord.Embed(title="💰 FRAUDE EM LICITAÇÃO", description=f"Licitação #{licitacao_id}", color=cor)
        embed.add_field(name="💰 Valor da Fraude", value=f"R$ {valor_fraude:,}", inline=True)
        embed.add_field(name="📋 Resultado", value=resultado, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - TRIBUNAL DO POVO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='julgamento', help='Realiza julgamento popular')
async def tribunal_povo(ctx, acusado: discord.User, *, acusacao: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS julgamentos (
            id INTEGER PRIMARY KEY, acusado_id INTEGER, acusacao TEXT,
            votos_culpado INTEGER DEFAULT 0, votos_inocente INTEGER DEFAULT 0,
            sentenca TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO julgamentos (acusado_id, acusacao) VALUES (?, ?)', 
                      (acusado.id, acusacao))
        conn.commit()
        julgamento_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="⚖️ TRIBUNAL DO POVO", description=acusacao, color=discord.Color.gold())
        embed.add_field(name="🎯 Acusado", value=acusado.mention, inline=True)
        embed.add_field(name="ID", value=julgamento_id, inline=True)
        embed.add_field(name="🗳️ Votação", value="Aberta para o povo votar!", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='votoTribunal', help='Vota no tribunal do povo')
async def voto_tribunal(ctx, julgamento_id: int, voto: str):
    try:
        if voto.lower() not in ['culpado', 'inocente']:
            await ctx.send("❌ Vote com: culpado ou inocente")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        
        if voto.lower() == 'culpado':
            cursor.execute('UPDATE julgamentos SET votos_culpado = votos_culpado + 1 WHERE id = ?', (julgamento_id,))
            voto_txt = "CULPADO 🔴"
        else:
            cursor.execute('UPDATE julgamentos SET votos_inocente = votos_inocente + 1 WHERE id = ?', (julgamento_id,))
            voto_txt = "INOCENTE 🟢"
        
        conn.commit()
        cursor.execute('SELECT * FROM julgamentos WHERE id = ?', (julgamento_id,))
        julgamento = cursor.fetchone()
        conn.close()
        
        embed = discord.Embed(title="✅ VOTO REGISTRADO", description=f"Julgamento #{julgamento_id}", color=discord.Color.green())
        embed.add_field(name="🗳️ Voto", value=voto_txt, inline=True)
        embed.add_field(name="📊 Placar", value=f"🔴 {julgamento['votos_culpado']} vs 🟢 {julgamento['votos_inocente']}", inline=True)
        db.adicionar_prestige(ctx.author.id, 5)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - NOSTALGIA E CONSPIRAÇÃO INTERNACIONAL
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='nostalgia', help='Expressa nostalgia de era passada')
async def nostalgia_era(ctx, *, info: str):
    try:
        partes = info.split('|')
        if len(partes) < 2:
            await ctx.send("❌ Formato: `!nostalgia Era|Presidente que sente falta`")
            return
        
        era = partes[0].strip()
        presidente = partes[1].strip()
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS nostalgias (
            id INTEGER PRIMARY KEY, era TEXT, presidente_saudade TEXT,
            apoio INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO nostalgias (era, presidente_saudade) VALUES (?, ?)', (era, presidente))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="😔 NOSTALGIA", description=f"Era de **{era}**", color=discord.Color.blurple())
        embed.add_field(name="👑 Presidente", value=presidente, inline=True)
        embed.add_field(name="💭 Sentimento", value="Saudade do passado", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='conspiracao', help='Cria conspiração internacional')
async def conspiração_internacional(ctx, pais_alvo: str, *, info: str):
    try:
        partes = info.split('|')
        if len(partes) < 2:
            await ctx.send("❌ Formato: `!conspiracao país_alvo Tipo|Objetivo`")
            return
        
        tipo = partes[0].strip()
        objetivo = partes[1].strip()
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS conspirações (
            id INTEGER PRIMARY KEY, pais_alvo TEXT, tipo TEXT,
            objetivo TEXT, descoberta BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO conspirações (pais_alvo, tipo, objetivo) VALUES (?, ?, ?)', 
                      (pais_alvo, tipo, objetivo))
        conn.commit()
        conspiracao_id = cursor.lastrowid
        conn.close()
        
        descoberta = random.choice([True, False, False])
        descoberta_txt = "🔍 DESCOBERTA!" if descoberta else "🤫 EM SEGREDO"
        
        embed = discord.Embed(title="🌍 CONSPIRAÇÃO INTERNACIONAL", description=objetivo, color=discord.Color.dark_red())
        embed.add_field(name="🌎 País Alvo", value=pais_alvo.upper(), inline=True)
        embed.add_field(name="📋 Tipo", value=tipo, inline=True)
        embed.add_field(name="🔒 Status", value=descoberta_txt, inline=False)
        
        if descoberta:
            db.alterar_aprovacao(ctx.guild.id, -30)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - MÚLTIPLOS PAÍSES
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='criarPais', help='Cria um novo país (Admin)')
@commands.has_permissions(administrator=True)
async def criar_pais(ctx, *, nome: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS paises (
            id INTEGER PRIMARY KEY, nome TEXT UNIQUE, presidente_id INTEGER,
            ideologia TEXT DEFAULT 'Neutra', poder_militar REAL DEFAULT 50.0,
            poder_economico REAL DEFAULT 50.0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        try:
            cursor.execute('INSERT INTO paises (nome) VALUES (?)', (nome,))
            conn.commit()
            pais_id = cursor.lastrowid
            
            embed = discord.Embed(title="✅ PAÍS CRIADO", description=f"**{nome}**", color=discord.Color.green())
            embed.add_field(name="🌍 Nome", value=nome, inline=True)
            embed.add_field(name="ID", value=pais_id, inline=True)
            embed.add_field(name="⚙️ Status", value="Aguardando presidente", inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("❌ País com este nome já existe!")
        conn.close()
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='tornarPresidente', help='Torna alguém presidente de um país')
async def tornar_presidente(ctx, pais_id: int):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('UPDATE paises SET presidente_id = ? WHERE id = ?', (ctx.author.id, pais_id))
        conn.commit()
        
        cursor.execute('SELECT * FROM paises WHERE id = ?', (pais_id,))
        pais = cursor.fetchone()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, 500)
        
        embed = discord.Embed(title="👑 PRESIDENTE ELEITO", description=f"País: **{pais['nome']}**", color=discord.Color.gold())
        embed.add_field(name="👤 Presidente", value=ctx.author.mention, inline=True)
        embed.add_field(name="🌍 País", value=pais['nome'], inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='paises', help='Lista todos os países')
async def listar_paises(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM paises')
        paises = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🌍 MAPA POLÍTICO MUNDIAL", description=f"Total de **{len(paises)}** países", color=discord.Color.blue())
        
        if paises:
            for pais in paises:
                try:
                    presidente = await bot.fetch_user(pais['presidente_id'])
                    pres_nome = presidente.name
                except:
                    pres_nome = "Vago"
                
                mil_bar = "█" * int(pais['poder_militar'] / 10) + "░" * (10 - int(pais['poder_militar'] / 10))
                eco_bar = "█" * int(pais['poder_economico'] / 10) + "░" * (10 - int(pais['poder_economico'] / 10))
                
                embed.add_field(name=f"🌍 {pais['nome']}", 
                               value=f"👑 Presidente: {pres_nome}\n🎖️ Ideologia: {pais['ideologia']}\n🪖 Militar: {mil_bar} {pais['poder_militar']:.0f}%\n💰 Economia: {eco_bar} {pais['poder_economico']:.0f}%", 
                               inline=False)
        else:
            embed.description = "Nenhum país criado ainda."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='relacoes', help='Mostra relações internacionais')
async def relacoes_internacionais(ctx, pais1_id: int, pais2_id: int):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS relacoes (
            id INTEGER PRIMARY KEY, pais1_id INTEGER, pais2_id INTEGER,
            tipo TEXT DEFAULT 'neutra', nivel INTEGER DEFAULT 50
        )''')
        cursor.execute('SELECT * FROM relacoes WHERE (pais1_id = ? AND pais2_id = ?) OR (pais1_id = ? AND pais2_id = ?)', 
                      (pais1_id, pais2_id, pais2_id, pais1_id))
        relacao = cursor.fetchone()
        
        if not relacao:
            cursor.execute('INSERT INTO relacoes (pais1_id, pais2_id) VALUES (?, ?)', (pais1_id, pais2_id))
            conn.commit()
            cursor.execute('SELECT * FROM relacoes WHERE pais1_id = ? AND pais2_id = ?', (pais1_id, pais2_id))
            relacao = cursor.fetchone()
        
        cursor.execute('SELECT * FROM paises WHERE id = ? OR id = ?', (pais1_id, pais2_id))
        paises = cursor.fetchall()
        conn.close()
        
        if len(paises) < 2:
            await ctx.send("❌ Um ou ambos os países não existem!")
            return
        
        pais1 = paises[0]['nome']
        pais2 = paises[1]['nome'] if paises[1]['id'] != paises[0]['id'] else paises[1]['nome']
        
        if relacao['nivel'] >= 75:
            status = "🤝 ALIADOS"
        elif relacao['nivel'] >= 50:
            status = "😐 NEUTROS"
        elif relacao['nivel'] >= 25:
            status = "😠 TENSOS"
        else:
            status = "💣 INIMIGOS"
        
        embed = discord.Embed(title="🌍 RELAÇÕES INTERNACIONAIS", description=f"{pais1} 🤝 {pais2}", color=discord.Color.blue())
        embed.add_field(name="📊 Tipo", value=relacao['tipo'].upper(), inline=True)
        embed.add_field(name="📈 Nível", value=f"{status}\n{relacao['nivel']}/100", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='guerra', help='Declara guerra (Drama máximo)')
async def declarar_guerra(ctx, pais_inimigo_id: int, *, motivo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS guerras (
            id INTEGER PRIMARY KEY, atacante_id INTEGER, defensor_id INTEGER,
            motivo TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            vencedor_id INTEGER, perdas_vida INTEGER DEFAULT 0
        )''')
        cursor.execute('INSERT INTO guerras (atacante_id, defensor_id, motivo) VALUES (?, ?, ?)', 
                      (ctx.author.id, pais_inimigo_id, motivo))
        conn.commit()
        guerra_id = cursor.lastrowid
        conn.close()
        
        vencedor = random.choice([ctx.author.id, pais_inimigo_id])
        perdas = random.randint(1000, 100000)
        
        embed = discord.Embed(title="💣 GUERRA DECLARADA", description=motivo, color=discord.Color.dark_red())
        embed.add_field(name="⚔️ Atacante", value=ctx.author.mention, inline=True)
        embed.add_field(name="🛡️ Defensor", value=f"País #{pais_inimigo_id}", inline=True)
        embed.add_field(name="📋 Resultado", value="Guerra em progresso...", inline=False)
        embed.add_field(name="💀 Perdas", value=f"{perdas:,} vidas", inline=True)
        
        db.alterar_aprovacao(ctx.guild.id, -50)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - ONU
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='onu', help='Mostra informações da ONU')
async def info_onu(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS onu (
            id INTEGER PRIMARY KEY, secao TEXT,
            tema TEXT, votos_sim INTEGER DEFAULT 0,
            votos_nao INTEGER DEFAULT 0, abstencoes INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT COUNT(*) as total FROM onu')
        total = cursor.fetchone()['total']
        conn.close()
        
        embed = discord.Embed(title="🇺🇳 ORGANIZAÇÃO DAS NAÇÕES UNIDAS", description="Fórum Mundial de Diplomacia", color=discord.Color.blue())
        embed.add_field(name="📊 Votações Ativas", value=f"{total}", inline=True)
        embed.add_field(name="🌍 Membros", value="Múltiplos países", inline=True)
        embed.add_field(name="⚖️ Poder", value="Mediação Internacional", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='votacaoONU', help='Cria votação na ONU')
async def votacao_onu(ctx, *, tema: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO onu (secao, tema) VALUES (?, ?)', ('assembleia', tema))
        conn.commit()
        votacao_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="🇺🇳 VOTAÇÃO NA ONU", description=tema, color=discord.Color.blue())
        embed.add_field(name="📋 ID", value=votacao_id, inline=True)
        embed.add_field(name="🗳️ Status", value="Aberta para votação", inline=True)
        embed.add_field(name="📊 Votos", value="SIM: 0 | NÃO: 0 | ABSTENÇÃO: 0", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='votar_onu', help='Vota em votação da ONU')
async def votar_onu(ctx, votacao_id: int, voto: str):
    try:
        if voto.lower() not in ['sim', 'nao', 'abstencao']:
            await ctx.send("❌ Vote com: sim, nao ou abstencao")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        
        if voto.lower() == 'sim':
            cursor.execute('UPDATE onu SET votos_sim = votos_sim + 1 WHERE id = ?', (votacao_id,))
            voto_txt = "SIM ✅"
        elif voto.lower() == 'nao':
            cursor.execute('UPDATE onu SET votos_nao = votos_nao + 1 WHERE id = ?', (votacao_id,))
            voto_txt = "NÃO ❌"
        else:
            cursor.execute('UPDATE onu SET abstencoes = abstencoes + 1 WHERE id = ?', (votacao_id,))
            voto_txt = "ABSTENÇÃO ⚪"
        
        conn.commit()
        cursor.execute('SELECT * FROM onu WHERE id = ?', (votacao_id,))
        votacao = cursor.fetchone()
        conn.close()
        
        embed = discord.Embed(title="✅ VOTO REGISTRADO NA ONU", description=f"Votação #{votacao_id}", color=discord.Color.green())
        embed.add_field(name="🗳️ Voto", value=voto_txt, inline=True)
        embed.add_field(name="📊 Placar", value=f"✅ {votacao['votos_sim']} | ❌ {votacao['votos_nao']} | ⚪ {votacao['abstencoes']}", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='conselhoSeguranca', help='Mostra conselho de segurança')
async def conselho_seguranca(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS conselho (
            id INTEGER PRIMARY KEY, pais_id INTEGER, posicao TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('SELECT * FROM conselho')
        membros = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🔐 CONSELHO DE SEGURANÇA DA ONU", description="5 Membros Permanentes", color=discord.Color.gold())
        
        if membros:
            for i, membro in enumerate(membros, 1):
                embed.add_field(name=f"🌍 Membro {i}", value=f"País #{membro['pais_id']}\nPosição: {membro['posicao'].upper()}", inline=False)
        else:
            embed.description = "Nenhum membro registrado no conselho."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ══════════════════════════════════════��════════════════════════════
# COMANDOS - CENSURA E LIBERDADE DE IMPRENSA
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='censura', help='Censura uma notícia (Admin)')
@commands.has_permissions(administrator=True)
async def censurar_noticia(ctx, *, motivo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS censuras (
            id INTEGER PRIMARY KEY, censura_por_id INTEGER,
            noticia TEXT, motivo TEXT, descoberta BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO censuras (censura_por_id, motivo) VALUES (?, ?)', (ctx.author.id, motivo))
        conn.commit()
        censura_id = cursor.lastrowid
        conn.close()
        
        descoberta = random.choice([True, False, False])
        descoberta_txt = "🔍 DESCOBERTA!" if descoberta else "🤐 SILENCIOSAMENTE"
        
        db.alterar_aprovacao(ctx.guild.id, -30 if descoberta else -5)
        
        embed = discord.Embed(title="🔇 CENSURA", description=motivo, color=discord.Color.red())
        embed.add_field(name="🔒 Status", value=descoberta_txt, inline=True)
        embed.add_field(name="⚠️ Impacto", value="Liberdade de imprensa em risco", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='processarJornalista', help='Processa jornalista')
async def processar_jornalista(ctx, jornalista: discord.User, *, motivo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS processos (
            id INTEGER PRIMARY KEY, jornalista_id INTEGER, acusante_id INTEGER,
            motivo TEXT, resultado TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO processos (jornalista_id, acusante_id, motivo) VALUES (?, ?, ?)', 
                      (jornalista.id, ctx.author.id, motivo))
        conn.commit()
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, -40)
        embed = discord.Embed(title="⚖️ PROCESSO JUDICIAL", description=f"**{jornalista.name}** processado", color=discord.Color.orange())
        embed.add_field(name="📰 Jornalista", value=jornalista.mention, inline=True)
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="⚠️ Alerta", value="Imprensa sofre pressão!", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - VOTO NULO E CABRESTO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='comprarvoto', help='Compra voto de alguém')
async def comprar_voto(ctx, votante: discord.User, valor: int, *, para_quem: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < valor:
            await ctx.send(f"❌ Você não tem R$ {valor:,} em prestige!")
            return
        
        descoberto = random.choice([True, False, False])
        descoberto_txt = "🚨 DESCOBERTO!" if descoberto else "✅ SUCESSO"
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS compras_votos (
            id INTEGER PRIMARY KEY, comprador_id INTEGER, votante_id INTEGER,
            valor INTEGER, para_quem TEXT, descoberto BOOLEAN,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO compras_votos (comprador_id, votante_id, valor, para_quem, descoberto) VALUES (?, ?, ?, ?, ?)', 
                      (ctx.author.id, votante.id, valor, para_quem, descoberto))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, -valor)
        
        if descoberto:
            db.alterar_aprovacao(ctx.guild.id, -50)
        
        embed = discord.Embed(title="💰 COMPRA DE VOTO", description=f"Voto comprado por R$ {valor:,}", color=discord.Color.red() if descoberto else discord.Color.green())
        embed.add_field(name="👤 Votante", value=votante.mention, inline=True)
        embed.add_field(name="🎯 Para", value=para_quem, inline=True)
        embed.add_field(name="📋 Status", value=descoberto_txt, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='ameaca', help='Ameaça alguém para não votar em outro')
async def ameaca_voto(ctx, ameacado: discord.User, *, descricao_ameaca: str):
    try:
        descoberta = random.choice([True, False, False])
        descoberta_txt = "🔍 DESCOBERTA!" if descoberta else "🤫 SEGREDO"
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ameacas_voto (
            id INTEGER PRIMARY KEY, ameacador_id INTEGER, ameacado_id INTEGER,
            ameaca TEXT, descoberta BOOLEAN DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO ameacas_voto (ameacador_id, ameacado_id, ameaca, descoberta) VALUES (?, ?, ?, ?)', 
                      (ctx.author.id, ameacado.id, descricao_ameaca, descoberta))
        conn.commit()
        conn.close()
        
        if descoberta:
            db.alterar_aprovacao(ctx.guild.id, -50)
        
        embed = discord.Embed(title="⚠️ AMEAÇA POLÍTICA", description=descricao_ameaca, color=discord.Color.red())
        embed.add_field(name="👤 Ameaçado", value=ameacado.mention, inline=True)
        embed.add_field(name="🔒 Status", value=descoberta_txt, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - PODER LOCAL / CIDADES
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='criarCidade', help='Cria uma cidade (Admin)')
@commands.has_permissions(administrator=True)
async def criar_cidade(ctx, *, info: str):
    try:
        partes = info.split('|')
        if len(partes) < 2:
            await ctx.send("❌ Formato: `!criarCidade Nome|Estado`")
            return
        
        nome = partes[0].strip()
        estado = partes[1].strip()
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cidades (
            id INTEGER PRIMARY KEY, nome TEXT UNIQUE, estado TEXT,
            populacao INTEGER DEFAULT 100000, pib INTEGER DEFAULT 100000000,
            prefeito_id INTEGER, vice_prefeito_id INTEGER,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        try:
            cursor.execute('INSERT INTO cidades (nome, estado) VALUES (?, ?)', (nome, estado))
            conn.commit()
            cidade_id = cursor.lastrowid
            
            embed = discord.Embed(title="✅ CIDADE CRIADA", description=f"**{nome}**", color=discord.Color.green())
            embed.add_field(name="🏙️ Nome", value=nome, inline=True)
            embed.add_field(name="📍 Estado", value=estado, inline=True)
            embed.add_field(name="👥 População", value="100.000", inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("❌ Cidade com este nome já existe!")
        conn.close()
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='elegerPrefeito', help='Elege prefeito de uma cidade')
async def eleger_prefeito(ctx, cidade_id: int):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('UPDATE cidades SET prefeito_id = ? WHERE id = ?', (ctx.author.id, cidade_id))
        conn.commit()
        
        cursor.execute('SELECT * FROM cidades WHERE id = ?', (cidade_id,))
        cidade = cursor.fetchone()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, 200)
        
        embed = discord.Embed(title="🏛️ PREFEITO ELEITO", description=f"Cidade: **{cidade['nome']}**", color=discord.Color.gold())
        embed.add_field(name="👤 Prefeito", value=ctx.author.mention, inline=True)
        embed.add_field(name="🏙️ Cidade", value=cidade['nome'], inline=True)
        embed.add_field(name="📍 Estado", value=cidade['estado'], inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='cidades', help='Lista todas as cidades')
async def listar_cidades(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cidades')
        cidades = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🗺️ MAPA DE CIDADES", description=f"Total de **{len(cidades)}** cidades", color=discord.Color.blue())
        
        if cidades:
            for cidade in cidades:
                try:
                    prefeito = await bot.fetch_user(cidade['prefeito_id'])
                    pref_nome = prefeito.name
                except:
                    pref_nome = "Vago"
                
                embed.add_field(name=f"🏙️ {cidade['nome']}", 
                               value=f"📍 Estado: {cidade['estado']}\n👥 População: {cidade['populacao']:,}\n💰 PIB: R$ {cidade['pib']:,}\n🏛️ Prefeito: {pref_nome}", 
                               inline=False)
        else:
            embed.description = "Nenhuma cidade criada ainda."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='orcamentoMunicipal', help='Mostra orçamento municipal')
async def orcamento_municipal(ctx, cidade_id: int):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orcamentos_municipais (
            id INTEGER PRIMARY KEY, cidade_id INTEGER UNIQUE,
            saude INTEGER DEFAULT 30, educacao INTEGER DEFAULT 30,
            infraestrutura INTEGER DEFAULT 20, seguranca INTEGER DEFAULT 20,
            total INTEGER DEFAULT 100
        )''')
        cursor.execute('SELECT * FROM orcamentos_municipais WHERE cidade_id = ?', (cidade_id,))
        orcamento = cursor.fetchone()
        
        if not orcamento:
            cursor.execute('INSERT INTO orcamentos_municipais (cidade_id) VALUES (?)', (cidade_id,))
            conn.commit()
            cursor.execute('SELECT * FROM orcamentos_municipais WHERE cidade_id = ?', (cidade_id,))
            orcamento = cursor.fetchone()
        
        conn.close()
        
        embed = discord.Embed(title="💰 ORÇAMENTO MUNICIPAL", description=f"Cidade #{cidade_id}", color=discord.Color.gold())
        embed.add_field(name="📊 DISTRIBUIÇÃO", value=f"Saúde:             {orcamento['saude']}%\nEducação:          {orcamento['educacao']}%\nInfraestrutura:    {orcamento['infraestrutura']}%\nSegurança:         {orcamento['seguranca']}%", inline=False)
        embed.add_field(name="✅ TOTAL", value="100%", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='vereador', help='Elege vereador municipal')
async def eleger_vereador(ctx, cidade_id: int):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vereadores (
            id INTEGER PRIMARY KEY, cidade_id INTEGER, vereador_id INTEGER,
            partido TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        filiacao = db.obter_filiacao(ctx.author.id)
        partido = filiacao['partido'] if filiacao else 'Independente'
        
        cursor.execute('INSERT INTO vereadores (cidade_id, vereador_id, partido) VALUES (?, ?, ?)', 
                      (cidade_id, ctx.author.id, partido))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, 100)
        
        embed = discord.Embed(title="✅ VEREADOR ELEITO", description=f"Cidade #{cidade_id}", color=discord.Color.green())
        embed.add_field(name="👤 Vereador", value=ctx.author.mention, inline=True)
        embed.add_field(name="🎯 Partido", value=partido, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='governador', help='Torna alguém governador de um estado')
async def eleger_governador(ctx, *, estado: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS governadores (
            id INTEGER PRIMARY KEY, estado TEXT UNIQUE,
            governador_id INTEGER, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        try:
            cursor.execute('INSERT OR REPLACE INTO governadores (estado, governador_id) VALUES (?, ?)', 
                          (estado, ctx.author.id))
            conn.commit()
            
            db.adicionar_prestige(ctx.author.id, 300)
            
            embed = discord.Embed(title="👑 GOVERNADOR ELEITO", description=f"Estado: **{estado.upper()}**", color=discord.Color.gold())
            embed.add_field(name="👤 Governador", value=ctx.author.mention, inline=True)
            embed.add_field(name="���� Estado", value=estado.upper(), inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("❌ Erro ao eleger governador!")
        conn.close()
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - CONSTITUIÇÃO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='constituicao', help='Mostra constituição')
async def mostra_constituicao(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS constituicao (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            titulo TEXT DEFAULT 'Constituição Federal',
            artigos TEXT DEFAULT '1. Democracia | 2. Igualdade | 3. Liberdade',
            emendas INTEGER DEFAULT 0
        )''')
        cursor.execute('SELECT * FROM constituicao WHERE servidor_id = ?', (ctx.guild.id,))
        const = cursor.fetchone()
        
        if not const:
            cursor.execute('INSERT INTO constituicao (servidor_id) VALUES (?)', (ctx.guild.id,))
            conn.commit()
            cursor.execute('SELECT * FROM constituicao WHERE servidor_id = ?', (ctx.guild.id,))
            const = cursor.fetchone()
        
        conn.close()
        
        embed = discord.Embed(title="📜 CONSTITUIÇÃO FEDERAL", description=const['titulo'], color=discord.Color.blue())
        embed.add_field(name="📝 ARTIGOS PRINCIPAIS", value=const['artigos'], inline=False)
        embed.add_field(name="🔄 Emendas", value=f"Total de **{const['emendas']}** emendas constitucionais", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='emendasConstitucionais', help='Propõe emenda constitucional')
async def propor_emenda(ctx, artigo: int, *, novo_texto: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 2000:
            await ctx.send("❌ Você precisa de 2000+ prestige para isso!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS emendas (
            id INTEGER PRIMARY KEY, propositor_id INTEGER, artigo INTEGER,
            novo_texto TEXT, votos_favor INTEGER DEFAULT 0,
            votos_contra INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO emendas (propositor_id, artigo, novo_texto) VALUES (?, ?, ?)', 
                      (ctx.author.id, artigo, novo_texto))
        conn.commit()
        emenda_id = cursor.lastrowid
        
        cursor.execute('UPDATE constituicao SET emendas = emendas + 1 WHERE servidor_id = ?', (ctx.guild.id,))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, -100)
        
        embed = discord.Embed(title="📜 EMENDA CONSTITUCIONAL PROPOSTA", description=f"Artigo {artigo}", color=discord.Color.blue())
        embed.add_field(name="👤 Propositor", value=ctx.author.mention, inline=True)
        embed.add_field(name="ID", value=emenda_id, inline=True)
        embed.add_field(name="📝 Novo Texto", value=novo_texto, inline=False)
        embed.add_field(name="🗳️ Status", value="Em votação!", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='votarEmenda', help='Vota em emenda constitucional')
async def votar_emenda(ctx, emenda_id: int, voto: str):
    try:
        if voto.lower() not in ['sim', 'não']:
            await ctx.send("❌ Vote com: sim ou não")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        
        if voto.lower() == 'sim':
            cursor.execute('UPDATE emendas SET votos_favor = votos_favor + 1 WHERE id = ?', (emenda_id,))
            voto_txt = "SIM ✅"
        else:
            cursor.execute('UPDATE emendas SET votos_contra = votos_contra + 1 WHERE id = ?', (emenda_id,))
            voto_txt = "NÃO ❌"
        
        conn.commit()
        cursor.execute('SELECT * FROM emendas WHERE id = ?', (emenda_id,))
        emenda = cursor.fetchone()
        conn.close()
        
        embed = discord.Embed(title="✅ VOTO REGISTRADO", description=f"Emenda #{emenda_id}", color=discord.Color.green())
        embed.add_field(name="🗳️ Voto", value=voto_txt, inline=True)
        embed.add_field(name="📊 Placar", value=f"✅ {emenda['votos_favor']} vs ❌ {emenda['votos_contra']}", inline=True)
        db.adicionar_prestige(ctx.author.id, 10)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - GABINETE MINISTERIAL
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='gabinete', help='Mostra gabinete ministerial')
async def mostra_gabinete(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS gabinete (
            id INTEGER PRIMARY KEY, cargo TEXT UNIQUE,
            ocupante_id INTEGER, data_posse TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('SELECT * FROM gabinete')
        cargos = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="👑 GABINETE PRESIDENCIAL", description="Ministérios e cargos de confiança", color=discord.Color.gold())
        
        if cargos:
            for cargo in cargos:
                try:
                    ministro = await bot.fetch_user(cargo['ocupante_id'])
                    ministro_nome = ministro.name
                except:
                    ministro_nome = "Vago"
                
                embed.add_field(name=f"📋 {cargo['cargo'].upper()}", value=f"Ministro: {ministro_nome}", inline=False)
        else:
            embed.description = "Gabinete vazio! Nenhum ministério preenchido."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='nomeiarMinistro', help='Nomeia um ministro (Admin)')
@commands.has_permissions(administrator=True)
async def nomear_ministro(ctx, ministro: discord.User, *, cargo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO gabinete (cargo, ocupante_id) VALUES (?, ?)', 
                      (cargo, ministro.id))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ministro.id, 200)
        
        embed = discord.Embed(title="✅ MINISTRO NOMEADO", description=f"**{cargo}**", color=discord.Color.green())
        embed.add_field(name="👤 Ministro", value=ministro.mention, inline=True)
        embed.add_field(name="📋 Cargo", value=cargo.upper(), inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='mocao', help='Propõe moção de desconfiança')
async def moção_desconfiança(ctx, alvo: discord.User, *, motivo: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 500:
            await ctx.send("❌ Você precisa de 500+ prestige para isso!")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS mocoes (
            id INTEGER PRIMARY KEY, alvo_id INTEGER, propositor_id INTEGER,
            motivo TEXT, votos_favor INTEGER DEFAULT 0,
            votos_contra INTEGER DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO mocoes (alvo_id, propositor_id, motivo) VALUES (?, ?, ?)', 
                      (alvo.id, ctx.author.id, motivo))
        conn.commit()
        mocao_id = cursor.lastrowid
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, -20)
        
        embed = discord.Embed(title="⚠️ MOÇÃO DE DESCONFIANÇA", description=motivo, color=discord.Color.red())
        embed.add_field(name="🎯 Alvo", value=alvo.mention, inline=True)
        embed.add_field(name="👤 Propositor", value=ctx.author.mention, inline=True)
        embed.add_field(name="🗳️ Status", value="Em votação no congresso!", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='impeachment', help='Inicia processo de impeachment (Admin)')
@commands.has_permissions(administrator=True)
async def impeachment_cmd(ctx, presidente: discord.User, *, motivo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS impeachments (
            id INTEGER PRIMARY KEY, presidente_id INTEGER, motivo TEXT,
            votos_favor INTEGER DEFAULT 0, votos_contra INTEGER DEFAULT 0,
            status TEXT DEFAULT 'em_votacao', data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO impeachments (presidente_id, motivo) VALUES (?, ?)', 
                      (presidente.id, motivo))
        conn.commit()
        impeach_id = cursor.lastrowid
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, -50)
        
        embed = discord.Embed(title="🚨 IMPEACHMENT INICIADO", description=f"Presidente: **{presidente.name}**", color=discord.Color.dark_red())
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="🗳️ Status", value="Em votação no Senado", inline=False)
        embed.add_field(name="⚠️ ALERTA", value="Crise constitucional extrema!", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - CANCELAMENTO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='cancelar', help='Cancela alguém nas redes sociais')
async def cancelamento(ctx, alvo: discord.User, *, motivo: str):
    try:
        severidade = random.uniform(20, 100)
        seguidores_perdidos = random.randint(10000, 1000000)
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cancelamentos (
            id INTEGER PRIMARY KEY, alvo_id INTEGER, cancelador_id INTEGER,
            motivo TEXT, severidade REAL, seguidores_perdidos INTEGER,
            resolvido BOOLEAN DEFAULT 0, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO cancelamentos (alvo_id, cancelador_id, motivo, severidade, seguidores_perdidos) VALUES (?, ?, ?, ?, ?)', 
                      (alvo.id, ctx.author.id, motivo, severidade, seguidores_perdidos))
        conn.commit()
        cancelamento_id = cursor.lastrowid
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, -random.uniform(10, 30))
        
        embed = discord.Embed(title="🚫 CANCELAMENTO", description=motivo, color=discord.Color.red())
        embed.add_field(name="🎯 Alvo", value=alvo.mention, inline=True)
        embed.add_field(name="📱 Seguidores Perdidos", value=f"{seguidores_perdidos:,}", inline=True)
        embed.add_field(name="📊 Severidade", value=f"{severidade:.0f}%", inline=True)
        embed.add_field(name="🌍 Viralidade", value="EM TODO O TWITTER", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='meme', help='Cria meme ridicularizador')
async def criar_meme(ctx, alvo: discord.User, *, descricao: str):
    try:
        viralidade = random.randint(10000, 5000000)
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS memes (
            id INTEGER PRIMARY KEY, alvo_id INTEGER, criador_id INTEGER,
            descricao TEXT, viralidade INTEGER, compartilhamentos INTEGER,
            impacto_carisma REAL DEFAULT -10.0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO memes (alvo_id, criador_id, descricao, viralidade, compartilhamentos) VALUES (?, ?, ?, ?, ?)', 
                      (alvo.id, ctx.author.id, descricao, viralidade, random.randint(1000, 50000)))
        conn.commit()
        meme_id = cursor.lastrowid
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, 50)
        
        embed = discord.Embed(title="😂 MEME CRIADO", description=descricao, color=discord.Color.green())
        embed.add_field(name="🎯 Sobre", value=alvo.mention, inline=True)
        embed.add_field(name="📱 Viralidade", value=f"{viralidade:,} visualizações", inline=True)
        embed.add_field(name="⚠️ Impacto", value="-10% Carisma do alvo", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - TWITTER AVANÇADO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='curtirTweet', help='Curte um tweet')
async def curtir_tweet(ctx, tweet_id: int):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('UPDATE tweets SET likes = likes + 1 WHERE id = ?', (tweet_id,))
        conn.commit()
        
        cursor.execute('SELECT * FROM tweets WHERE id = ?', (tweet_id,))
        tweet = cursor.fetchone()
        conn.close()
        
        embed = discord.Embed(title="❤️ TWEET CURTIDO", description=tweet['conteudo'][:200], color=discord.Color.red())
        embed.add_field(name="❤️ Likes", value=tweet['likes'], inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='retweet', help='Faz retweet')
async def retweet_cmd(ctx, tweet_id: int):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS retweets (
            id INTEGER PRIMARY KEY, tweet_id INTEGER, retweitador_id INTEGER,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO retweets (tweet_id, retweitador_id) VALUES (?, ?)', (tweet_id, ctx.author.id))
        conn.commit()
        
        cursor.execute('SELECT * FROM tweets WHERE id = ?', (tweet_id,))
        tweet = cursor.fetchone()
        conn.close()
        
        embed = discord.Embed(title="🔄 RETWEET", description=tweet['conteudo'][:200], color=discord.Color.green())
        embed.add_field(name="👤 Autor Original", value=f"<@{tweet['autor_id']}>", inline=True)
        embed.add_field(name="🔄 Retweetado por", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='responderTweet', help='Responde um tweet')
async def responder_tweet(ctx, tweet_id: int, *, resposta: str):
    try:
        if len(resposta) > 280:
            await ctx.send("❌ Resposta muito longa! Máximo 280 caracteres")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY, tweet_id INTEGER, respondente_id INTEGER,
            resposta TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO replies (tweet_id, respondente_id, resposta) VALUES (?, ?, ?)', 
                      (tweet_id, ctx.author.id, resposta))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="💬 RESPOSTA POSTADA", description=resposta, color=discord.Color.blue())
        embed.add_field(name="👤 Respondente", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='meusTweets', help='Mostra seus tweets')
async def meus_tweets(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tweets WHERE autor_id = ? ORDER BY id DESC LIMIT 5', (ctx.author.id,))
        tweets = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="📱 MEUS TWEETS", description=f"Total de **{len(tweets)}** tweets", color=discord.Color.blue())
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        
        if tweets:
            for tweet in tweets:
                embed.add_field(name=f"Tweet #{tweet['id']}", value=f"{tweet['conteudo']}\n❤️ {tweet['likes']} likes", inline=False)
        else:
            embed.description = "Você ainda não postou nenhum tweet."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='discurso', help='Faz um discurso político')
async def fazer_discurso(ctx, *, conteudo: str):
    try:
        if len(conteudo) > 500:
            await ctx.send("❌ Discurso muito longo! Máximo 500 caracteres")
            return
        
        impacto = random.uniform(-30, 50)
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS discursos (
            id INTEGER PRIMARY KEY, autor_id INTEGER, conteudo TEXT,
            impacto_aprovacao REAL, audiencia INTEGER DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO discursos (autor_id, conteudo, impacto_aprovacao) VALUES (?, ?, ?)', 
                      (ctx.author.id, conteudo, impacto))
        conn.commit()
        discurso_id = cursor.lastrowid
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, impacto)
        db.adicionar_prestige(ctx.author.id, int(abs(impacto) / 2))
        
        impacto_txt = f"+{impacto:.0f}%" if impacto > 0 else f"{impacto:.0f}%"
        
        embed = discord.Embed(title="🎤 DISCURSO POLÍTICO", description=conteudo, color=discord.Color.purple())
        embed.add_field(name="👤 Orador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📈 Impacto", value=impacto_txt, inline=True)
        embed.add_field(name="🎤 Audiência", value="Transmitido ao vivo", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - LIDER OPOSIÇÃO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='liderOposicao', help='Mostra líder da oposição')
async def mostra_lider_oposicao(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lider_oposicao (
            id INTEGER PRIMARY KEY, servidor_id INTEGER UNIQUE,
            lider_id INTEGER, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('SELECT * FROM lider_oposicao WHERE servidor_id = ?', (ctx.guild.id,))
        lider = cursor.fetchone()
        conn.close()
        
        if not lider or not lider['lider_id']:
            await ctx.send("❌ Nenhum líder de oposição eleito!")
            return
        
        try:
            user = await bot.fetch_user(lider['lider_id'])
            lider_nome = user.name
        except:
            lider_nome = "Desconhecido"
        
        embed = discord.Embed(title="🔴 LÍDER DA OPOSIÇÃO", color=discord.Color.red())
        embed.add_field(name="👤 Líder", value=lider_nome, inline=True)
        embed.add_field(name="🎯 Função", value="Aglutinar críticas ao governo", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='elegerLiderOposicao', help='Elege líder da oposição')
async def eleger_lider_oposicao(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO lider_oposicao (servidor_id, lider_id) VALUES (?, ?)', 
                      (ctx.guild.id, ctx.author.id))
        conn.commit()
        conn.close()
        
        db.adicionar_prestige(ctx.author.id, 300)
        
        embed = discord.Embed(title="✅ LÍDER DA OPOSIÇÃO ELEITO", description=f"**{ctx.author.name}**", color=discord.Color.red())
        embed.add_field(name="👤 Líder", value=ctx.author.mention, inline=True)
        embed.add_field(name="🎯 Responsabilidade", value="Criticar e questionar o governo", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - REFERENDO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='referendo', help='Abre referendo popular')
async def abrir_referendo(ctx, *, info: str):
    try:
        partes = info.split('|')
        if len(partes) < 2:
            await ctx.send("❌ Formato: `!referendo Tema|Descrição`")
            return
        
        tema = partes[0].strip()
        descricao = partes[1].strip()
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS referendos (
            id INTEGER PRIMARY KEY, tema TEXT, descricao TEXT,
            propositor_id INTEGER, votos_sim INTEGER DEFAULT 0,
            votos_nao INTEGER DEFAULT 0, status TEXT DEFAULT 'aberto',
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO referendos (tema, descricao, propositor_id) VALUES (?, ?, ?)', 
                      (tema, descricao, ctx.author.id))
        conn.commit()
        referendo_id = cursor.lastrowid
        conn.close()
        
        embed = discord.Embed(title="🗳️ REFERENDO POPULAR", description=tema, color=discord.Color.blue())
        embed.add_field(name="📝 Descrição", value=descricao, inline=False)
        embed.add_field(name="👤 Propositor", value=ctx.author.mention, inline=True)
        embed.add_field(name="ID", value=referendo_id, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='votarReferendo', help='Vota em referendo')
async def votar_referendo(ctx, referendo_id: int, voto: str):
    try:
        if voto.lower() not in ['sim', 'não']:
            await ctx.send("❌ Vote com: sim ou não")
            return
        
        conn = db.conexao()
        cursor = conn.cursor()
        
        if voto.lower() == 'sim':
            cursor.execute('UPDATE referendos SET votos_sim = votos_sim + 1 WHERE id = ?', (referendo_id,))
            voto_txt = "SIM ✅"
        else:
            cursor.execute('UPDATE referendos SET votos_nao = votos_nao + 1 WHERE id = ?', (referendo_id,))
            voto_txt = "NÃO ❌"
        
        conn.commit()
        cursor.execute('SELECT * FROM referendos WHERE id = ?', (referendo_id,))
        referendo = cursor.fetchone()
        conn.close()
        
        embed = discord.Embed(title="✅ VOTO REGISTRADO", description=f"Referendo #{referendo_id}", color=discord.Color.green())
        embed.add_field(name="🗳️ Voto", value=voto_txt, inline=True)
        embed.add_field(name="📊 Placar", value=f"✅ {referendo['votos_sim']} vs ❌ {referendo['votos_nao']}", inline=True)
        db.adicionar_prestige(ctx.author.id, 10)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")
        # ═══════════════════════════════════════════════════════════════════
# COMANDOS - GOLPE DE ESTADO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='golpe', help='Inicia golpe de estado (Drama MÁXIMO)')
async def golpe_estado(ctx, *, descricao: str):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        if prestige['pontos'] < 5000:
            await ctx.send("❌ Você precisa de 5000+ prestige para isso!")
            return
        
        sucesso = random.choice([True, False])
        resistencia = random.randint(0, 100)
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS golpes (
            id INTEGER PRIMARY KEY, conspirador_id INTEGER, descricao TEXT,
            sucesso BOOLEAN, resistencia INTEGER, novo_presidente_id INTEGER,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('INSERT INTO golpes (conspirador_id, descricao, sucesso, resistencia, novo_presidente_id) VALUES (?, ?, ?, ?, ?)', 
                      (ctx.author.id, descricao, sucesso, resistencia, ctx.author.id if sucesso else None))
        conn.commit()
        golpe_id = cursor.lastrowid
        conn.close()
        
        if sucesso:
            db.adicionar_prestige(ctx.author.id, 1000)
            db.alterar_aprovacao(ctx.guild.id, -100)
            resultado = "✅ GOLPE BEM-SUCEDIDO!"
            cor = discord.Color.dark_red()
        else:
            db.adicionar_prestige(ctx.author.id, -2000)
            db.alterar_aprovacao(ctx.guild.id, -50)
            resultado = "❌ GOLPE FRACASSOU!"
            cor = discord.Color.red()
        
        embed = discord.Embed(title="⚡ GOLPE DE ESTADO", description=descricao, color=cor)
        embed.add_field(name="👤 Conspirador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📋 Resultado", value=resultado, inline=True)
        embed.add_field(name="🪖 Resistência", value=f"{resistencia}%", inline=True)
        embed.add_field(name="🚨 STATUS", value="CAOS TOTAL NA NAÇÃO", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - LINHA DE SUCESSÃO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='linhaSuccessao', help='Mostra linha de sucessão')
async def linha_sucessao(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sucessao (
            id INTEGER PRIMARY KEY, servidor_id INTEGER, posicao INTEGER,
            membro_id INTEGER, cargo TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        cursor.execute('SELECT * FROM sucessao WHERE servidor_id = ? ORDER BY posicao ASC', (ctx.guild.id,))
        sucessores = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="👑 LINHA DE SUCESSÃO PRESIDENCIAL", description="Ordem de sucessão", color=discord.Color.gold())
        
        if sucessores:
            for sucessor in sucessores:
                try:
                    user = await bot.fetch_user(sucessor['membro_id'])
                    membro_nome = user.name
                except:
                    membro_nome = "Vago"
                
                emoji_pos = {1: "🥇", 2: "🥈", 3: "🥉"}
                emoji = emoji_pos.get(sucessor['posicao'], f"{sucessor['posicao']}.")
                
                embed.add_field(name=f"{emoji} Posição {sucessor['posicao']}", value=f"👤 {membro_nome}\n📋 {sucessor['cargo']}", inline=False)
        else:
            embed.description = "Nenhum sucessor registrado."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='adicionarSuccessor', help='Adiciona alguém na linha de sucessão (Admin)')
@commands.has_permissions(administrator=True)
async def adicionar_sucessor(ctx, posicao: int, usuario: discord.User, *, cargo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sucessao (servidor_id, posicao, membro_id, cargo) VALUES (?, ?, ?, ?)', 
                      (ctx.guild.id, posicao, usuario.id, cargo))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="✅ SUCESSOR ADICIONADO", description=f"Posição {posicao}", color=discord.Color.green())
        embed.add_field(name="👤 Sucessor", value=usuario.mention, inline=True)
        embed.add_field(name="📋 Cargo", value=cargo, inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - ALIANÇA INTERNACIONAL
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='criarAlianca', help='Cria aliança internacional (Admin)')
@commands.has_permissions(administrator=True)
async def criar_alianca(ctx, *, nome: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS aliancas (
            id INTEGER PRIMARY KEY, nome TEXT UNIQUE, tipo TEXT DEFAULT 'militar',
            descricao TEXT, membros TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        try:
            cursor.execute('INSERT INTO aliancas (nome) VALUES (?)', (nome,))
            conn.commit()
            alianca_id = cursor.lastrowid
            
            embed = discord.Embed(title="✅ ALIANÇA CRIADA", description=f"**{nome}**", color=discord.Color.green())
            embed.add_field(name="🌍 Nome", value=nome, inline=True)
            embed.add_field(name="ID", value=alianca_id, inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("❌ Aliança com este nome já existe!")
        conn.close()
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='aliancas', help='Lista aliações internacionais')
async def listar_aliancas(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM aliancas')
        aliancas = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🌍 ALIANÇAS INTERNACIONAIS", description=f"Total de **{len(aliancas)}** alianças", color=discord.Color.blue())
        
        if aliancas:
            for alianca in aliancas:
                embed.add_field(name=f"🤝 {alianca['nome']}", value=f"Tipo: {alianca['tipo'].upper()}\nDescrição: {alianca['descricao'] or 'N/A'}", inline=False)
        else:
            embed.description = "Nenhuma aliança criada."
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - VETO PRESIDENCIAL
# ═════════���═════════════════════════════════════════════════════════

@bot.command(name='vetarLei', help='Veta uma lei (Presidente)')
async def vetar_lei(ctx, lei_id: int, *, motivo: str):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vetos (
            id INTEGER PRIMARY KEY, lei_id INTEGER, presidente_id INTEGER,
            motivo TEXT, data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            votos_derrota INTEGER DEFAULT 0
        )''')
        cursor.execute('INSERT INTO vetos (lei_id, presidente_id, motivo) VALUES (?, ?, ?)', 
                      (lei_id, ctx.author.id, motivo))
        conn.commit()
        veto_id = cursor.lastrowid
        conn.close()
        
        db.alterar_aprovacao(ctx.guild.id, -20)
        
        embed = discord.Embed(title="🚫 VETO PRESIDENCIAL", description=f"Lei #{lei_id}", color=discord.Color.red())
        embed.add_field(name="👤 Presidente", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="⚠️ Status", value="Pode ser derrubado no congresso!", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - APOSENTADORIA E LEGADO
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='aposentar', help='Se aposenta da política')
async def se_aposentar(ctx):
    try:
        prestige = db.obter_prestige(ctx.author.id)
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS aposentados (
            id INTEGER PRIMARY KEY, politico_id INTEGER, prestige_final INTEGER,
            data_aposentadoria TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pensao_mensal INTEGER DEFAULT 0
        )''')
        cursor.execute('INSERT INTO aposentados (politico_id, prestige_final, pensao_mensal) VALUES (?, ?, ?)', 
                      (ctx.author.id, prestige['pontos'], prestige['pontos'] // 100))
        conn.commit()
        conn.close()
        
        embed = discord.Embed(title="🎖️ APOSENTADORIA POLÍTICA", description=f"**{ctx.author.name}** se aposenta", color=discord.Color.gold())
        embed.add_field(name="👤 Político", value=ctx.author.mention, inline=True)
        embed.add_field(name="⭐ Prestige Final", value=prestige['pontos'], inline=True)
        embed.add_field(name="💰 Pensão Mensal", value=f"R$ {prestige['pontos'] // 100:,}", inline=True)
        embed.add_field(name="🎖️ Legado", value="Seu nome ficar na história!", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='legado', help='Mostra legado político')
async def mostra_legado(ctx, usuario: discord.User = None):
    try:
        if usuario is None:
            usuario = ctx.author
        
        prestige = db.obter_prestige(usuario.id)
        
        if prestige['pontos'] < 100:
            legado_status = "Iniciante"
        elif prestige['pontos'] < 500:
            legado_status = "Político Promissor"
        elif prestige['pontos'] < 1000:
            legado_status = "Político Consolidado"
        elif prestige['pontos'] < 2000:
            legado_status = "Estadista Respeitado"
        else:
            legado_status = "Lenda Política"
        
        embed = discord.Embed(title="🏛️ LEGADO POLÍTICO", color=discord.Color.gold())
        embed.set_author(name=usuario.name, icon_url=usuario.display_avatar)
        embed.add_field(name="⭐ Prestige", value=prestige['pontos'], inline=True)
        embed.add_field(name="📊 Status", value=legado_status, inline=True)
        embed.add_field(name="📖 Lugar na História", value="A ser definido...", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# COMANDOS - ESTATÍSTICAS E RANKINGS
# ═══════════════════════════════════════════════════════════════════

@bot.command(name='topPrestige', help='Top 10 maior prestige')
async def top_prestige(ctx):
    try:
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM prestige ORDER BY pontos DESC LIMIT 10')
        tops = cursor.fetchall()
        conn.close()
        
        embed = discord.Embed(title="🏆 TOP 10 - MAIOR PRESTIGE", color=discord.Color.gold())
        
        if tops:
            for i, top in enumerate(tops, 1):
                try:
                    user = await bot.fetch_user(top['user_id'])
                    nome = user.name
                except:
                    nome = "Desconhecido"
                
                medalha = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                embed.add_field(name=f"{medalha} {nome}", value=f"⭐ {top['pontos']} pontos", inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='statusServidor', help='Status geral do servidor')
async def status_servidor(ctx):
    try:
        aprovacao = db.obter_aprovacao(ctx.guild.id)
        
        conn = db.conexao()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as total FROM personagens')
        total_personagens = cursor.fetchone()['total']
        cursor.execute('SELECT SUM(pontos) as total FROM prestige')
        total_prestige = cursor.fetchone()['total'] or 0
        conn.close()
        
        if aprovacao['taxa'] >= 75:
            status_gov = "🟢 ESTÁVEL"
        elif aprovacao['taxa'] >= 50:
            status_gov = "🟡 INSTÁVEL"
        elif aprovacao['taxa'] >= 25:
            status_gov = "🔴 CRÍTICO"
        else:
            status_gov = "💀 CAÓTICO"
        
        embed = discord.Embed(title="📊 STATUS DO SERVIDOR", description=f"Servidor: **{ctx.guild.name}**", color=discord.Color.blue())
        embed.add_field(name="👥 Personagens", value=total_personagens, inline=True)
        embed.add_field(name="⭐ Prestige Total", value=total_prestige, inline=True)
        embed.add_field(name="📊 Aprovação", value=f"{aprovacao['taxa']:.1f}%", inline=True)
        embed.add_field(name="🏛️ Status do Governo", value=status_gov, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

# ═══════════════════════════════════════════════════════════════════
# RODAR BOT - FINAL
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    TOKEN = "MTQ4Mjk5OTc5NzMwNzY3NDcxNg.GHVqRu.iLYrkXip0ZqLHm6RxvxVwxpFV1OS5NFGw-dlz4"

    print("\n" + "="*100)
    print("🇧🇷 ULTRA MEGA PACOTE FINAL DEFINITIVO COMPLETO")
    print("Sistema de Governo RP Brasil - 250+ Comandos - 80+ Tabelas")
    print("IA Automática | Twitter | Filhos & Herança | Morte & Legado")
    print("Fake News | Escândalos | Debates | Revolução | Golpe de Estado")
    print("E MUITO MAIS!")
    print("="*100 + "\n")

    print("🚀 INICIANDO BOT...")
    print("⌛ Conectando ao Discord...")

    bot.run(TOKEN)