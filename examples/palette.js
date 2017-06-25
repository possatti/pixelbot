points = [
  {x:0, y:0, color:0}, {x:1, y:0, color:1}, {x:2, y:0, color:2}, {x:3, y:0, color:3}, {x:4, y:0, color:4}, {x:5, y:0, color:5}, {x:6, y:0, color:6}, {x:7, y:0, color:7}, {x:0, y:1, color:8}, {x:1, y:1, color:9}, {x:2, y:1, color:10}, {x:3, y:1, color:11}, {x:4, y:1, color:12}, {x:5, y:1, color:13}, {x:6, y:1, color:14}, {x:7, y:1, color:15}, 
];

// Offset
ox = 845;
oy = -190;
points.forEach(p => {p.x += ox; p.y += oy});

fingerprint = "0013c7fc94b0e5847b294f751bec4aaf"

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
      console.log('Request succeful. Response:', response)
      console.log('All arguments:', arguments);
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
    .catch(function (argument) {
      console.error('Failed to paint:', paint.x, paint.y, paint.color);
      console.error('Due to the following reason:', reason);
      console.error('All arguments', arguments);
      console.log('Halting? I am confused... I don\' know...');
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
    oldCaptchaHandler(arguments);
  }
  window.onCaptcha = newCaptchaHandler;
}

processNext();
