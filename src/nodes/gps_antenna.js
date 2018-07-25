#!/usr/bin/env node

"use strict";

const rosnodejs = require("rosnodejs");
const GPS = require("gps");
const angles = require("angles");
const SerialPort = require("serialport");
const Readline = SerialPort.parsers.Readline;
const Delimiter = SerialPort.parsers.Delimiter;

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
  
  const parser = new Readline();
  const delimiter = new Delimiter({ delimiter: "\r\n" });
  port.pipe(delimiter);
  port.pipe(parser);

  port.write("AT\r\n");
  port.write("AT+CGNSPWR=1\r\n");
  port.write("AT+CGNSTST=1\r\n");

  const gps = new GPS();
  nh.getParam("gps_start_point").then(GPS_START_POINT => {
      gps.on("data", function(data) {
        // rosnodejs.log.info(data, gps.state);
        // rosnodejs.log.info(JSON.stringify(data));
        const state = gps.state;
        if(state.lat)
        const msg = new GPSMessage();
        msg.data = {};
        pub.publish(msg);
      });

      port.on("data", function(data) {
        const strData = data.toString("utf8");
        if (strData == "OK\r\n") {
          rosnodejs.log.info("Enabled GPS");
        } else {
          gps.updatePartial(strData);
        }
      });
    })
    .catch(error => {
      rosnodejs.log.error("Can't get gps_start_point, GPS Disabled");
    });
})();
