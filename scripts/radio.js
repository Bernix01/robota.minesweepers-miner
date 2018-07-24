#!/usr/bin/env node

'use strict';

const rosnodejs = require('rosnodejs');

const SX127x = require('sx127x');


(async () => {
  await rosnodejs.initNode('radio', {
    onTheFly: true
  });
  const ComRadioRequest = rosnodejs.require('minesweepers').srv.ComRadio;
  
  const nh = rosnodejs.nh;


  var sx127x = new SX127x({
    frequency: 433e6
  });


  var count = 0;

  // open the device
  sx127x.open(function (err) {
    console.log('open', err ? err : 'success');

    if (err) {
      throw err;
    }

    const service = nh.advertiseService('/send_message', ComRadioRequest, (req, resp) => {
      console.log(req)
      sx127x.write(new Buffer(req.str), function (err) {
        console.log('\t', err ? err : 'success');
        resp = err ? err : 'Ok';
      });
      return true;
    });
  });



  process.on('SIGINT', function () {
    // close the device
    sx127x.close(function (err) {
      console.log('close', err ? err : 'success');
      process.exit();
    });
  });

})();