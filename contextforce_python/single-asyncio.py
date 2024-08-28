import asyncio
import httpx
from time import time

async def fetch(client, url):
    start_time = time()
    response = await client.get(url)
    end_time = time()
    print(f"Thread completed in: {int((end_time - start_time) * 1000)} milliseconds with status code: {response.status_code}")
    return response

async def main():
    url = "https://a.cdn.searchiq.co/test/amazon.html"  # Replace with your file URL
    number_of_threads = 200  # Number of parallel threads you want to run

    start_time = time()

    async with httpx.AsyncClient(http2=True) as client:
        tasks = [fetch(client, url) for _ in range(number_of_threads)]
        responses = await asyncio.gather(*tasks)

    end_time = time()
    print(f"Total time for all threads: {int((end_time - start_time) * 1000)} milliseconds")

if __name__ == "__main__":
    asyncio.run(main())
