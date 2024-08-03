import openai
import requests
import os
import random
from datetime import datetime
# Set your OpenAI API keys here
openai.api_key = 'YOUR OPENAI API KEY'

class OpenAIClient:
    def __init__(self):
        self.client = openai

    def generate_prompt(self):
        """
        Generate a descriptive prompt for creating an image with random shapes and colors.
        Parameters:
            - None
        Returns:
            - str: A prompt describing the shapes and colors to be used in an image.
        Example:
            - generate_prompt() -> "Generate an image with circle, square in random colors such as red, blue. The shapes should be arranged in a pleasing manner."
        """
        shapes = ['circle', 'square', 'triangle', 'cube', 'sphere', 'pyramid']
        colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
        shape = random.choice(shapes)
        num_colors = random.randint(1, 3)
        color_list = random.sample(colors, num_colors)
        
        prompt = (
            f"Generate an image with a {shape} in random colors "
            f"such as {', '.join(color_list)}. The shape should be arranged in a pleasing manner."
        )
        return prompt

def generate_images(prompt, num_images=10):
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        n=num_images,
        size="1024x1024"
    )
    return response['data']

def download_images(image_data, output_dir='images'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, image in enumerate(image_data):
        image_url = image['url']
        response = requests.get(image_url)
        if response.status_code == 200:
            # Generate a unique filename using timestamp and index
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = os.path.join(output_dir, f'image_{timestamp}_{i + 1}.png')
            with open(unique_filename, 'wb') as f:
                f.write(response.content)
            print(f"Saved image as {unique_filename}")
        else:
            print(f"Failed to download image {i + 1}")
def main():
    client = OpenAIClient()
    
    # Generate random prompts and images
    for _ in range(10):
        prompt = client.generate_prompt()
        print(f"Generated Prompt: {prompt}")
        
        # Generate images from the prompt
        image_data = generate_images(prompt, num_images=1)
        
        # Download and save the images
        download_images(image_data)

if __name__ == "__main__":
    main()
