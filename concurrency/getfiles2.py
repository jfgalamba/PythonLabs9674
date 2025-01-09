#!/usr/bin/env python3
"""
Cliente síncrono (apesar do nome) da linha de comandos para descarregar
ficheiros. Utiliza requests.
"""

import asyncio
import httpx
import aiofiles


DEFAULT_URLS = [
    'http://localhost:8000/4.jpg',
    'http://localhost:8000/5.jpg',
    'http://localhost:8000/6.jpg',
    'http://localhost:8000/7.jpg',
]


async def get_file(url: str, file_path: str, client: httpx.AsyncClient):
    print(f"[+] STARTING download of {url}")
    response = await client.get(url, timeout=None)
    async with aiofiles.open(file_path, 'wb') as file:
        async for chunk in response.aiter_bytes(1024):
            await file.write(chunk)

        # Mais simples mas lê tudo para memória
        #
        #   async with aiofiles.open(path, 'wb') as file:
        #       await file.write(await response.aread())
    print(f"[+] ENDING download of {url}")
#:

async def get_files(urls_paths: dict[str, str]):
    """
    `url_paths` is a dictionary mapping urls to file paths. 
    Example:
        urls_paths = {
            'http://localhost:8000/4.jpg': '4.jpg',
            'http://api.cat.com/pics/xpt.gif': 'xpt.gif',
        }
    """
    async with httpx.AsyncClient() as client:
        # juntar todas as co-rotinas (ie, todas funções assíncronas),
        # lançá-las em simultâneo e aguardar (await gather) por todas
        coros = (
            get_file(url, file_path, client) for url, file_path in urls_paths.items()
        )
        await asyncio.gather(*coros)

        # Semelhante ao bloco anterior, mas criando uma tarefa por 
        # cada co-rotina. O método anterior (gather) acaba por fazer 
        # algo semelhante:
        # 
        # tasks = (
        #     asyncio.create_task(get_file(url, file_path, client)) 
        #     for url, file_path in urls_paths.items()
        # )
        # await asyncio.wait(tasks)

        # for url, file_path in urls_paths.items():
        #     await get_file(url, file_path, client)
#:

async def main():
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

    await get_files(dict(zip(urls, file_paths)))
#:

def file_path_from_url(url: str) -> str:
    """
    file_path_from_url('http://www.xpto.com/abc/imagem23.jpg') 
    => 'imagem23.jpg'
    """
    return url.rpartition('/')[-1]
#:

if __name__ == '__main__':
    asyncio.run(main())
