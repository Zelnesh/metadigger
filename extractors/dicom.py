# extractors/dicom.py

import pydicom

def extract_metadata(path):
    metadata = {}

    try:
        ds = pydicom.dcmread(path)

        for elem in ds.iterall():
            tag_name = elem.name if elem.name else str(elem.tag)
            tag_value = str(elem.value)[:200]  # Truncate long binary blobs
            metadata[tag_name] = tag_value

    except Exception as e:
        metadata['error'] = str(e)

    return metadata

