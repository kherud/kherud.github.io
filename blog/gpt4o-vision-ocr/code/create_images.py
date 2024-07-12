import os
import random

import nltk
from PIL import Image, ImageDraw, ImageFont
from nltk.corpus import words

nltk.data.path.append('.')


def generate_random_words(num_words):
    word_list = words.words()
    random_words = random.sample(word_list, num_words)
    return ' '.join(random_words)


def create_image_with_text(width, height, text, font_size):
    # Create a blank white image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Draw the vertical lines
    for x in range(0, width + 1, 64):
        draw.line((x, 0, x, width), fill=(211, 211, 211))

    # Draw the horizontal lines
    for y in range(0, height + 1, 64):
        draw.line((0, y, height, y), fill=(211, 211, 211))

    # Load a font
    try:
        font = ImageFont.truetype("./Arial.ttf", font_size)
    except IOError:
        print("could not load font")
        font = ImageFont.load_default()

    # Split the text into lines that fit the image width
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_width <= max_width:
                line = test_line
            else:
                if line:  # Add the previous line to the list
                    lines.append(line)
                line = word  # Start a new line with the current word
        if line:  # Add the last line to the list
            lines.append(line)
        return lines

    lines = wrap_text(text, font, width)

    # Calculate the height required for the text
    total_text_height = len(lines) * (font_size)  # Adding a small padding between lines

    # Check if the total text height fits within the image height
    if total_text_height > height:
        raise ValueError("The text is too large to fit in the image with the given dimensions and font size")

    # Draw the text
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill='black')
        y += font_size  # Move to the next line

    # Save or show the image
    return img


# Parameters
steps = range(0, 1100, 100)
samples_per_step = 10
width = 1024
height = 1024
text = generate_random_words(1000)
font_size = 14

for n in steps:
    img_dir = os.path.join("data", "img", str(n))
    txt_dir = os.path.join("data", "txt", str(n))
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)
    for i in range(samples_per_step):
        img_file = os.path.join(img_dir, str(i) + ".png")
        txt_file = os.path.join(txt_dir, str(i) + ".txt")
        while True:
            try:
                text = generate_random_words(n)
                img = create_image_with_text(width, height, text, font_size)
                img.save(img_file)
                with open(txt_file, "w") as file:
                    file.write(text)
                break
            except Exception as e:
                print(e)
