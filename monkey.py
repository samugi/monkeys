import requests
from random import uniform, choice
from time import sleep
from concurrent.futures import ProcessPoolExecutor
import logging
import asyncio

PATHS = [
    '/foo?q=test',
    '/bar?q=test2'
]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

class Monkey:

    def __init__(self, endpoint, num_req, monkey_name="bob"):
        self.endpoint = endpoint
        self.num_req = num_req
        self.monkey_name = monkey_name

    def unleash(self):
        try:
            for i in range(0, self.num_req):
                path = choice(PATHS)
                resp = requests.get(self.endpoint + path)
                if resp.status_code != 200:
                    logging.error(f"Monkey: {self.monkey_name} - [error]: {resp.text} from {path}")
                else:
                    logging.info(f"Monkey: {self.monkey_name} - All good from {path}")
                self.rand_sleep(0, 3)
        except Error as er:
            logging.error(er)

    def rand_sleep(self, start, end):
        sleep(uniform(start, end))

   

if __name__ == "__main__":
    N_MONKEYS = 30

    executor = ProcessPoolExecutor(N_MONKEYS)
    loop = asyncio.get_event_loop()

    for i in range(N_MONKEYS):
        loop.run_in_executor(executor, Monkey("http://10.10.10.10", 100, i).unleash)
    
    loop.run_forever()
