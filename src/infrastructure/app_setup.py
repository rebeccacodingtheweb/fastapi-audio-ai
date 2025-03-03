import asyncio
from contextlib import asynccontextmanager

from db import mongo_setup
from infrastructure import app_secrets
from services import background_service, web_sync_service

development_mode: bool = True


@asynccontextmanager
async def app_lifespan(_):
    if development_mode:
        # Default to local mongodb with default port and no auth for dev.
        await mongo_setup.init_connection(
            "xray_podcasts", server=app_secrets.mongo_host, port=app_secrets.mongo_port
        )
    else:
        # This is what you'd use connect to a production server
        # Pass the username, password, server, etc.
        # await mongo_setup.init_connection(...)
        ...

    # Start the background workers

    asyncio.create_task(web_sync_service.load_starter_data())
    asyncio.create_task(background_service.worker_function())

    # TODO: Register search task

    yield

    # Nothing to clean up.
