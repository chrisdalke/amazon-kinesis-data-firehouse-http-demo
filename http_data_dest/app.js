var express = require('express');
var path = require('path');
var logger = require('morgan');

var indexRouter = require('./routes/index');
var ingestRouter = require('./routes/ingest');

var app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use('/', indexRouter);
app.use('/ingest', ingestRouter);

module.exports = app;
