import queue
from .Response import Response

class ResponsesQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def add(self, response: Response):
        self.queue.put(response)        

    def get(self) -> Response:
        try:
            message = self.queue.get(block=False)
        except queue.Empty:
            message = None
        return message