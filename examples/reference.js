points = [
	{x:0, y:0, color:3}, {x:1, y:0, color:3}, {x:2, y:0, color:3}, {x:1, y:1, color:5}, {x:2, y:1, color:10}, {x:0, y:2, color:10}, {x:2, y:2, color:14}, 
];

// Offset
ox = 688;
oy = 318;
points.forEach(p => {p.x += ox; p.y += oy});

function paint(x, y, color, token, cb) {
	req = new XMLHttpRequest();
	req.open('POST', '/api/pixel');
	req.setRequestHeader("Content-type", "application/json");
	req.onerror = function () {
		console.error('Failed to paint:', x, y, color);
		console.log('Request:', req);
		console.log('Response:', req.response);
		console.log('Halting!');
	}
	req.onload = function (e) {
		console.log('Status:', req.status);
		console.log('Response:', req.response);
		res = JSON.parse(req.responseText);
		cb(res);
	}
	data = JSON.stringify({x:x, y:y, color:color, fingerprint: "30c435861c11298f63df83d2191da1ba", token: token})
	req.send(data);
}

function doPaint(point, token, done) {
	paint(next.x, next.y, next.color, null, function () {
		if (res.success) {
			done();
		} else if (res.waitSeconds > 0) {
			setTimeout(doPaint.bind(null, point, null, done), res.waitSeconds*1000);
		} else if (res.errors[0].msg == 'You must provide a token') {
			getNewToken(function (newtoken) {
				doPaint(point, newtoken, done);
			});
		} else {
			console.error('We received a weird error. Halting!')
		}
	});
}

function processNext() {
	if (points.length === 0) {
		console.log("We're finished.");
		return
	}

	next = points.pop();
	console.log(points);
	console.log(next);

	// Make sure you paint, and then process next.
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
