from setuptools import setup, find_packages


def read_readme() -> str:
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='file-thumbnailer',
    version='0.0.4',
    packages=find_packages(exclude=['tests', 'tests.*']),
    package_data={'file_thumbnailer': ['py.typed']},
    install_requires=[
        'python-magic',
        'Pillow'
    ],
    tests_require=[
        'tox'
    ],
    extras_require={
      'pdf': [
          'PyMuPDF'
      ]
    },
    url='https://github.com/Salamek/file-thumbnailer',
    license='LGPL-3.0 ',
    author='Adam Schubert',
    author_email='adam.schubert@sg1-game.net',
    description='File thumbnailer for images, pdfs and more',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    test_suite='tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development',
    ],
    python_requires='>=3.4',
    project_urls={
        'Release notes': 'https://github.com/Salamek/file-thumbnailer/releases',
    },
)
