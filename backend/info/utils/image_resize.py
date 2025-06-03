from PIL import Image
import os

def resize_avatar(image_path, size=(500, 500)):
    img = Image.open(image_path)
    
    # First convert to RGB (in case it's RGBA or P mode)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    # Make it square (center crop)
    width, height = img.size
    min_size = min(width, height)
    left = (width - min_size) / 2
    top = (height - min_size) / 2
    right = (width + min_size) / 2
    bottom = (height + min_size) / 2

    img = img.crop((left, top, right, bottom))
    img = img.resize(size, Image.ANTIALIAS)
    img.save(image_path)
