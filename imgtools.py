# 0-255 format for internal training
# rgba png export with r=g=b=255 and alpha for opacity
# input with 000 -> 255 255 255 255, x x x 0 -> 255... x

from PIL import Image, ImageDraw, ImageFont

from pathlib import Path


def text_on_img(filename='test.png', out_folder='', text="8", font_file=None):

    # path preparation
    out_path = out_folder / filename

    # create image, transparent
    size = (256, 256)
    image = Image.new(mode="RGBA", size=size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # font set up
    if font_file is None:
        font_file = "arial.ttf"
    else:
        font_file = str(font_file)

    font = ImageFont.truetype(font_file, 280)

    bbox = draw.textbbox((0, 0), "2", font=font)
    width_box = bbox[0] + bbox[2]
    height_box = bbox[1] + bbox[3]

    pos = (size[0] / 2 - width_box / 2, size[1] / 2 - height_box / 2)

    '''
    # this is testing of box for text
    bbox_testing = draw.textbbox(pos, "2", font=font)
    draw.rectangle(bbox_testing, outline="red")
    '''

    draw.text(pos, text=text, font=font, fill=(0, 0, 0))

    # save file
    image.save(out_path)

    # show file
    # os.system(str(out_path))



if __name__ == "__main__":

    # this generates 0-9 for each font
    fonts_path = Path("fonts")
    data_path = Path("dataset")
    for font_file in fonts_path.glob("*.ttf"):
        (data_path / font_file.stem).mkdir(parents=True, exist_ok=True)
        for num in range(10):
            text_on_img(text=str(num), filename=str(num) + ".png", font_file=font_file,
                        out_folder=data_path / font_file.stem)
