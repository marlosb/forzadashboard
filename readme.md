# Forza Telemetry Data Exporter

##  Features
This program reads Forza telemetry data and sends it to Azure Event Hubs.
Data is read from UDP stream and write to Event Hubs concurrently to avoid performance bottlenecks. 

## Requeriments
- Python (tested on version 3.10)
- all packages listed on requirements.txt
- An Azure Event Hubs Namespace
- Azure Event Hubs connection string in an enviroment variable named `EVENTHUBS_CONNECTION_STRING`
- Azure Event Hubs name in an enviroment variable named `EVENTHUBS_NAME`
- Forza (both on PC or XBOX) set to send telemetry data to local IP of the machine runing this program

## Usage
```> python main.py /name <driver_name>```

A random driver name will be generated in case it is not provided as argument.