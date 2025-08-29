from __future__ import annotations
import asyncio
import httpx
from fraud_detection.simulator.stream import generate_transactions


API_URL = "http://127.0.0.1:8000/predict"


async def main():
    async with httpx.AsyncClient(timeout=5.0) as client:
        for tx in generate_transactions(200):
            resp = await client.post(API_URL, json=tx)
            print(resp.status_code, resp.text)
            await asyncio.sleep(0.05)


if __name__ == "__main__":
    asyncio.run(main())

