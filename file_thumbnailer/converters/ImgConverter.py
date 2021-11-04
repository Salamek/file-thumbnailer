import io
from typing import List, Optional
from file_thumbnailer.converters.Converter import Converter

is_pil = True
try:
    from PIL import Image
except ImportError:
    is_pil = False


class ImgConverter(Converter):

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
            'image/gif'
        ]

    def to_pil_image(self, page: Optional[int] = None) -> Image:
        return Image.open(io.BytesIO(self.data))
