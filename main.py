import tweepy
import dotenv
import os
import numpy as np
from PIL import Image
from io import BytesIO

dotenv.load_dotenv()

# Create v1.1 client for media upload
def get_client_v1():
    auth = tweepy.OAuth1UserHandler(
        os.getenv("X_API_KEY"),
        os.getenv("X_API_KEY_SECRET")
    )
    auth.set_access_token(
        os.getenv("X_ACCESS_TOKEN"),
        os.getenv("X_ACCESS_TOKEN_SECRET")
    )
    return tweepy.API(auth)

def get_client_v2():
    return tweepy.Client(
        bearer_token=os.getenv("X_BEARER_TOKEN"),
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_KEY_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET"),
    )

client_v1 = get_client_v1()
client_v2 = get_client_v2()


def generate_random_color_image():
    PHI = 1.61803398875
    height = 512
    width = int(height * PHI)
    random_rgb = np.random.randint(0, 256, size=3, dtype=np.uint8)
    print(random_rgb)
    # Fill every pixel with the same RGB triple
    image_pixels = np.ones((height, width, 3), dtype=np.uint8) * random_rgb
    image = Image.fromarray(image_pixels, mode='RGB')
    file = BytesIO()
    image.save(file, format='PNG')
    file.seek(0)
    return file


def post_tweet(message):
    response = client_v2.create_tweet(text=message)
    return response


def post_image_tweet(message):
    media = client_v1.media_upload(file=generate_random_color_image(), filename='color.png')
    media_id = media.media_id
    response = client_v2.create_tweet(text=message, media_ids=[media_id])
    return response


if __name__ == "__main__":
    tweet_message = "Today's color"
    response = post_image_tweet(tweet_message)
    print(f"Tweet posted with ID: {response.data['id']}")