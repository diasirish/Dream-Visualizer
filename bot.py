import os
import telebot
import whisper
import openai
from openai import OpenAI

from utils import extract_scenes, download_image_from_URL

# Load the necessary environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize Whisper model (loading this globally for efficiency)
whisper_model = whisper.load_model("medium")

openai.api_key = os.getenv("OPENAI_API_KEY")
client_OpenAI = OpenAI()

# Command handler for /start and /hello
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Greetings. Tell me what you saw in your dreams??")

# Message handler for voice and audio messages
@bot.message_handler(content_types=['voice', 'audio'])
def get_audio_messages(message):
    if message.voice:
        # Handle voice messages (usually .ogg format)
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        audio_file_path = 'user_voice.ogg'
        with open(audio_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Your dream was received and saved. Now let me imagine it...")

    elif message.audio:
        # Handle regular audio messages (could be .mp3, .m4a, etc.)
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_extension = file_info.file_path.split('.')[-1]
        audio_file_path = f'user_audio.{file_extension}'
        with open(audio_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, f"Audio message received and saved as {audio_file_path}. Now processing...")

    # Transcribe audio to text using Whisper
    dream_description_text = audio_to_text(whisper_model, audio_file_path)

    if dream_description_text is None:
        bot.reply_to(message, "No dream was captured, try again...")
    else:
        bot.reply_to(message, "Dream is vivid. Generating scenes...")

        # Generate dream sequences using LLM
        dream_sequences_dict = text_to_frames(dream_description_text, LLM_model="gpt-3.5-turbo", LLM_type="OpenAI_API")

        # Generate images for each scene
        for key in dream_sequences_dict:
            prompt = dream_sequences_dict[key]
            image_url = frame_to_image(img_gen_type="OpenAI_API", model="dall-e-3", prompt=prompt, frame_num=key)
            bot.send_photo(message.chat.id, image_url, caption=f"Scene {key}: {prompt}")

def audio_to_text(whisper_model, audio_file_path):
    """Transcribes audio into text using Whisper."""
    results = whisper_model.transcribe(audio_file_path)
    return results["text"]

def text_to_frames(full_dream, LLM_model, LLM_type="OpenAI_API"):
    """Divides the dream into specific frames and fine-tunes them for image generation."""
    if LLM_type == "OpenAI_API":

        prompt = f"""
        I have a dream description: "{full_dream}". 
        Please break this dream into four distinct scenes, providing detailed descriptions for each scene. 
        Each sequence should begin with a Scene int. Name of the scene.
        And scene description should follow right after with Description: Detailed prompt of the scene.
        Each scene should be detailed enough to serve as a prompt for an image generation model. Stylistically make it as realistic and as HD as possible to create vivid and realistic images.
        """

        completion = client_OpenAI.chat.completions.create(
            model=LLM_model,
            messages=[
                {"role": "system", "content": "You are a creative assistant that helps to create detailed image descriptions to be used as prompts."},
                {"role": "user", "content": prompt}
            ]
        )
        dream_sequences_dict = extract_scenes(completion.choices[0].message.content)
        return dream_sequences_dict
    else:
        print("No other modules are yet implemented. Use OpenAI's GPT-3.5 by setting LLM_model='gpt-3.5-turbo'")
        return {}

def frame_to_image(img_gen_type='OpenAI_API', model='dall-e-3', prompt='test', frame_num=0):
    """Creates image from the prompt provided using OpenAI's DALL-E model."""
    if img_gen_type == 'OpenAI_API':
        openai.api_key = OPENAI_API_KEY
        
        response = client_OpenAI.images.generate(
            model=model,
            prompt=prompt,
            size='1024x1024',
            quality = 'standard',
            n=1
        )

        image_url = response.data[0].url
        download_image_from_URL(image_url, img_num=frame_num)
        return image_url
    else:
        print("No other modules are yet implemented. Use OpenAI's Dall-E 3 by setting model='dall-e-3' & img_gen_type='OpenAI_API'")
        return ""

# Start polling
bot.infinity_polling()