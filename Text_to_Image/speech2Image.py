import speech_recognition as sr
from translate import Translator
from monsterapi import client
import requests
from PIL import Image
import os
import time


IMAGES_DIR = "generated_images"
os.makedirs(IMAGES_DIR, exist_ok=True)

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImNjYTI0ZTliNTU0YjVlNTkxNmQ0OGYxZGU3NTI2ODlhIiwiY3JlYXRlZF9hdCI6IjIwMjUtMDctMjRUMDQ6MjE6MDEuNDMzNjExIn0.M5BcdHpJliiIdr9eOiYyQMao92LTVlcXRHAyLC358UA'
monster_client = client(api_key)

def generate_and_save_image(translated_text):
    model = 'txt2img'
    input_data = {
        'prompt': f'{translated_text}',
        'negprompt': 'deformed, bad anatomy, disfigured, poorly drawn face',
        'samples': 1,
        'steps': 50,
        'aspect_ratio': 'square',
        'guidance_scale': 7.5,
        'seed': 2414,
    }

    print("Generating image... Please wait.")

    try:
        # Generate image
        result = monster_client.generate(model, input_data)
        image_url = result['output'][0]

        # Create unique filename using timestamp
        timestamp = int(time.time())
        file_name = os.path.join(IMAGES_DIR, f'image_{timestamp}.png')

        # Download and save image
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Image saved as {file_name}")

            # Show the image
            img = Image.open(file_name)
            img.show()
            return True
        else:
            print(f"Failed to download the image")
            return False

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return False

def main():
    recognizer = sr.Recognizer()
    translator = Translator(from_lang="hi", to_lang="en")

    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio, language="hi-IN")
            translated_text = translator.translate(text)
            print(f"Translated text: {translated_text}")
            
            # Generate and save image
            generate_and_save_image(translated_text)
            
        except sr.UnknownValueError:
            print("Can't Understand")
        except sr.RequestError as e:
            print("Google API Error")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()