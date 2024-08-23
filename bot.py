import telebot
import sqlite3
import uuid

API_TOKEN = '7218564504:AAGqJ8Etv4y4MkJQlonvThw3kB20uLuC5uc'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['create'])
def create_user_link(message):
    user_id = message.from_user.id

    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if the user already has a UUID
    cursor.execute("SELECT uuid FROM UserLink WHERE telegram_user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        # If the user already has a UUID, return the existing link
        user_uuid = result[0]
        bot.reply_to(message, f"You already have a link: http://127.0.0.1:5000/link/{user_uuid}")
    else:
        # If the user does not have a UUID, create a new one
        user_uuid = str(uuid.uuid4())
        cursor.execute("INSERT INTO UserLink (telegram_user_id, uuid) VALUES (?, ?)", (user_id, user_uuid))
        conn.commit()
        bot.reply_to(message, f"Your link has been created: http://127.0.0.1:5000/link/{user_uuid}")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    bot.polling()