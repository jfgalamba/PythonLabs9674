#!/usr/bin/env python3
"""
Cliente assíncrono da linha de comandos para descarregar ficheiros.
Utiliza aiohttp e aiofiles.
"""

import asyncio
from typing import Iterable
import aiohttp
import aiofiles


DEFAULT_URLS = [
    'http://localhost:8000/4.jpg',
    'http://localhost:8000/5.jpg',
    'http://localhost:8000/6.jpg',
    'http://localhost:8000/7.jpg',
]


async def get_file(url: str, path: str, session: aiohttp.ClientSession):
    print(f"[+] STARTING download of {url}")
    async with session.get(url) as response:
        async with aiofiles.open(path, 'wb') as file:
            async for chunk in response.content.iter_chunked(1024):
                await file.write(chunk)

        # Mais simples mas lê tudo para memória e escrita é 
        # síncrona (logo, bloqueante):
        #
        #   with open(path, 'wb') as file:
        #       file.write(await response.read())  # write é síncrono
    print(f"[+] ENDING download of {url}")
#:

async def get_files(urls_paths: Iterable[tuple[str, str]]):
    async with aiohttp.ClientSession() as session:
        # for url, file_path in urls_paths:
        #     await get_file(url, file_path, session)
        tasks = (
            asyncio.create_task(get_file(url, file_path, session)) 
            for url, file_path in urls_paths
        )
        await asyncio.wait(tasks)

        # coros = (
        #     get_file(url, file_path, client, no_timeout=True)
        #     for url, file_path in urls_paths
        # )
        # await asyncio.gather(*coros)

        # for url, file_path in urls_paths:
        #     await get_file(url, file_path, client, no_timeout=True)
#:

async def main():
    import sys
    from docopt import docopt

    doc = """
Simple GET client made with the requests HTTP library.

Usage:
    getfile [-u URL...] [-f FILE_PATHS...]

Options:
    -u URL, --urls=URL                 URLs to get. Assumes some value for testing
                                       purposes.
    -f FILE_PATHS, --files=FILE_PATHS  FILE_PATHS where to store downloaded files.
"""
    args = docopt(doc)
    urls = args['--urls'] or DEFAULT_URLS
    file_paths = args['--files'] or [file_path_from_url(url) for url in urls]
    if len(file_paths) != len(urls):
        print("Error: number of URLs not equal to the number of file paths.", file=sys.stderr)
        sys.exit(3)

    await get_files(zip(urls, file_paths))
#:

def file_path_from_url(url: str) -> str:
    return url.rpartition('/')[-1]
#:

if __name__ == '__main__':
    asyncio.run(main())
#:
