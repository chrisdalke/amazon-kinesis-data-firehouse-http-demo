import sys
import os
import boto3
import logging as log

# Initialize base logging settings for job
log.basicConfig(stream=sys.stdout,
                format='%(asctime)s %(name)s [%(levelname)s]: %(message)s',
                datefmt='%d-%b-%y %H:%M:%S',
                level=log.INFO)

class FirehoseDataSource():
    def __init__(self):
        self.numMessages = 1000
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
        log.info("Sending data to Firehose...")

    def printHelp(self):
        log.info("Message type must be one of:")
        log.info("")
        log.info("  succeed: Send a JSON packet that the destination server will process successfully.")
        log.info("  fail: Send a JSON packet that the destination server will quickly fail to process.")
        log.info("  fail_then_succeed: Send a JSON packet that will fail at first, then eventually succeed.")
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