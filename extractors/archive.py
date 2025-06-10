# extractors/archive.py
import zipfile
import tarfile
import os

def extract_metadata(file_path: str) -> dict:
    metadata = {}
    try:
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zipf:
                metadata['type'] = 'zip'
                metadata['file_count'] = len(zipf.namelist())
                metadata['files'] = zipf.namelist()
                metadata['uncompressed_size'] = sum(
                    z.file_size for z in zipf.infolist()
                )
        elif tarfile.is_tarfile(file_path):
            with tarfile.open(file_path, 'r') as tarf:
                metadata['type'] = 'tar'
                metadata['file_count'] = len(tarf.getmembers())
                metadata['files'] = [m.name for m in tarf.getmembers()]
                metadata['uncompressed_size'] = sum(
                    m.size for m in tarf.getmembers()
                )
        else:
            metadata['error'] = 'Unsupported archive format'
    except Exception as e:
        metadata['error'] = str(e)
    return metadata

