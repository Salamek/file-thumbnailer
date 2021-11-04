import io
from typing import List, Optional
from PIL import Image
from file_thumbnailer.models.Dimensions import Dimensions
from file_thumbnailer.Tools import Tools


class Converter:

    def __init__(self, data: bytes, mime_type: str):
        self.data = data
        self.mime_type = mime_type

    @staticmethod
    def is_available() -> bool:
        raise NotImplementedError

    @staticmethod
    def get_handle_mimetypes() -> List[str]:
        raise NotImplementedError

    def to_pil_image(self, page: Optional[int] = None) -> Image:
        raise NotImplementedError

    def to_image_bytes(self, dimensions: Dimensions, image_format: str = 'PNG') -> bytes:
        pil_image = self.to_pil_image()
        buffer = io.BytesIO()
        calculated_dimensions = Tools.calculate_dimensions(Dimensions(pil_image.width, pil_image.height), dimensions)
        resized = pil_image.resize((calculated_dimensions.width, calculated_dimensions.height), resample=True)
        resized.save(buffer, format=image_format)
        return buffer.getvalue()
