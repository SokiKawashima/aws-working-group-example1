import logging
from logging import BASIC_FORMAT, Formatter, StreamHandler, getLogger
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from .core.fibonacci import fast_doubling_fibonacci

app = FastAPI()

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
st_handler = StreamHandler()
st_handler.setLevel(logging.INFO)
st_handler.setFormatter(
    Formatter(
        "%(asctime)s [%(levelname)s] (%(filename)s | %(funcName)s | %(lineno)s) %(message)s"
    )
)
logger.addHandler(st_handler)


@app.get("/")
def root():
    logger.info("in root method")
    return {"message": "Hello World!!"}


@app.get("/fib")
def getFibonacci(
    n: Annotated[
        int,
        Query(
            title="n",
            description="number to calculate fibonacci for",
            gt=0,
            le=30000000,
        ),
    ]
):
    logger.info("Received request to calculate Fibonacci for n=%s", n)
    try:
        result = fast_doubling_fibonacci(n)
        logger.info("Successfully calculated Fibonacci for n=%s", n)
    except Exception as e:  # ValueError, OverflowErrorはFastAPIのQueryで処理される
        logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"result": result}
