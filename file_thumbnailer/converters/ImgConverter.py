import io
from typing import List, Optional, Union, BinaryIO
from file_thumbnailer.converters.Converter import Converter

is_pil = True
try:
    from PIL import Image, ImageFile
except ImportError:
    is_pil = False


class ImgConverter(Converter):

    def __init__(self, fp: Union[io.BytesIO, BinaryIO], mime_type: str):
        super().__init__(fp, mime_type)
        self.image = Image.open(fp)
        self.image.load()

    @staticmethod
    def is_available() -> bool:
        return is_pil

    @staticmethod
    def get_handle_mimetypes() -> List[str]:
        return [
            'image/bmp',
            'image/vnd-ms.dds',
            'image/dib',
            'application/eps',
            'image/gif',
            'image/jpeg',
            'image/png',
            'image/ico',
            'image/webp',
        ]

    def to_pil_image(self, page: Optional[int] = None) -> ImageFile.ImageFile:
        return self.image
