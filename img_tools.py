# 0-255 format for internal training
# rgba png export with r=g=b=255 and alpha for opacity
# input with 000 -> 255 255 255 255, x x x 0 -> 255... x

from PIL import Image, ImageDraw, ImageFont
import numpy as np

from pathlib import Path


def text_on_img(filename='test.png', out_folder='', text="8", font_file=None, auto_adjast=True):
    # path preparation
    out_path = out_folder / filename

    # create image, transparent
    pic_dim = 256
    pic_size = (pic_dim, pic_dim)
    image = Image.new(mode="RGBA", size=pic_size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # font set up
    if font_file is None:
        font_file = "arial.ttf"
    else:
        font_file = str(font_file)

    size = 256
    font = ImageFont.truetype(font_file, size)
    max_area = 0.90
    if auto_adjast:
        while True:
            bbox = draw.textbbox((0, 0), text, font=font)
            width_box = bbox[2] - bbox[0]
            height_box = bbox[3] - bbox[1]
            if (width_box / pic_dim >= max_area) or (height_box / pic_dim >= max_area):
                break
            else:
                size += 1
                font = ImageFont.truetype(font_file, size)
        print(size, ";", end=" ")

    bbox = draw.textbbox((0, 0), text, font=font)
    width_box = bbox[2] - bbox[0]
    height_box = bbox[3] - bbox[1]
    x_pos = (pic_dim - width_box) / 2
    y_pos = (pic_dim - height_box) / 2
    x_offset = -bbox[0] + x_pos
    y_offset = -bbox[1] + y_pos

    pos = (x_offset, y_offset)

    test_mode = False
    if test_mode:
        # this is testing of box for text
        bbox_testing = draw.textbbox(pos, "2", font=font)
        draw.rectangle(bbox_testing, outline="red")

    draw.text(pos, text=text, font=font, fill=(0, 0, 0))

    # save file
    image.save(out_path)

    # show file
    # os.system(str(out_path))


def augmentation(img_arr, scale_arr=None, translation_arr=None, rotate_arr=None):
    if scale_arr is None:
        scale_arr = [0.85, 0.9, 0.95, 1]
    if translation_arr is None:
        translation_arr = list(range(-9, 10, 3))
    if rotate_arr is None:
        rotate_arr = list(range(-6, 7))
    # full augmentation size
    total_samples = len(img_arr) * len(scale_arr) * len(translation_arr) * len(translation_arr) * len(rotate_arr)
    size_input = img_arr[0].size
    ans_shape = (total_samples, size_input[0], size_input[1])
    ans = np.zeros(ans_shape, dtype=np.single)

    for img in img_arr:
        for angle in rotate_arr:
            tmp_pic = img.rotate(angle, resample=Image.BILINEAR)
    return ans


if __name__ == "__main__":

    # this generates 0-9 for each font
    fonts_path = Path("fonts")
    data_path = Path("dataset")
    for font_file in fonts_path.glob("*.ttf"):
        (data_path / font_file.stem).mkdir(parents=True, exist_ok=True)
        for num in range(10):
            text_on_img(auto_adjast=True, text=str(num), filename=str(num) + ".png", font_file=font_file,
                        out_folder=data_path / font_file.stem)
