import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)
      
@bot.message_handler(content_types=['voice', 'audio'])
def get_audio_messages(message):
    if message.voice:
        # Handle voice messages (usually .ogg format)
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('user_voice.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Voice message received and saved as user_voice.ogg")

    elif message.audio:
        # Handle regular audio messages (could be .mp3, .m4a, etc.)
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_extension = file_info.file_path.split('.')[-1]
        with open(f'user_audio.{file_extension}', 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, f"Audio message received and saved as user_audio.{file_extension}")


bot.infinity_polling()