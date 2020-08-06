var express = require('express');
var winston = require('winston');
var parse = require('csv-parse/lib/sync')
var log = winston.loggers.get('default'); 

var router = express.Router();

// Parse and respond to the Firehose data
// Data is batched, and the request schema is at: 
// https://docs.aws.amazon.com/firehose/latest/dev/httpdeliveryrequestresponse.html
router.post('/', function(req, res, next) {
  ingestRecords = req.body.records;
  ingestRequestId = req.body.requestId;

  console.log(`Received batch of ${ingestRecords.length} records to ingest...`)
  
  rawCsvRecords = []
  ingestRecords.forEach(ingestRecord => {
    // Decode the data from the record from its base64 representation to csv
    ingestRecordDecoded = Buffer.from(ingestRecord.data, 'base64').toString('utf-8');
    rawCsvRecords.push(ingestRecordDecoded);
  });

  // Parse all records from csv to objects
  csvRecords = parse(rawCsvRecords.join(""), {
    columns: ["id", "type", "timestamp"],
    trim: true
  });

  // Handle each individual record
  shouldFail = false
  shouldHang = false
  statusCode = 200
  csvRecords.forEach(csvRecord => {
      console.log(csvRecord)
      index = csvRecord.id;
      type = csvRecord.type;
      timestamp = csvRecord.timestamp;

      if (type === "fail") {
        shouldFail = true
      }
      if (type === "hang") {
        shouldHang = true
      }
  });

  ingestFinishTime = Date.now();
  
  if (shouldFail) {
    // Fail; send a failure response
    console.log("Sending failure message for record batch!")
    res.status(400).send({
      "requestId": ingestRequestId,
      "timestamp" : ingestFinishTime,
      "errorMessage" : "Unable to process the records"
    });
  } else if (shouldHang) {
    // Hang; don't send a response at all
    console.log("Sending no message (hanging) for record batch!")
  } else {
    console.log("Sending success message for record batch!")
    // Succeed
    res.status(200).send({
      "requestId": ingestRequestId,
      "timestamp" : ingestFinishTime
    });
  }
});

module.exports = router;
