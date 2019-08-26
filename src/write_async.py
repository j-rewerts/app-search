from async_client import AsyncClient
import csv
import asyncio
import aiofiles
import time
from aiohttp import ClientSession

ENGINE = 'council-reports-csv'
FILE_NAME = 'council_meta_sample.csv'
QUEUE_PULL_SIZE = 1000

async def main():
    print('Setting up connection')
    async with ClientSession() as session:
        client = AsyncClient(
            client=session,
            api_key='',
            base_endpoint='192.168.1.1:3002/api/as/v1',
            use_https=False,
        )
        print('connection established')

        q = asyncio.Queue()
        producer = [asyncio.create_task(read_csv_file(FILE_NAME, q))]
        consumers = [asyncio.create_task(send_data(client, q)) for n in range(10)]
        await asyncio.gather(*producer)
        await q.join()
        for c in consumers:
            c.cancel()



async def read_csv_file(file: str, q: asyncio.Queue, delim: str =','):
    """
    Asyncronously reads a file into a work queue. 
    We use the CSV library to parse lines, as splitting on commas naively
    can cause quoted strings containing commas to fail.
    """
    columns = []
    async with aiofiles.open(file, 'r') as report:
        rows = []
        async for line in report:
                if not columns:
                    print('Headers are ' + line)
                    columns = line.strip().split(delim)
                else:
                    csv_reader = csv.reader([line], skipinitialspace=True)
                    for data in csv_reader:
                        rows.append(dict(zip(columns, data)))
                    if len(rows) >= QUEUE_PULL_SIZE:
                        await q.put(rows)
                        rows = []
        if rows:
            await q.put(rows)
    print('Done reading')

async def send_data(client: AsyncClient, q: asyncio.Queue):
    """
    Pulls data off the Queue and sends it to AppSearch.
    """
    while True:
        data_list = await q.get()
        
        try:
            response = await client.index_documents(ENGINE, data_list)
        except Exception as e:
            print(e)
        q.task_done()

if __name__ == '__main__':
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")