# Kinesis Data Firehose 

This repository is a simple test of the Amazon Kinesis Data Firehose service. 

## Data Source Test
`http_data_source` contains a python script that will send test data directly to Firehose.

### Dependency Setup
Dependencies for this script are managed with Conda.

Common development tasks:
- To load the environment, run `conda env create -f environment.yml`.
- To save updated dependencies to the environment file, run `conda env export --from-history > environment.yml`. 
- To activate the environment: `conda activate firehose-demo-data-source`.
- To deactivate the environment: `conda deactivate`.

### Environment Setup
You must have the following variables on the environment:

- `FIREHOSE_AWS_ACCESS_KEY` - The AWS access key ID to access the Firehose.
- `FIREHOSE_AWS_SECRET` - The AWS secret to access the Firehose.
- `FIREHOSE_NAME` - The name of the firehose to push data to.

### Usage
To run the script, use `send_data.sh <type>`. The `<type>` parameter should be one of the following options, each of which will test a different behavior of the destination server and Firehose retry logic:

- `succeed` - Send a JSON packet that the destination server will process successfully.
- `fail` - Send a JSON packet that the destination server will quickly fail to process.
- `hang` - Send a packet that will cause the request to hang.

## Data Destination Test
`http_data_dest` contains a simple Node.js server which can ingest data from Firehose via the HTTP destination. This server should be run somewhere accessible from the public internet, and Firehose configured to send data to the destination. 

The server will behave differently depending on the contents of the packets sent to its endpoint, discussed above. The server can either succeed, fail, or hang, testing Firehose's timeout and retry intervals.
