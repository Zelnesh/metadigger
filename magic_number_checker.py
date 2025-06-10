# magic_number_checker.py

from extractors import image, archive, dicom, generic

def get_file_signature(path):
    with open(path, 'rb') as f:
        return f.read(16)

def identify_file_type(signature):
    sig_hex = signature.hex()

    # JPEG
    if sig_hex.startswith('ffd8ff'):
        return 'jpeg'
    # PNG
    elif sig_hex.startswith('89504e47'):
        return 'png'
    # TIFF (little endian)
    elif sig_hex.startswith('49492a00'):
        return 'tiff'
    # TIFF (big endian)
    elif sig_hex.startswith('4d4d002a'):
        return 'tiff'
    # ZIP/Docx/XLSX
    elif sig_hex.startswith('504b0304'):
        return 'zip'
    # RAR
    elif sig_hex.startswith('52617221'):
        return 'rar'
    # 7z
    elif sig_hex.startswith('377abcaf271c'):
        return '7z'
    # DICOM
    elif len(signature) >= 132 and signature[128:132] == b'DICM':
        return 'dicom'
    else:
        return 'unknown'

def check_file_and_extract_metadata(path):
    try:
        signature = get_file_signature(path)
        file_type = identify_file_type(signature)

        if file_type in ['jpeg', 'png', 'tiff']:
            return image.extract_metadata(path)
        elif file_type in ['zip', 'rar', '7z']:
            return archive.extract_metadata(path)
        elif file_type == 'dicom':
            return dicom.extract_metadata(path)
        else:
            return generic.extract_metadata(path)

    except Exception as e:
        return {"error": str(e)}

