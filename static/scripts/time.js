function startClock() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
  //  var s = today.getSeconds();
    m = checkTime(m);
    //s = checkTime(s);

    if (h >= 12) {
      ampm = "pm"
      if (h > 12) {
        h = h -12
      }
    } else {
      ampm = "am"
    }

    document.getElementById('clock').innerHTML =
    "<h1>" + h + ":" + m + ampm + "</h1>";
    var t = setTimeout(startClock, 500);
  }
  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }
