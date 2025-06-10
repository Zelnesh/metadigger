# extractors/generic.py
import os

def extract_metadata(file_path: str) -> dict:
    metadata = {}
    try:
        stat = os.stat(file_path)
        metadata['size_bytes'] = stat.st_size
        metadata['last_modified'] = stat.st_mtime
        metadata['last_accessed'] = stat.st_atime
        metadata['created'] = stat.st_ctime
    except Exception as e:
        metadata['error'] = str(e)
    return metadata

