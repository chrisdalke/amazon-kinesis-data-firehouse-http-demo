var express = require('express');
var path = require('path');
var logger = require('morgan');
var winston = require('winston');

var ingestRouter = require('./routes/ingest');

winston.loggers.add('default', {
    console: {
        colorize: 'true',
        handleExceptions: true,
        json: false,
        level: 'silly',
        label: 'default',
    }
});

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/ingest', ingestRouter);

module.exports = app;
