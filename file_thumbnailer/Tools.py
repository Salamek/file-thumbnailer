import io
from typing import Optional, Union, BinaryIO
import mimetypes
import pathlib
import magic
from file_thumbnailer.models.Dimensions import Dimensions


class Tools:

    @staticmethod
    def calculate_dimensions(from_dimensions: Dimensions, to_dimensions: Dimensions) -> Dimensions:
        ratio_from = from_dimensions.width / from_dimensions.height

        if not to_dimensions.width and to_dimensions.height:
            to_dimensions.width = int(to_dimensions.height * ratio_from)

        if not to_dimensions.height and to_dimensions.width:
            to_dimensions.height = int(to_dimensions.width / ratio_from)

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
    def detect_mimetype(fp: Union[io.BytesIO, BinaryIO], file_path: Optional[pathlib.Path] = None) -> str:
        extension_detection_mimetypes = [
            'application/zip',
            'text/xml'
        ]
        mime_type = magic.from_buffer(fp.read(4096), mime=True)  # type: ignore
        fp.seek(0)
        if file_path and mime_type in extension_detection_mimetypes:
            mime_type, _ = mimetypes.guess_type(str(file_path.absolute()))

        return mime_type
