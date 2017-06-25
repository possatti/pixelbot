points = [
  ${points}
].reverse();

// Offset
ox = ${ox};
oy = ${oy};
points.forEach(p => {p.x += ox; p.y += oy});

fingerprint = "${fingerprint}"

function paint(x, y, color, fingerprint, token) {
  data = JSON.stringify({x:x, y:y, color:color, fingerprint: fingerprint, token: token})

  return fetch("/api/pixel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: data
  });
}

function doPaint(point, token, done) {
  paint(point.x, point.y, point.color, fingerprint, token)
    .then(function (response) {
      console.log('Request successful. Response:', response)
      response.json()
        .then(function (json_body) {
          console.log('Response body:', json_body);
          if (response.ok) {
            done();
          } else if (json_body.waitSeconds > 0) {
            console.log('Ok! Ok! We will wait', json_body.waitSeconds, 'seconds then.')
            setTimeout(doPaint.bind(null, point, null, done), json_body.waitSeconds*1000);
          } else if (json_body.errors[0].msg == 'You must provide a token') {
            console.log('Oh... We need a token? Let\'s try to get one then.')
            getNewToken(function (newtoken) {
              doPaint(point, newtoken, done);
            });
          } else {
            console.error('We have received an unexpected error. Body:', json_body);
            console.error('Halting!');
          }
        })
        .catch(function (reason) {
          console.error('Failed to read body of response. Reason:', reason);
        });
    })
    .catch(function (reason) {
      console.error('Failed to paint:', point.x, point.y, point.color);
      console.error('Due to the following reason:', reason);
      console.error('Are you sure everything is fine with your internet connection?');
      console.log('Halting for now.');
    });
}

function processNext() {
  if (points.length === 0) {
    var notification = new Notification("Your drawing is ready. Yey!");
    console.log("We're finished.");
    return
  }

  next = points.pop();
  console.log('This pixel will now be painted:', next);

  // Make sure you paint, and then process next point.
  doPaint(next, null, processNext);
}

oldCaptchaHandler = onCaptcha;
function getNewToken(cb) {
  var notification = new Notification("You may need to solve a captcha.");
  grecaptcha.execute();

  function newCaptchaHandler(token) {
    console.log('The captcha was solved:', arguments);
    cb(token);
    // Invoke the old captcha handler. So that everything keeps going normal.
    oldCaptchaHandler.apply(this, arguments);
  }
  window.onCaptcha = newCaptchaHandler;
}

processNext();
