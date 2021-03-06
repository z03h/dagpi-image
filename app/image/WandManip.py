import functools
from io import BytesIO

from wand.exceptions import TypeError
from wand.image import Image

from app.exceptions.errors import BadImage, FileLarge


class WandManip:
    @staticmethod
    def wand_open(byt: bytes) -> Image:
        if byt.__sizeof__() > 10 * (2 ** 20):
            raise FileLarge("Large file")
        try:
            return Image(blob=byt)
        except TypeError:
            raise BadImage("Invalid Format")

    @staticmethod
    def wand_save(byt: bytes) -> BytesIO:
        io = BytesIO(byt)
        io.seek(0)
        return io


def wand_static(function):
    @functools.wraps(function)
    def wrapper(image, *args, **kwargs):
        img = WandManip.wand_open(image)
        if img.format in ["PNG", "JPEG"]:
            dst_image = function(img, *args, **kwargs)
            byt = dst_image.make_blob()
        else:
            raise BadImage("Inavlid Format")
        return WandManip.wand_save(byt), img.format

    return wrapper


def wand(function):
    @functools.wraps(function)
    def wrapper(image, *args, **kwargs):
        img = WandManip.wand_open(image)
        if img.format == "GIF":
            with Image() as dst_image:
                for frame in img.sequence:
                    frame = function(frame, *args, **kwargs)
                    dst_image.sequence.append(frame)
                byt = dst_image.make_blob()
        elif img.format in ["PNG", "JPEG"]:
            dst_image = function(img, *args, **kwargs)
            byt = dst_image.make_blob()
        else:
            raise BadImage("Inavlid Format")
        return WandManip.wand_save(byt), img.format

    return wrapper
