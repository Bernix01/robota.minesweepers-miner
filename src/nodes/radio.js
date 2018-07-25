#!/usr/bin/env node

"use strict";

const rosnodejs = require("rosnodejs");

const SX127x = require("sx127x");

(async () => {
  await rosnodejs.initNode("radio", {
    onTheFly: true
  });
  const ComRadioRequest = rosnodejs.require("minesweepers").srv.ComRadio;

  const nh = rosnodejs.nh;

  var sx127x = new SX127x({
    frequency: 433e6
  });

  // open the device
  sx127x.open(function(err) {
    console.log("open", err ? err : "success");

    if (err) {
      throw err;
    }

    const service = nh.advertiseService(
      "/send_message",
      ComRadioRequest,
      (req, resp) => {
        sx127x.write(new Buffer(req.str), function(err) {
          resp = err ? false : true;
        });
        return true;
      }
    );
  });

  process.on("SIGINT", function() {
    // close the device
    sx127x.close(function(err) {
      process.exit();
    });
  });
})();
