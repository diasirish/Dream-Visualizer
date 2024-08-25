import os

import openai
from openai import OpenAI
import whisper

from utils import extract_scenes


def audio_to_text(model_name='whisper', audio_file_path='audio_files/test_3.m4a'):
    """Transcribes audio into a text.
    Inputs
        model_name (str) : defines the model we would like to use
        audio_file_path (str) : path to the audio file we would liket o transcribe
    Outputs
        text (str) : transcribed text from the audio
    """

    if model_name == 'whisper':
        model = whisper.load_model("medium")
        results = model.transcribe(audio_file_path, task='translate')
        return results["text"]
    else:
        print("No other modules are yet implemented. Use OpenAI's Whisper 2 by settin model_name='whisper'")
        return None


def text_to_frames(full_dream, LLM_model, LLM_type="API"):
    """Divides the whole dream into specific frames and fine-tunes these to be used as a good prompt for the image generation step.
    Inputs
        full_dream (str) : a full dream description
        type (str) : 'API' or 'local'. If API is chosen, then OpenAI's API will be used. Otherwise some local LLM will be used.
        model (str) : a type of model 
        model_size (str) : a size of a model
    """
    if LLM_type == "API":
        openai.api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI()

        # TODO: Figure out a way to pass the prompt with a link to full_dream from the main function
        prompt = f"""
        I have a dream description: "{full_dream}". 
        Please break this dream into four distinct scenes, providing detailed descriptions for each scene. 
        Each sequence should begin with a Scene int. Name of the scene.
        And scene description should follow right after with Desctiption: Detailed propmt of the scene.
        Each scene should be detailed enough to serve as a prompt for an image generation model. Stylistically make it as realistic and as HD as possible to create vivid and realistic images.
        """

        completion = client.chat.completions.create(
            model=LLM_model,
            messages=[
                {"role": "system", "content": "You are a creative assistant that helps to create detailed image descriptions to be used as prompts."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        print(f"OpenAI {LLM_model} returned: {completion.choices[0].message}")
        dream_sequences_dict = extract_scenes(completion.choices[0].message.content)
    else:
        # TODO: create a local implementation of the LLM image prompts generator
        ...
    
    return dream_sequences_dict


def main():
    """Main function that runs the whole dream generation sequence"""
   
    FORMAT = 'pre_recorded' # or "live_recording"    
    MODEL_AUTOMATIC_SPEECH_RECOGNITION = 'whisper'
    LLM_MODEL = "gpt-3.5-turbo"

    if FORMAT == 'live_recording':
        # TODO: add option to capture live recording and store it into a file
        # or should I pass it directly into the whisper model???
        ...
    else:
        AUDIO_FILE_PATH = 'audio_files/test_3.m4a'

    dream_description_text = audio_to_text(model_name=MODEL_AUTOMATIC_SPEECH_RECOGNITION,
                                           audio_file_path=AUDIO_FILE_PATH)
    
    if dream_description_text == None:
        print("No dream was captured, try again...")
        exit()


    dream_sequences_dict = text_to_frames(full_dream=dream_description_text, LLM_model=LLM_MODEL)
    print(dream_sequences_dict)


if __name__ == "__main__":
    main()