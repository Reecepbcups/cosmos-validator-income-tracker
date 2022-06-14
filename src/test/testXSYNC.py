import asyncio

import xsync
import aiofiles

@xsync.as_hybrid()
def read_text(path):
    with open(path, 'r') as f:
        return f.read().strip()

@xsync.set_async_impl(read_text)
async def async_read_text(path):
    async with aiofiles.open(path, 'r') as f:
        return (await f.read()).strip()



import httpx
async def async_make_request(link):
    async with httpx.AsyncClient() as client:
        resp = await client.get(link)
        return resp.json()


if __name__ == '__main__':

    # print(read_text('test.txt'))

    async def main():
        v = async_make_request('https://jsonplaceholder.typicode.com/todos/1')
        print(await v)

    asyncio.run(main())