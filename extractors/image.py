# extractors/image.py

from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(path):
    metadata = {}

    try:
        with Image.open(path) as img:
            metadata['format'] = img.format
            metadata['mode'] = img.mode
            metadata['size'] = img.size

            if hasattr(img, '_getexif'):
                exif_data = img._getexif()
                if exif_data:
                    for tag, value in exif_data.items():
                        decoded = TAGS.get(tag, tag)
                        metadata[decoded] = value
    except Exception as e:
        metadata['error'] = str(e)

    return metadata

