import uvicorn
from main import app
from fastapi import time


def run_server():
    uvicorn.run(
        app, port=8000, log_level="error"
    )  # starts your fast api app from main.py running uvicorn


from contextlib import contextmanager
from multiprocessing import Process


@contextmanager
def run_server_in_process():
    p = Process(
        target=run_server
    )  # starts the server in another process(background process)
    p.start()  # starts the server
    time.sleep(
        2
    )  # give the server a second to start # waits for the server to fully boot before you send requests
    print("Server is running in a seprate process")
    yield  # allows you to run other code (like making api calls) while the server is running
    p.terminate()  # automatically shuts dow the server
