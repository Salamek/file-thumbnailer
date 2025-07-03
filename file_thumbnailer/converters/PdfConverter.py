import io
from typing import List, Optional, Union, BinaryIO
from file_thumbnailer.converters.Converter import Converter

is_pil = True
try:
    from PIL import Image, ImageFile
except ImportError:
    is_pil = False

is_fitz = True
try:
    import fitz
except ImportError:
    is_fitz = False


class PdfConverter(Converter):

    def __init__(self, fp: Union[io.BytesIO, BinaryIO], mime_type: str):
        super().__init__(fp, mime_type)
        if not isinstance(fp, (bytes, io.BytesIO)):
            fp = io.BytesIO(fp.read())

        self.document = fitz.Document(stream=fp, filetype=self.mime_type)

    @staticmethod
    def is_available() -> bool:
        return is_fitz and is_pil

    @staticmethod
    def get_handle_mimetypes() -> List[str]:
        return [
            'application/pdf',
            'application/vnd.ms-xpsdocument',
            'application/oxps',
            'application/epub+zip',
            'application/vnd.comicbook+zip'
        ]

    def to_pil_image(self, page: Optional[int] = None) -> ImageFile.ImageFile:
        if not page:
            page = 0

        selected_page: fitz.Page = self.document[page]

        # Compatibility with older version of fitz
        pixmap_callable = getattr(selected_page, 'get_pixmap', getattr(selected_page, 'getPixmap', None))
        if not pixmap_callable:
            raise ValueError('Failed to retrieve pixmap callable')

        selected_page_image = pixmap_callable(alpha=False, matrix=fitz.Matrix(4.0, 4.0))
        # Compatibility with older version of fitz
        to_bytes_callable = getattr(selected_page_image, 'tobytes', getattr(selected_page_image, 'getPNGData', None))
        if not to_bytes_callable:
            raise ValueError('Failed to retrieve tobytes callable')

        return Image.open(io.BytesIO(to_bytes_callable()))
