from PIL import Image, ImageDraw, ImageFont
import time
import io

from memelist import meme_images

class OutputFile:
    def __init__(self, image, filetype):
        self.file = image
        self.filetype = filetype

def add_text(image_name, text):
    try:
        chosen_image = meme_images[image_name.lower()]
    except KeyError:
        return None

    font = ImageFont.truetype(chosen_image.font, 60)

    # calculate size of text using 10x10 test image canvas so actual text image
    # can be sized dynamically
    draw_example = ImageDraw.Draw(Image.new('RGBA', (10, 10), (255, 255, 255, 0)))
    text_width, text_height = draw_example.textsize(text, font)
    if text_width > 2000: text_width = 2000
    if text_height > 2000: text_height = 2000

    max_text_image_dimension = text_width + text_height
    text_image_size = (max_text_image_dimension, max_text_image_dimension)
    text_image_offset = (
        (max_text_image_dimension - text_width) / 2,
        (max_text_image_dimension - text_height) / 2
    )

    text_image = Image.new('RGBA', text_image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text(text_image_offset, text, chosen_image.color, font=font)

    resize_ratio = min(
        chosen_image.size[0] / text_width,
        chosen_image.size[1] / text_height
    )
    new_text_image_size = (
        int(text_image_size[0] * resize_ratio),
        int(text_image_size[1] * resize_ratio)
    )
    transformed_text_image = text_image.resize(new_text_image_size, Image.ANTIALIAS).rotate(chosen_image.rotation)

    text_location = (chosen_image.location[0] - int(text_image_offset[0]*resize_ratio),
                     chosen_image.location[1] - int(text_image_offset[1]*resize_ratio))

    background_image = Image.open(chosen_image.path)
    output = io.BytesIO()
    if not chosen_image.is_gif:
        background_image.paste(transformed_text_image, text_location, transformed_text_image)
        background_image.save(output, format='jpeg')
        return OutputFile(output, 'jpg')
    else:
        frames = []
        frame_no = 0
        while True:
            try:
                background_image.seek(frame_no)
            except EOFError:
                break
            frame = background_image.copy().convert('RGBA')
            frame.paste(transformed_text_image, text_location, transformed_text_image)
            frames += [frame]
            frame_no += 1
        frames[0].save(output, format='gif', save_all=True, append_images=frames[1:])
        return OutputFile(output, 'gif')

if __name__ == '__main__':
    import sys
    Image.open(add_text(sys.argv[1], sys.argv[2]).file).show()
