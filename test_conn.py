# test_conn.py
import asyncio

import asyncpg


async def main():
    try:
        conn = await asyncpg.connect(user='postgres', password='password',
                                    database='qrs', host='127.0.0.1', port=5432)
        print("connected")
        await conn.close()
    except Exception as e:
        print("ERROR:", e)

asyncio.run(main())
