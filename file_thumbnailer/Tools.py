from typing import Optional
import magic
from file_thumbnailer.models.Dimensions import Dimensions


class Tools:

    @staticmethod
    def calculate_dimensions(from_dimensions: Dimensions, to_dimensions: Dimensions) -> Dimensions:

        ratio_from = from_dimensions.width / from_dimensions.height
        ratio_to = to_dimensions.width / to_dimensions.height

        if ratio_from > ratio_to:
            ratio = to_dimensions.width / from_dimensions.width
        else:
            ratio = to_dimensions.height / from_dimensions.height

        return Dimensions(
            round(from_dimensions.width * ratio),
            round(from_dimensions.height * ratio)
        )

    @staticmethod
    def detect_mimetype(data: bytes, extension: Optional[str] = None) -> str:
        mime_type = magic.from_buffer(data, mime=True)  # type: ignore
        if extension:
            # Try to narrow down mimetype by extension in some shitty situation like zip archive packed XMLs and shit
            mime_type_override = {
                'application/zip': {
                    'xps': 'application/vnd.ms-xpsdocument',
                    'cbz': 'application/vnd.comicbook+zip'
                },
                'text/xml': {
                    'fb2': 'application/x-fictionbook+xml'
                }
            }.get(mime_type, {}).get(extension)

            if mime_type_override:
                return mime_type_override

        return mime_type
