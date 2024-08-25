from openai import OpenAI
client = OpenAI()

prompt_example = "In the final scene, the bird descends from the sky and lands gracefully on the dreamer's third arm. The dreamer and their friend exchange glances filled with excitement before taking off into the sky alongside the bird. The dreamer's three arms move in synchrony, emphasizing the sense of unity between the dreamer, their friend, and the bird. The sky around them is a canvas of pastel hues, creating a magical atmosphere for their flight together"

response = client.images.generate(
    model = "dall-e-3",
    prompt = prompt_example,
    size = '1024x1024',
    quality = 'standard',
    n=1,
)

image_url = response.data[0].url

print(image_url)