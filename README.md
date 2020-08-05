# Kinesis Data Firehose 

This repository is a simple test of the Amazon Kinesis Data Firehose service. 

## Data Source
`http_data_source` contains a set of bash scripts that will send test data directly to Firehose via the HTTP PUT endpoint.

## Data Destination
`http_data_dest` contains a simple Node.js server which can ingest data from Firehose via the HTTP destination. This server should be run somewhere accessible from the public internet, and Firehose configured to send data to the destination. 

The server will behave differently depending on the contents of the packets sent to its endpoint. The server can either succeed, fail, or hang, testing Firehose's timeout and retry intervals.
