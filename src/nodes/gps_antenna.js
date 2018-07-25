#!/usr/bin/env node

"use strict";

const rosnodejs = require("rosnodejs");
const GPS = require("gps");
const SerialPort = require("serialport");
const Readline = SerialPort.parsers.Readline;

(async () => {
  await rosnodejs.initNode("gps", {
    onTheFly: true
  });
  const GPSMessage = rosnodejs.require("minesweepers").msg.Gps;

  const nh = rosnodejs.nh;
  let pub = nh.advertise("/gps_data", GPSMessage);

  const port = new SerialPort("/dev/serial0", {
    baudRate: 9600
  });

  const parser = new Readline({ delimiter: '\r\n' });
  port.pipe(parser);

  port.write("AT\r\n");
  port.write("AT+CGNSPWR=1\r\n");
  port.write("AT+CGNSTST=1\r\n");

  const gps = new GPS();
  nh.getParam("GPS_START_POINT")
    .then(GPS_START_POINT => {
      gps.on("data", function(data) {
        // rosnodejs.log.info(data, gps.state);
        // rosnodejs.log.info(JSON.stringify(data));
        const state = gps.state;
        if (state && state.lat && state.lon) {
          const msg = new GPSMessage();
          const distance = gps.distance(GPS_START_POINT[0],GPS_START_POINT[1],state.lat,state.lon)
          msg.data = {
            lat: state.lat,
            lng: state.lon,
            distance: distance
          };
          pub.publish(msg);
        }
      });

      parser.on("data", function(data) {
        if (data == "OK") {
          rosnodejs.log.info("Enabled GPS");
        } else {
          gps.updatePartial(data);
        }
      });
    })
    .catch(error => {
      rosnodejs.log.error("Can't get gps_start_point, GPS Disabled");
    });
})();
