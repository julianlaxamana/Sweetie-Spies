
# TODO: Import your libaries
from secrets import API_KEY
from openai import OpenAI
from gtts import gTTS
import base64

client = OpenAI(api_key=API_KEY)

# Image encoding, code provided
def encode_image(image_path):
    with open(image_path, "rb") as image_F:
        return base64.b64encode(image_F.read()).decode('utf-8')


# TODO: Sending a request and getting a response

def describe(image_path, audiopath):
    image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
         messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please describe this image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    answer = response.choices[0].message.content

    tts = gTTS(answer)
    tts.save(audiopath)
    return answer




# TODO: How do we make things audible?
    


# TODO: Can we put everything together?

