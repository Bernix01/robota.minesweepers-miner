#!/usr/bin/env node

'use strict';

const rosnodejs = require('rosnodejs');

const SX127x = require('sx127x');
const SerialPort = require('serialport');
const Readline = SerialPort.parsers.Readline;
const Delimiter = SerialPort.parsers.Delimiter;
const GPS = require('gps');


(async () => {
  await rosnodejs.initNode('gps', {
    onTheFly: true
  });
  const GPSMessage = rosnodejs.require('minesweepers').msg.Gps;

  const nh = rosnodejs.nh;
  let pub = nh.advertise('/gps_data', GPSMessage);

  const port = new SerialPort('/dev/serial0', { 
    baudRate: 9600
  });
  const parser = new Readline();
  const delimiter = new Delimiter({ delimiter: '\r\n'});
  port.pipe(delimiter);
  port.pipe(parser);

  port.write('AT\r\n');
  port.write('AT+CGNSPWR=1\r\n');
  port.write('AT+CGNSTST=1\r\n');

  const gps = new GPS;

  gps.on('data', function (data) {
    rosnodejs.log.info(data, gps.state);
    // rosnodejs.log.info(JSON.stringify(data));
  });

  port.on('data', function (data) {
    const strData = data.toString('utf8')
    if (strData == 'OK\r\n') {
      rosnodejs.log.info("Enabled GPS");
    } else {
      gps.updatePartial(strData);
    }
  });

})();