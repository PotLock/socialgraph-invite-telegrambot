import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import sqlite3
import os

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Use environment variable for the bot token
bot = telebot.TeleBot(API_TOKEN)

# Database setup
def init_db():
    with sqlite3.connect('builder_votes.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS builders
                     (name TEXT, last_proposed DATE, votes INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS daily_stats
                     (date DATE, proposals_left INTEGER)''')
        conn.commit()

def get_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Vote For", callback_data="vote_for"),
                 InlineKeyboardButton("Vote Against", callback_data="vote_against"))
    return keyboard

def get_proposals_left(today):
    with sqlite3.connect('builder_votes.db') as conn:
        c = conn.cursor()
        c.execute("SELECT proposals_left FROM daily_stats WHERE date=?", (today,))
        return c.fetchone()

@bot.message_handler(commands=['propose_builder'])
def propose_builder(message):
    today = datetime.now().date()
    result = get_proposals_left(today)
    
    if result and result[0] > 0:
        builder_name = message.text.split(' ', 1)[1]
        with sqlite3.connect('builder_votes.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM builders WHERE name=? AND last_proposed=?", (builder_name, today))
            if c.fetchone():
                bot.reply_to(message, "Error: A poll for this builder already exists today.")
            else:
                c.execute("INSERT INTO builders (name, last_proposed, votes) VALUES (?, ?, 0)", (builder_name, today))
                c.execute("UPDATE daily_stats SET proposals_left = proposals_left - 1 WHERE date=?", (today,))
                conn.commit()
                
                poll_message = f"Vote for builder: {builder_name}"
                bot.send_message(message.chat.id, poll_message, reply_markup=get_keyboard())
    else:
        bot.reply_to(message, "No more proposals allowed today.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    builder_name = call.message.text.split(': ')[1]
    with sqlite3.connect('builder_votes.db') as conn:
        c = conn.cursor()
        if call.data == "vote_for":
            c.execute("UPDATE builders SET votes = votes + 1 WHERE name=?", (builder_name,))
        elif call.data == "vote_against":
            c.execute("UPDATE builders SET votes = votes - 1 WHERE name=?", (builder_name,))
        conn.commit()
    bot.answer_callback_query(call.id, "Vote recorded!")

@bot.message_handler(commands=['generate_invite'])
def generate_invite(message):
    today = datetime.now().date()
    with sqlite3.connect('builder_votes.db') as conn:
        c = conn.cursor()
        c.execute("SELECT name, votes FROM builders WHERE last_proposed=?", (today,))
        results = c.fetchall()
        
        for builder, votes in results:
            if votes > 0:  # Assuming threshold is 1 for simplicity
                invite_link = bot.create_chat_invite_link(message.chat.id).invite_link
                bot.reply_to(message, f"Invite link for {builder}: {invite_link}")
            else:
                bot.reply_to(message, f"Not enough votes for {builder}.")

@bot.message_handler(commands=['increment_daily_count'])
def increment_daily_count(message):
    today = datetime.now().date()
    with sqlite3.connect('builder_votes.db') as conn:
        c = conn.cursor()
        c.execute("UPDATE daily_stats SET proposals_left = proposals_left + 1 WHERE date=?", (today,))
        conn.commit()
    bot.reply_to(message, "Daily builder invite count incremented.")

# Run daily reset
def daily_reset():
    today = datetime.now().date()
    with sqlite3.connect('builder_votes.db') as conn:
        c = conn.cursor()
        c.execute("DELETE FROM builders WHERE last_proposed<?", (today,))
        c.execute("INSERT OR REPLACE INTO daily_stats (date, proposals_left) VALUES (?, 1)", (today,))
        conn.commit()

# Initialize database and run the bot
if __name__ == "__main__":
    init_db()
    daily_reset()
    bot.polling()
