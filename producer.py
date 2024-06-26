import json
import logging

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

from logger import create_logger

logger = create_logger(__name__, logging.DEBUG)

class Producer:
    '''Class to send events to Azure Event Hub'''
    def __init__(self, 
                connection_string: str, 
                eventhub_name: str) -> None:
        '''Initialize Producer class
        Args:
            connection_string (str): connection string to Azure Event Hub
            eventhub_name (str): name of the event hub
        '''
        self.producer = EventHubProducerClient.from_connection_string(
                        conn_str=connection_string,
                        eventhub_name=eventhub_name)
        logger.debug(f'Producer object created with eventhub_name: {eventhub_name}')

    async def prepare_events(self, events_list: list[dict]):
        '''Prepare events to be sent to Azure Event Hub
        Args:
            events_list (list[dict]): list of events to be sent to Azure Event Hub
        Returns:
            event_data_batch (EventDataBatch): batch of events to be sent to Azure Event Hub
        '''
        async with self.producer:
            logger.info('Creating batch ot events')
            event_data_batch = await self.producer.create_batch()
            logger.info(f'Adding {len(events_list)} events to batch')
            for event in events_list:
                event_str = json.dumps(event)
                event_data_batch.add(EventData(event_str))
        logger.debug(f'batch of {len(events_list)} events created')
        return event_data_batch

    async def send_events(self, events_list: list[dict]) -> None:
        '''Send events to Azure Event Hub
        Args:
            events_list (list[dict]): list of events to be sent to Azure Event Hub
        Returns:
            None
        '''

        logger.info('sending batch of events to Azure Event Hub')
        if len(events_list) > 75:
            logger.warning(f'batch of {len(events_list)} events is too big. Splitting into 2 batches (recursively)')
            events_list_overflow = events_list[75:]
            events_list = events_list[:75]
            await self.send_events(events_list = events_list_overflow)

        event_data_batch = await self.prepare_events(events_list = events_list)
        try:
            await self.producer.send_batch(event_data_batch)
        except Exception as e:
            logger.error(f'Error sending batch of events to Azure Event Hub: {e}')
        finally:
            await self.producer.close()

        logger.debug(f'batch of {len(events_list)} events sent to Azure Event Hub')

    def close(self) -> None:
        '''Close connection to Azure Event Hub'''
        self.producer.close()