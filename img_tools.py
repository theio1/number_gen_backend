# 0-255 format for internal training
# rgba png export with r=g=b=255 and alpha for opacity
# input with 000 -> 255 255 255 255, x x x 0 -> 255... x

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops

import numpy as np

from pathlib import Path


def text_on_img(filename='test.png', out_folder='', text="8", font_file=None, auto_adjast=True, pic_dim=128):
    # path preparation
    out_path = out_folder / filename

    # create image, transparent
    pic_size = (pic_dim, pic_dim)
    image = Image.new(mode="RGBA", size=pic_size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    # font set up
    if font_file is None:
        font_file = "arial.ttf"
    else:
        font_file = str(font_file)

    size = pic_dim
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


def img_to_nparr(img, ):
    # not needed for now
    pass

def augmentation(img_arr, scale_arr=None, translation_arr=None, rotate_arr=None, mode="np"):
    img_size = img_arr[0].size[0]

    if scale_arr is None:
        scale_arr = [0.87, 0.9, 0.93, 0.96, 0.97, 1]
    if translation_arr is None:
        # percentages!
        translation_arr = list(range(-4, 5, 2))
        translation_arr = [round(img_size*i/100) for i in translation_arr]
    if rotate_arr is None:
        rotate_arr = list(range(-6, 7))

    # full augmentation size
    total_samples = len(img_arr) * len(scale_arr) * len(translation_arr) * len(translation_arr) * len(rotate_arr)
    size_input = img_arr[0].size

    if mode == "np":
        ans_shape = (total_samples, size_input[0], size_input[1])
        ans = np.zeros(ans_shape, dtype=np.single)
    elif mode == "img":
        ans = [None] * total_samples


    iter_pic = 0
    for img in img_arr:
        for angle in rotate_arr:
            img_rotated = img.rotate(angle, resample=Image.BILINEAR)
            for scale in scale_arr:
                new_size = int(img_size * scale) // 2 * 2
                img_scaled_small = ImageOps.pad(img_rotated, size=(new_size, new_size))
                border = (img_size - img_scaled_small.size[0]) // 2
                img_scaled = ImageOps.expand(img_scaled_small, border=border)
                for offset_x in translation_arr:
                    for offset_y in translation_arr:
                        img_translated = ImageChops.offset(img_scaled, xoffset=offset_x, yoffset=offset_y)

                        # this is final picture, not turn in into numpy arr and write to ans


                        # flip to fix y-inversion
                        # [:, :, 3] picks only alpha channel
                        # we only need black and its opacity
                        if mode == "np":
                            img_np = np.asarray(img_translated)
                            img_np_float = np.array((np.flip(img_np[:, :, 3], axis=0)) / 255)
                            ans[iter_pic] = img_np_float

                        elif mode == "img":
                            r, g, b, a = img_translated.split()
                            ans[iter_pic] = a
                        iter_pic += 1

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
