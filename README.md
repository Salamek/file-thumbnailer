# File thumbnailer
File thumbnailer is "saner" file thumbnailer with as little weird depedencies as possible

[![Tox tests](https://github.com/Salamek/file-thumbnailer/actions/workflows/python-test.yml/badge.svg)](https://github.com/Salamek/file-thumbnailer/actions/workflows/python-test.yml)

## Supported file formats

Supported file formats are all images supported by Pillow OOTB and all files supported by PyMuPDF (if installed)

## Installation

### PIP (pip3 on some distros)
```bash
$ pip install file-thumbnailer
$ pip install file-thumbnailer[pdf] # for PyMuPDF support
```



### Repository
You can also use these repositories maintained by me
#### Debian and derivates

Add repository by running these commands

```
$ wget -O- https://repository.salamek.cz/deb/salamek.gpg | sudo tee /usr/share/keyrings/salamek-archive-keyring.gpg
$ echo "deb     [signed-by=/usr/share/keyrings/salamek-archive-keyring.gpg] https://repository.salamek.cz/deb/pub all main" | sudo tee /etc/apt/sources.list.d/salamek.cz.list
```

And then you can install a package python3-file-thumbnailer

```
$ apt update && apt install python3-file-thumbnailer
```

## Usage

```python
from file_thumbnailer.ConverterManager import ConverterManager
from file_thumbnailer.models.Dimensions import Dimensions

converter_manager = ConverterManager()
with open('my_file.pdf', 'rb') as read_file:
    converter = converter_manager.from_data(read_file
    thumbnail = converter.to_image_bytes(Dimensions())
    with open('my_file_thumbnail.jpg', 'wb') as thumbnail_file:
        thumbnail_file.write(thumbnail)

```