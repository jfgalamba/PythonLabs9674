#!/usr/bin/env python3
"""
Cliente síncrono (apesar do nome) da linha de comandos para descarregar
ficheiros. Utiliza requests.
"""

import requests
import httpx
# import aiohttp

DEFAULT_URLS = [
    'http://localhost:8000/4.jpg',
    'http://localhost:8000/5.jpg',
    'http://localhost:8000/6.jpg',
    'http://localhost:8000/7.jpg',
]

def get_file(url: str, file_path: str, session: requests.Session):
    print(f"[+] STARTING download of {url}")
    response = session.get(url)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(1024):
            file.write(chunk)
        # Mais simples mas lê tudo para memória
        #
        #   with open(path, 'wb') as file:
        #       file.write(response.content)
    print(f"[+] ENDING download of {url}")
#:

def get_files(urls_paths: dict[str, str]):
    """
    `url_paths` is a dictionary mapping urls to file paths. 
    Example:
        urls_paths = {
            'http://localhost:8000/4.jpg': '4.jpg',
            'http://api.cat.com/pics/xpt.gif': 'xpt.gif',
        }
    """
    with requests.Session() as session:
        for url, file_path in urls_paths.items():
            get_file(url, file_path, session)
#:

def main():
    from docopt import docopt
    doc = """
Simple GET client using the requests HTTP library.

Usage:
    getfiles [-u URLS] [-f FILE_PATHS]

Options:
    -u URLS, --urls=URLS               URLs to get. Assumes some values for
                                       testing purposes.
    -f FILE_PATHS, --files=FILE_PATHS  A file path for each URL in URLS.
"""
    args = docopt(doc)
    urls = DEFAULT_URLS
    if args['--urls']:
        urls = args['--urls'].split(',')
    file_paths = [file_path_from_url(url) for url in urls]
    if args['--files']:
        file_paths = args['--files'].split(',')

    get_files(dict(zip(urls, file_paths)))
#:

def file_path_from_url(url: str) -> str:
    """
    file_path_from_url('http://www.xpto.com/abc/imagem23.jpg') 
    => 'imagem23.jpg'
    """
    return url.rpartition('/')[-1]
#:

if __name__ == '__main__':
    main()
