import logging
from typing import Dict, Type, Optional
from pathlib import Path
from file_thumbnailer.converters.Converter import Converter
from file_thumbnailer.converters.PdfConverter import PdfConverter
from file_thumbnailer.converters.ImgConverter import ImgConverter
from file_thumbnailer.Tools import Tools


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
                self.log.info('Converter %(converter_name)s is not available', converter_name=converter_class)
                continue
            for supported_mimetype in converter_class.get_handle_mimetypes():
                mimetype_used = self.supported_mimetypes.get(supported_mimetype)
                if mimetype_used:
                    raise Exception('Mimetype is already handled by {}'.format(mimetype_used))

                self.supported_mimetypes[supported_mimetype] = converter_class

        self.log.info('Supported mimetypes: %(mimetypes)s', mimetypes=self.supported_mimetypes.keys())

    def from_data(self, data: bytes, force_mime_type: Optional[str] = None) -> Converter:
        mime_type = Tools.detect_mimetype(data) if not force_mime_type else force_mime_type
        converter = self.supported_mimetypes.get(mime_type)
        if not converter:
            raise Exception('Mimetype {} is not supported, supported mimes are: {}'.format(mime_type, ', '.join(self.supported_mimetypes.keys())))
        return converter(data, mime_type)

    def from_file(self, file_path: str, force_mime_type: Optional[str] = None) -> Converter:
        path_info = Path(file_path)
        with path_info.open('rb') as file_handle:
            data = file_handle.read()
            mime_type = Tools.detect_mimetype(data, path_info) if not force_mime_type else force_mime_type
            return self.from_data(data, mime_type)
