import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import requests
import re
import textwrap
from datetime import datetime
import os


quotes = []

def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)

def get_black_background():
    return np.zeros((500, 500))

def convert_time_to_string(dt):
    return f"{dt.hour}:{dt.minute:02}" if dt.hour > 9 else f"0{dt.hour}:{dt.minute:02}"

def get_quote():
    r = requests.post("http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=xml&lang=ru")
    quote = re.findall(".*<quoteText>(.*)</quoteText>", r.text)[0]
    author = re.findall(".*<quoteAuthor>(.*)</quoteAuthor>", r.text)[0]
    quotes.append(quote)
    while quote in quotes:
        r = requests.post("http://api.forismatic.com/api/1.0/?method=getQuote&key=457653&format=xml&lang=ru")
        quote = re.findall(".*<quoteText>(.*)</quoteText>", r.text)[0]
    return quote, author

def generate_image_with_text():
    image = get_black_background()
    text, author = get_quote()

    line_length = 30
    text = textwrap.wrap(text, line_length)

    fontpath = f"{os.getcwd()}/src/wqy-zenhei.ttf"
    font_size = 25
    font = ImageFont.truetype(fontpath, font_size)

    img_pil = Image.fromarray(image)
    draw = ImageDraw.Draw(img_pil)

    counter = 0
    offset = len(text)/2
    default_left_offset = 45
    for line in text:
        draw.text((default_left_offset+(((line_length-len(line))/2)*(font_size/2)), 250 + font_size * (counter - offset)), line, font=font, fill="White")
        counter += 1

    draw.text((default_left_offset+(((line_length-len(author))/2)*(font_size/2)), 500-(font_size*2)), author, font=font, fill="White")

    time = convert_time_to_string(datetime.now())

    draw.text((default_left_offset+(((line_length-len(time))/2)*(font_size/2)), (font_size*2)), time, font=font, fill="White")

    img = np.array(img_pil)
    return img

def generate_and_save_quote():
    print(f"Generate image...")
    image = generate_image_with_text()
    cv2.imwrite(f"src/quote_images/new_quote.jpg", image)
    print("Images succesfully saved.")

# quotes_count = 1000
# for i in range(quotes_count):
#     print(f"Generate {i} image...")
#     image = generate_image_with_text()
#     cv2.imwrite(f"quote_images/{i}.jpg", image)