import io
from typing import Optional, Union, BinaryIO
import mimetypes
import pathlib
import magic
from file_thumbnailer.models.Dimensions import Dimensions


class Tools:

    @staticmethod
    def calculate_dimensions(from_dimensions: Dimensions, to_dimensions: Dimensions) -> Dimensions:
        if not from_dimensions.width or not from_dimensions.height:
            raise ValueError('from_dimensions width/height has to be set!')

        ratio_from = from_dimensions.width / from_dimensions.height

        if not to_dimensions.width and to_dimensions.height:
            to_dimensions.width = int(to_dimensions.height * ratio_from)

        if not to_dimensions.height and to_dimensions.width:
            to_dimensions.height = int(to_dimensions.width / ratio_from)

        if not to_dimensions.width or not to_dimensions.height:
            raise ValueError('Failed to resolve to_dimensions')

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
        # These mimetypes are sometimes not what they seems, lot of file formats are just renamed zips or xml
        # We need to attempt file extension detection
        extension_detection_mimetypes = [
            'application/zip',
            'text/xml'
        ]

        # These mimetypes are broken in python-magic on debian and alike when using small buffer for detection for some reason?
        # It works ok on Archlinux with file 5.41-1
        bricked_mime_detection = [
            ([0x42, 0x4d], 'image/bmp')
        ]

        buffer = fp.read(4096)
        for magic_number, override_mime_type in bricked_mime_detection:
            if buffer.startswith(bytearray(magic_number)):
                return override_mime_type

        mime_type = magic.from_buffer(buffer, mime=True)
        fp.seek(0)
        if file_path and mime_type in extension_detection_mimetypes:
            mime_type_guessed, _ = mimetypes.guess_type(str(file_path.absolute()))
            if mime_type_guessed:
                mime_type = mime_type_guessed

        return mime_type
