from typing import Optional
import mimetypes
import pathlib
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
    def detect_mimetype(data: bytes, file_path: Optional[pathlib.Path] = None) -> str:
        extension_detection_mimetypes = [
            'application/zip',
            'text/xml'
        ]

        mime_type = magic.from_buffer(data, mime=True)  # type: ignore
        if file_path and mime_type in extension_detection_mimetypes:
            mime_type, _ = mimetypes.guess_type(str(file_path.absolute()))

        return mime_type
