from app import db
import config
import asyncio


async def main():
    await db.set_bind(config.DATABASE_URL)
    await db.gino.create_all()


asyncio.get_event_loop().run_until_complete(main())