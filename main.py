import asyncio, queue
import logging
import os
import random
import sys

from forza_package import ForzaDataReader
from logger import create_logger
from producer import Producer

# define constants
IP_ADDRESS = '0.0.0.0'
PORT = 6667
CONN_STRING = os.environ['EVENTHUBS_CONNECTION_STRING']
EVENTHUB_NAME = os.environ['EVENTHUBS_NAME']

logger = create_logger(__name__, logging.DEBUG)

class AsyncForzaIO:
    '''AsyncForzaIO is a class that handles the async reading and writing of
       This class coordinates asyncronous execution of 2 concurrent task loopings:
            1. read_data() - reads data from Forza Horizon 4 UDP stream
            2. write_data() - sends data to Azure EventHub
        Boths tasks are repeting continuoesly until the program is terminated.
        Income UDP messages are read one by one and put in a queue.
        The queue is then emptied and all messages are sent to EventHub.
        The run() method is used to start both tasks and is the only one you should call direct.
    '''
    def __init__(self,
                 reader: ForzaDataReader,
                 producer: Producer) -> None:
        self.reader = reader
        self.producer = producer
        self.queue = queue.Queue()
        logger.debug('\tAsyncForzaIO object created')
        self._post_init()
    
    def _post_init(self) -> None:
        self.reader.start()
        logger.debug('\tForzaData.reader started')

    def _read_data(self) -> None:
        logger.debug('\tStarting read_data() loop')
        [self.queue.put_nowait(i.to_dict()) for i in self.reader.read() if i]
    
    async def _read_data_async(self) -> None:
        return await asyncio.to_thread(self._read_data)
    
    def _get_all_messages(self) -> list[str]:
        logger.debug('\tGetting messages from queue')
        items = []
        while True:
            try:
                items.append(self.queue.get_nowait())
            except queue.Empty:
                break
        logger.debug(f'\tGot {len(items)} messages from queue')
        return items
    
    async def _write_data(self) -> None:
        logger.debug('\tStarting write_data() loop')
        while True:
            items = self._get_all_messages()
            if items:
                logger.debug(f'\tSending {len(items)} messages to EventHub')
                await self.producer.send_events(items)
                logger.debug('\tMessages sent')
            else:
                logger.debug('\tNo messages to send, sleeping for 0.5 seconds')
                await asyncio.sleep(0.5)

    async def run(self) -> None:
        await asyncio.gather(self._read_data_async(), self._write_data())
        logger.debug('\tAsyncForzaIO.run() involked')

if __name__ == '__main__':
    logger.debug('Starting main function')
    if '/name' in sys.argv:
        driver_name = sys.argv[sys.argv.index('/name') + 1]
        logger.debug(f'/name argument found, setting driver name to: {driver_name}')
    elif '/n' in sys.argv:
        driver_name = sys.argv[sys.argv.index('/n') + 1]
        logger.debug(f'/n argument found, setting driver name to: {driver_name}')
    else:
        driver_name = f'driver{random.randint(1000, 9999)}'
        logger.debug(f'No driver name provided, setting driver name to: {driver_name}')
    
    reader = ForzaDataReader(ip = IP_ADDRESS, 
                             port = PORT, 
                             driver_name = driver_name)
    producer = Producer(connection_string = CONN_STRING, 
                        eventhub_name = EVENTHUB_NAME)
    
    forza_io = AsyncForzaIO(reader = reader, producer = producer)

    asyncio.run(forza_io.run())