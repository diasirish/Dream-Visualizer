import os
import openai
from openai import OpenAI


#openai.api_key = os.getenv("OPENAI_API_KEY")

#openai.api_key = ''

dream_description = "I saw the bird flying in the sky next to the sun. I look down I see I have three arms, and my friend was there. We took off flying next to the bird and it started to sit on my third arm."

prompt = f"""
I have a dream description: "{dream_description}". 
Please break this dream into four distinct scenes, providing detailed descriptions for each scene. 
Each scene should be detailed enough to serve as a prompt for an image generation model.
"""
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a creative assistant."},
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(completion.choices[0].message.content)