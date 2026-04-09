from PIL import Image
import imagehash

def generate_hash(image_path):
    image = Image.open(image_path)

    # perceptual hash (best for duplicate detection)
    hash_value = imagehash.phash(image)

    return str(hash_value)