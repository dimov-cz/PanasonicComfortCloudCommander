from typing import Optional
import queue
import logging
from .Response import Response

class ResponsesQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def add(self, response: Response):
        logging.debug(f"Adding response to queue: {response}")
        self.queue.put(response)        

    def get(self) -> Optional[Response]:
        try:
            message = self.queue.get(block=False)
        except queue.Empty:
            message = None
        return message