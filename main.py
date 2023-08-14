import asyncio, queue
import concurrent.futures
import os

from forza_package import ForzaDataReader
from producer import Producer

# define constants
IP_ADDRESS = '0.0.0.0'
PORT = 6667
CONN_STRING = os.environ['EVENTHUB_CONNECTION_STRING']
EVENTHUB_NAME = os.environ['EVENTHUB_NAME']

class AsyncForzaIO:
    '''AsyncForzaIO is a class that handles the async reading and writing of
       This class coordinates asyncronous execution of 2 concurrent task loopings:
            1. read_data() - reads data from Forza Horizon 4 UDP stream
            2. write_data() - sends data to Azure EventHub
        Boths tasks are repeting continuoesly until the program is terminated.
        Income UDP messages are read one by one and put in a queue.
        The queue is then emptied and all messages are sent to EventHub.
    '''
    def __init__(self,
                 reader: ForzaDataReader,
                 producer: Producer) -> None:
        self.reader = reader
        self.producer = producer
        self.queue = queue.Queue()
        self._post_init()
    
    def _post_init(self) -> None:
        self.reader.start()

    def read_data(self) -> None:
        print('\tStarting read_data() loop')
        [self.queue.put_nowait(i.to_dict()) for i in self.reader.read()]
    
    def _get_all_messages(self) -> list[str]:
        items = []
        while True:
            try:
                items.append(self.queue.get_nowait())
            except queue.Empty:
                break
        return items
    
    async def write_data(self) -> None:
        print('\tStarting write_data() loop')
        while True:
            items = self._get_all_messages()
            if items:
                await self.producer.send_events(items)

async def main():
    print('Starting async loopings')

    reader = ForzaDataReader(ip = IP_ADDRESS, port = PORT)
    producer = Producer(connection_string = CONN_STRING, 
                        eventhub_name = EVENTHUB_NAME)
    forza_io = AsyncForzaIO(reader = reader, producer = producer)

    future_writes = asyncio.ensure_future(forza_io.write_data())

    pool = concurrent.futures.ThreadPoolExecutor()
    future_reads = asyncio.get_event_loop().run_in_executor(
                     pool, forza_io.read_data)
    
    done, pending = await asyncio.wait([future_reads],)
    print("async main() loop exited !")


if __name__ == '__main__':
    asyncio.run(main())