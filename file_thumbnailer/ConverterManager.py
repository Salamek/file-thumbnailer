import io
import logging
from typing import Dict, Type, Optional, Union, BinaryIO
from pathlib import Path
from file_thumbnailer.converters.Converter import Converter
from file_thumbnailer.converters.PdfConverter import PdfConverter
from file_thumbnailer.converters.ImgConverter import ImgConverter
from file_thumbnailer.Tools import Tools
from file_thumbnailer.exceptions import NotSupportedException, ConflictingConverters


class ConverterManager:
    log = logging.getLogger(__name__)
    supported_mimetypes: Dict[str, Type[Converter]] = {}
    converter_classes = [
        PdfConverter,
        ImgConverter
    ]

    def __init__(self) -> None:
        # Make sure that self.supported_mimetypes is empty, things got weird when running in pytest (supported_mimetypes was already full when running bellow code)
        self.supported_mimetypes = {}
        for converter_class in self.converter_classes:
            if not converter_class.is_available():
                self.log.info('Converter %s is not available', converter_class)
                continue
            for supported_mimetype in converter_class.get_handle_mimetypes():
                mimetype_used = self.supported_mimetypes.get(supported_mimetype)
                if mimetype_used:
                    raise ConflictingConverters(f'Mimetype is already handled by {mimetype_used}')

                self.supported_mimetypes[supported_mimetype] = converter_class

        self.log.info('Supported mimetypes: %s', self.supported_mimetypes.keys())

    def from_data(self, fp: Union[bytes, io.BytesIO, BinaryIO], force_mime_type: Optional[str] = None) -> Converter:
        if isinstance(fp, bytes):
            fp = io.BytesIO(fp)

        try:
            fp.seek(0)
        except (AttributeError, io.UnsupportedOperation):
            fp = io.BytesIO(fp.read())

        mime_type = Tools.detect_mimetype(fp) if not force_mime_type else force_mime_type
        converter = self.supported_mimetypes.get(mime_type)
        if not converter:
            supported_mimetypes = ', '.join(self.supported_mimetypes.keys())
            raise NotSupportedException(f'Mimetype {mime_type} is not supported, supported mimes are: {supported_mimetypes}')
        return converter(fp, mime_type)

    def from_file(self, file_path: Union[str, Path], force_mime_type: Optional[str] = None) -> Converter:
        path_info = Path(file_path) if isinstance(file_path, str) else file_path
        with path_info.open('rb') as file_handle:
            mime_type = Tools.detect_mimetype(file_handle, path_info) if not force_mime_type else force_mime_type
            return self.from_data(file_handle, mime_type)
