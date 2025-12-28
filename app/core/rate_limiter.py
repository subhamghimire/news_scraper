import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, delay_seconds: float = 2):
        self.delay = delay_seconds
        self.last_call = defaultdict(float)

    def wait(self, domain: str) -> None:
        now = time.time()
        last = self.last_call[domain]
        if now - last < self.delay:
            time.sleep(self.delay - (now - last))
        self.last_call[domain] = time.time()

