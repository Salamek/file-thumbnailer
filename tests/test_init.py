import os
from pathlib import Path
from file_thumbnailer.ConverterManager import ConverterManager
from file_thumbnailer.models.Dimensions import Dimensions


def test_converter_manager_init() -> None:
    ConverterManager()


def test_get_convert_pdf() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))

    with open(os.path.join(files_path, 'sample.pdf'), 'rb') as sample_pdf:
        processor = converter_manager.from_data(sample_pdf.read())
    image_bytes = processor.to_image_bytes(Dimensions(height=500))

    assert isinstance(image_bytes, bytes)


def test_get_convert_epub() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))

    processor = converter_manager.from_file(os.path.join(files_path, 'sample.epub'))
    image_bytes = processor.to_image_bytes(Dimensions(height=500))

    assert isinstance(image_bytes, bytes)


def test_get_convert_bmp() -> None:
    converter_manager = ConverterManager()
    files_path = Path(os.path.join(os.path.dirname(__file__), 'files'))

    processor = converter_manager.from_file(os.path.join(files_path, 'sample.bmp'))
    image_bytes = processor.to_image_bytes(Dimensions(height=500))

    assert isinstance(image_bytes, bytes)
