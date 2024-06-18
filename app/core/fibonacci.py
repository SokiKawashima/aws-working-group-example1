import logging
import sys
from logging import Formatter, StreamHandler, getLogger

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


def fast_doubling_fibonacci(n: int) -> int:
    logger.info("Starting fast_doubling_fibonacci with n=%d", n)
    sys.set_int_max_str_digits(7000000)
    logger.debug("Set max string digits to 7000000")

    def _fib_recursive(n):
        logger.debug("Entering _fib_recursive with n=%d", n)
        if n == 0:
            logger.debug("Base case reached with n=0")
            return (0, 1)
        a, b = _fib_recursive(n // 2)
        logger.debug("Values from recursive call: a=%d, b=%d", a, b)

        c = a * (b * 2 - a)
        d = a * a + b * b
        logger.debug("Computed values: c=%d, d=%d", c, d)

        if n % 2 == 0:
            logger.debug("Even case for n=%d", n)
            return (c, d)
        else:
            logger.debug("Odd case for n=%d", n)
            return (d, c + d)

    result = _fib_recursive(n)[0]
    logger.info("Result of fast_doubling_fibonacci for n=%d is %d", n, result)
    return result


if __name__ == "__main__":
    import time

    logger.info("Script execution started")
    start = time.time()
    fib_value = fast_doubling_fibonacci(30000000)
    end = time.time()

    logger.info("Fibonacci value calculated")
    logger.info("fib_value: %d", fib_value)
    logger.info("Length of fib_value: %d", len(str(fib_value)))
    logger.info("Execution time: %f seconds", end - start)

    print(fib_value)
    print("===========")
    print(len(str(fib_value)))
    print("===========")
    print("time: ", end - start)
    logger.info("Script execution finished")
