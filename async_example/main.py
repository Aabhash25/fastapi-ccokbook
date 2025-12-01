from fastapi import FastAPI

app = FastAPI()

# ENDPOINT THAT SLEEPS FOR 1 SECOND
import time


@app.get("/sync")
def read_sync():
    time.sleep(2)
    return {"message": "Synchronous blocking endpoint"}


# Now, let’s create the same endpoint for the async def version. The sleeping operation will
# be the sleep function from the asyncio module:

import asyncio


@app.get("/async")
async def read_async():
    await asyncio.sleep(2)
    return {"message": "Asynchronous non-blocking endpoint"}

