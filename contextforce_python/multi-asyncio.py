import asyncio
import httpx
from concurrent.futures import ProcessPoolExecutor
from time import time

async def fetch(client, url):
    start_time = time()
    response = await client.get(url)
    end_time = time()
    print(f"Task completed in: {int((end_time - start_time) * 1000)} milliseconds with status code: {response.status_code}")
    return response.text

async def fetch_in_process(urls):
    async with httpx.AsyncClient(http2=True) as client:
        tasks = [fetch(client, url) for url in urls]
        await asyncio.gather(*tasks)

def run_fetch_in_event_loop(urls):
    asyncio.run(fetch_in_process(urls))

async def main():
    url = "https://a.cdn.searchiq.co/test/amazon.html"  # Replace with your file URL
    number_of_requests = 200  # Total number of requests
    number_of_processes = 4   # Number of parallel processes

    urls_per_process = [url] * (number_of_requests // number_of_processes)

    start_time = time()

    with ProcessPoolExecutor(max_workers=number_of_processes) as process_pool:
        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(process_pool, run_fetch_in_event_loop, urls_per_process) for _ in range(number_of_processes)]
        await asyncio.gather(*tasks)

    end_time = time()
    print(f"Total time for all tasks: {int((end_time - start_time) * 1000)} milliseconds")

if __name__ == "__main__":
    asyncio.run(main())
