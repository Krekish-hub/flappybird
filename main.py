import telebot
import psycopg2
from telebot.async_telebot import AsyncTeleBot
import asyncio

API_TOKEN = '7951627550:AAEAvW2yU7I2oL2HEobM45gIkptRZWKx1Y8'
WEB_APP_URL = 'https://krekish-hub.github.io/flappyy/'

bot = AsyncTeleBot(API_TOKEN)

def init_db():
    connection = psycopg2.connect(dbname='datab', user='postgres', password='1', host='localhost', port=5432)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE,
            name TEXT NOT NULL,
            record INTEGER DEFAULT 0
        )
    ''')
    connection.commit()
    cursor.close()
    connection.close()

@bot.message_handler(commands=['start'])
async def start(message):
    connection = psycopg2.connect(dbname='datab', user='postgres', password='1', host='localhost', port=5432)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO users (user_id, name)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO NOTHING
    ''', (message.from_user.id, message.from_user.first_name))
    connection.commit()
    cursor.close()
    connection.close()

    await bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Ваш аккаунт создан в базе данных.")

@bot.message_handler(commands=['play'])
async def play_game(message):
    user_id = message.from_user.id
    await bot.send_message(
        message.chat.id,
        "Нажмите на ссылку, чтобы начать игру Flappy Bird!",
        reply_markup=telebot.types.InlineKeyboardMarkup().add(
            telebot.types.InlineKeyboardButton("Играть", url=f"{WEB_APP_URL}?userId={user_id}")
        )
    )

init_db()
asyncio.run(bot.polling())
