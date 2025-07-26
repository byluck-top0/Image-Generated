from monsterapi import client
import requests
from PIL import Image
              
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImNjYTI0ZTliNTU0YjVlNTkxNmQ0OGYxZGU3NTI2ODlhIiwiY3JlYXRlZF9hdCI6IjIwMjUtMDctMjRUMDQ6MjE6MDEuNDMzNjExIn0.M5BcdHpJliiIdr9eOiYyQMao92LTVlcXRHAyLC358UA'
monster_client = client(api_key)



model = 'txt2img'  
input_data = {
'prompt': 'detailed sketch of lion by greg rutkowski, beautiful, intricate, ultra realistic, elegant, art by artgerm',
'negprompt': 'deformed, bad anatomy, disfigured, poorly drawn face',
'samples': 1,
'steps': 50,
'aspect_ratio': 'square',
'guidance_scale': 7.5,
'seed': 2414,
            }

result = monster_client.generate(model, input_data)
image_url = result['output'][0]

file_name = 'Image.png'

response = requests.get(image_url)
if response.status_code == 200:
    with open(file_name, 'wb') as file:
        file.write(response.content)
    print(f"Image saved as {file_name}")

    img = Image.open(file_name)
    img.show()
    

else:
    print(f"Failed to download the image")

