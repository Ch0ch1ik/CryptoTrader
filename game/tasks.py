from celery import shared_task
from game.utils import connect
import asyncio


@shared_task
def update_data():
    asyncio.run(connect())
