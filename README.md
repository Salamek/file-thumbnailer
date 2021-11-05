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
