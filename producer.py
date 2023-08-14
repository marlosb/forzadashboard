import json

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

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

    async def prepare_events(self, events_list: list[dict]):
        '''Prepare events to be sent to Azure Event Hub
        Args:
            events_list (list[dict]): list of events to be sent to Azure Event Hub
        Returns:
            event_data_batch (EventDataBatch): batch of events to be sent to Azure Event Hub
        '''
        async with self.producer:
            print('Creating batch ot events')
            event_data_batch = await self.producer.create_batch()
            print(f'Adding {len(events_list)} events to batch')
            for event in events_list:
                event_str = json.dumps(event)
                event_data_batch.add(EventData(event_str))
        return event_data_batch

    async def send_events(self, events_list: list[dict]) -> None:
        '''Send events to Azure Event Hub
        Args:
            events_list (list[dict]): list of events to be sent to Azure Event Hub
        Returns:
            None
        '''

        event_data_batch = await self.prepare_events(events_list = events_list)
        print('sending batch of events to Azure Event Hub')
        async with self.producer:
            await self.producer.send_batch(event_data_batch)

    def close(self) -> None:
        '''Close connection to Azure Event Hub'''
        self.producer.close()