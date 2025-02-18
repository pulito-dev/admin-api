from .core.db import db_cl
from fastapi import FastAPI
from .core.config import config
from .rabbit.client import mq_cl
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_: FastAPI):
    # everything before yield is executed before the app starts up
    # set up rabbit
    await mq_cl.connect(str(config.RABBIT_URI))
    await mq_cl.setup_rpc_queues()

    # set up db
    db_cl.connect(str(config.DB_URI))
    await db_cl.create_schema(str(config.DB_SCHEMA))

    # create tables
    await db_cl.init_db()

    yield
    
    # everything after yield is execute after the app shuts down
    await mq_cl.disconnect()
    await db_cl.disconnect()


if not config.CI:
    app = FastAPI(
        title=config.TITLE,
        lifespan=lifespan
    )
else:
    app = FastAPI(
        title=config.TITLE
    )



from .routes.reports import reports_router


app.include_router(reports_router, prefix="/reports")


# @app.api_route("/")
# async def home():
#     txt = "".join(random.choices(string.ascii_letters, k=4))
#     await mq_cl.send_message("accommodations", {
#         "random_id": txt
#     })
#     print(f"SENT: {txt}")

#     return {
#         "hello": "world"
#     }
