import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import threading
import time
from datetime import datetime, timedelta

# ==========================================
# ⚙️ SUAS CONFIGURAÇÕES
# ==========================================
BOT_TOKEN = '8987873672:AAEZWHValZ7a0_pR9n7QsGo5v98t3gQ-6gY'          # Insira o Token do seu Bot
BOT_USERNAME = 'T33sty67bot'           # Nome do seu bot SEM O @

# 🚀 LISTA DE GRUPOS ONDE O BOT VAI DIVULGAR:
GRUPOS_PUBLICOS_IDS = [
    '-1003962069382',   # SVB PRÉVIAS
    '-1003959804103',   # GRUPO NV TD DIA
    '-1004316226762',   # SEM LIMITES
    '-1003755823081'    # PVTARIA ON 🔥
]

# 🔒 GRUPO VIP DE DESTINO (ONDE O USUÁRIO FICA 10 MINUTOS):
GRUPO_VIP_ID = '-1004391882200'       # ID do seu Grupo VIP

INTERVALO_PROPAGANDA_MINUTOS = 5      # Mensagem enviada a cada 5 minutos
# ==========================================

bot = telebot.TeleBot(BOT_TOKEN)
DB_FILE = 'controle_teste_vip.json'

# --- BANCO DE DADOS LOCAL ---
def carregar_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"historico": [], "ativos": {}}

def salvar_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

# --- 1. DIVULGAÇÃO AUTOMÁTICA EM TODOS OS GRUPOS ---
def enviar_propaganda():
    while True:
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton("🔥 Testar VIP por 10 Minutos", url=f"https://t.me/{BOT_USERNAME}?start=teste")
        markup.add(btn)
        
        for grupo_id in GRUPOS_PUBLICOS_IDS:
            try:
                bot.send_message(
                    grupo_id, 
                    "🚨 *Acesso VIP Liberado Temporariamente!*\n\nClique no botão abaixo para ganhar 10 minutos de acesso gratuito. Válido apenas 1 vez por conta.", 
                    reply_markup=markup,
                    parse_mode="Markdown"
                )
                print(f"Propaganda enviada para o grupo: {grupo_id}")
            except Exception as e:
                print(f"Erro ao enviar para o grupo {grupo_id}: {e}")
            
            time.sleep(2)
            
        time.sleep(INTERVALO_PROPAGANDA_MINUTOS * 60)

# --- 2. RECEPÇÃO NO PRIVADO E ENTREGA DO LINK ---
@bot.message_handler(commands=['start'])
def processar_teste(message):
    texto = message.text
    user_id = str(message.chat.id)
    
    if texto == '/start teste':
        db = carregar_db()
        
        if user_id in db['historico']:
            bot.send_message(user_id, "❌ Você já utilizou o seu limite de teste gratuito de 10 minutos nesta conta.")
            return
            
        try:
            convite = bot.create_chat_invite_link(chat_id=GRUPO_VIP_ID, member_limit=1)
            link = convite.invite_link
            
            expiracao = (datetime.now() + timedelta(minutes=10)).timestamp()
            
            db['historico'].append(user_id)
            db['ativos'][user_id] = expiracao
            salvar_db(db)
            
            bot.send_message(
                user_id,
                f"✅ *Seu acesso teste foi gerado com sucesso!*\n\n"
                f"Você tem exatos **10 minutos** a partir de agora para aproveitar o grupo VIP.\n\n"
                f"🔗 Link de Acesso: {link}\n\n"
                f"_(Este link só pode ser usado 1 vez)_",
                parse_mode="Markdown"
            )
            print(f"Teste de 10 min liberado para o ID: {user_id}")
            
        except Exception as e:
            bot.send_message(user_id, "Erro ao gerar seu acesso. Certifique-se de que o bot é Administrador do Grupo VIP.")
            print(f"Erro na criação do link: {e}")

# --- 3. INSPETOR (EXPULSA APÓS 10 MINUTOS) ---
def vigia_de_expulsao():
    while True:
        db = carregar_db()
        agora = datetime.now().timestamp()
        usuarios_vencidos = []
        
        for user_id, tempo_expiracao in db['ativos'].items():
            if agora > tempo_expiracao:
                try:
                    bot.ban_chat_member(GRUPO_VIP_ID, int(user_id))
                    bot.unban_chat_member(GRUPO_VIP_ID, int(user_id))
                    
                    bot.send_message(int(user_id), "⏳ Seus 10 minutos de teste no VIP acabaram! Espero que tenha gostado da experiência.")
                    print(f"Usuário {user_id} removido do VIP por tempo esgotado.")
                except Exception as e:
                    print(f"Erro ao remover usuário {user_id}: {e}")
                
                usuarios_vencidos.append(user_id)
        
        if usuarios_vencidos:
            for u in usuarios_vencidos:
                del db['ativos'][u]
            salvar_db(db)
            
        time.sleep(15)

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == '__main__':
    threading.Thread(target=enviar_propaganda, daemon=True).start()
    threading.Thread(target=vigia_de_expulsao, daemon=True).start()
    
    print("Bot otimizado e rodando em todos os grupos...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
