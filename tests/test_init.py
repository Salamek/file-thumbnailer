import os
from pathlib import Path
from file_thumbnailer.ConverterManager import ConverterManager
from file_thumbnailer.models.Dimensions import Dimensions


def test_converter_manager_init() -> None:
    ConverterManager()


def test_get_convert_pdf_bytes() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))

    with open(os.path.join(files_path, 'sample.pdf'), 'rb') as sample_pdf:
        converter = converter_manager.from_data(sample_pdf.read())
    image_bytes = converter.to_image_bytes(Dimensions(height=500))

    assert isinstance(image_bytes, bytes)


def test_get_convert_pdf() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))

    with open(os.path.join(files_path, 'sample.pdf'), 'rb') as sample_pdf:
        converter = converter_manager.from_data(sample_pdf)
    image_bytes = converter.to_image_bytes(Dimensions(height=500))

    assert isinstance(image_bytes, bytes)


def test_get_convert_epub() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))

    converter = converter_manager.from_file(os.path.join(files_path, 'sample.epub'))
    image_bytes = converter.to_image_bytes(Dimensions(height=500))

    assert isinstance(image_bytes, bytes)


def test_get_convert_bmp() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))

    converter = converter_manager.from_file(os.path.join(files_path, 'sample.bmp'))
    image_bytes = converter.to_image_bytes(Dimensions(height=500))

    assert isinstance(image_bytes, bytes)


def test_get_convert_bmp_large_file() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))
    source_file = os.path.join(files_path, 'sample.bmp')
    big_file = os.path.join(files_path, 'sample_big.bmp')
    # Prepare "huge" file
    with open(source_file, 'rb') as s:
        with open(big_file, 'ab') as b:
            b.write(s.read())
            for i in range(30):
                b.write(bytearray(10485760))

    try:
        converter = converter_manager.from_file(big_file)
        image_bytes = converter.to_image_bytes(Dimensions(height=500))
    except Exception:
        raise
    finally:
        os.remove(big_file)
    assert isinstance(image_bytes, bytes)
