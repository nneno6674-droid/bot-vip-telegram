import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os
import threading
import time
from datetime import datetime, timedelta
import http.server
import socketserver

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

# Dicionário para armazenar o ID da última mensagem enviada em cada grupo
mensagens_anteriores = {}

# --- MINI SERVIDOR WEB PARA LIBERAR PLANO 100% GRATUITO NO RENDER ---
def rodar_servidor_web():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"Servidor web: {e}")

# --- BANCO DE DADOS LOCAL ---
def carregar_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"historico": [], "ativos": {}}

def salvar_db(db):
    with open(DB_FILE, 'w') as f:
        json.dump(db, f)

# --- 1. DIVULGAÇÃO AUTOMÁTICA EM TODOS OS GRUPOS (COM AUTO-DELETAR) ---
def enviar_propaganda():
    while
    
