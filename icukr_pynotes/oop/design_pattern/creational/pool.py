"""
*introduction
This pattern is used when creating an object is costly (and they are
created frequently) but only a few are used at a time. With a Pool we
can manage those instances we have as of now by caching them. Now it
is possible to skip the costly creation of an object if one is
available in the pool.

*example
this example is about mysql connections pool, keep MAX_CONNECTIONS connection in queue.

"""


import queue


class ObjectPool:
    def __init__(self, q: queue.Queue):
        self._q = q
        self.item = None

    def __enter__(self):
        if self.item is None:
            self.item = self._q.get()
        return self.item

    def __exit__(self, exc_type, exc_value, traceback):
        if self.item is not None:
            self._q.put(self.item)
            self.item = None

    def __del__(self):
        if self.item is not None:
            self._q.put(item)
            self.item = None


MAX_CONNECTIONS = 10


def initialize_mysql_connections() -> queue.Queue:
    q = queue.Queue()
    for i in range(MAX_CONNECTIONS):
        q.put(f"mysqlConnection{i}")
    return q


if __name__ == "__main__":
    q = initialize_mysql_connections()
    for _ in range(12):
        with ObjectPool(q) as pool:
            print(pool)
