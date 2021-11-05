import io
from typing import List, Optional
from file_thumbnailer.converters.Converter import Converter

is_pil = True
try:
    from PIL import Image
except ImportError:
    is_pil = False

is_fitz = True
try:
    import fitz
except ImportError:
    is_fitz = False


class PdfConverter(Converter):

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

    def to_pil_image(self, page: Optional[int] = None) -> Image:
        if not page:
            page = 0
        source_pdf = fitz.Document(stream=self.data, filetype=self.mime_type)
        selected_page: fitz.Page = source_pdf[page]

        # Compatibility with older version of fitz
        pixmap_callable = getattr(selected_page, 'get_pixmap', getattr(selected_page, 'getPixmap'))

        selected_page_image = pixmap_callable(alpha=False, matrix=fitz.Matrix(4.0, 4.0))
        # Compatibility with older version of fitz
        tobytes_callable = getattr(selected_page_image, 'tobytes', getattr(selected_page_image, 'getPNGData'))
        return Image.open(io.BytesIO(tobytes_callable()))
