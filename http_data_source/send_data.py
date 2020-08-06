import sys
import os
import boto3
import datetime
import base64
import json
import logging as log

# Initialize base logging settings for job
log.basicConfig(stream=sys.stdout,
                format='%(asctime)s %(name)s [%(levelname)s]: %(message)s',
                datefmt='%d-%b-%y %H:%M:%S',
                level=log.INFO)

class FirehoseDataSource():
    def __init__(self):
        try:
            self.awsKey = os.environ['FIREHOSE_AWS_ACCESS_KEY']
        except:
            log.error("Missing FIREHOSE_AWS_ACCESS_KEY environment config!")
            exit(1)
        try:
            self.awsSecret = os.environ['FIREHOSE_AWS_SECRET']
        except:
            log.error("Missing FIREHOSE_AWS_SECRET environment config!")
            exit(1)
        try:
            self.firehoseName = os.environ['FIREHOSE_NAME']
        except:
            log.error("Missing FIREHOSE_NAME environment config!")
            exit(1)

        log.info("FIREHOSE_AWS_ACCESS_KEY: " + self.awsKey)
        log.info("FIREHOSE_AWS_SECRET: " + self.awsSecret)
        log.info("FIREHOSE_NAME: " + self.firehoseName)

        self.firehose = boto3.client('firehose')
        self.streamInfo = self.firehose.describe_delivery_stream(DeliveryStreamName=self.firehoseName)

    def run(self, dataType):
        self.numMessages = 1000
        self.batchSize = 100
        log.info("Sending {} messages to Firehose...".format(self.numMessages))
        buffer = []
        for i in range(1, self.numMessages + 1):
            log.info("{} - {}".format(dataType, i))
            testMessage = {
                'id' : i,
                'type' : dataType,
                'timestamp' : datetime.datetime.now().timestamp() * 1000
            }
            messageCsv = "{}, {}, {}\n".format(testMessage['id'], testMessage['type'], testMessage['timestamp'])
            buffer.append(messageCsv)
            if len(buffer) >= self.batchSize:
                recordArray = []
                for message in buffer:
                    recordArray.append({
                        'Data' : message.encode('utf-8')
                    })
                self.firehose.put_record_batch(
                    DeliveryStreamName=self.firehoseName,
                    Records=recordArray
                )
                buffer = []

    def printHelp(self):
        log.info("Message type must be one of:")
        log.info("")
        log.info("  succeed: Send a packet that the destination server will process successfully.")
        log.info("  fail: Send a packet that the destination server will quickly fail to process.")
        log.info("  fail_then_succeed: Send a packet that will fail at first, then eventually succeed.")
        log.info("  hang: Send a packet that will cause the request to hang.")
        log.info("")

if __name__ == "__main__":
    job = FirehoseDataSource()
    if len(sys.argv) > 1:
        dataType = sys.argv[1]
        dataTypes = ["succeed", "fail", "fail_then_succeed", "hang"]
        if not dataType in dataTypes:
            log.info("Invalid message type!")
            job.printHelp()
            exit(1)
        job.run(dataType)
    else:
        log.info("No message type specified!")
        job.printHelp()
        exit(1)