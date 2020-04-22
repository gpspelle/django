$(function() {

	//var roomName = document.getElementById("room").getAttribute("room-name");
		
	// When we're using HTTPS, use WSS too.
	var ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";
	var chatSocket = new WebSocket(ws_scheme + window.location.host + '/ws/chat/chat/');
	var imageSocket = new WebSocket(ws_scheme + window.location.host + '/ws/chat/image/');

	chatSocket.onmessage = function(e) {
		var data = JSON.parse(e.data);
		var message = data['message'];
		document.querySelector('#chat-log').value += ('Message received: ');
		document.querySelector('#chat-log').value += (message + '\n');

	};

	imageSocket.onmessage = function(e) {

		var data = JSON.parse(e.data);
		var url = data['message'];
		var src_url = 'data:image/jpeg;base64,' + url;
		$('#image').attr('src', src_url);

	};

	chatSocket.onopen = function(e) {
		console.log("Chat WebSocket is open now.");
		document.querySelector('#chat-log').value += ('Chat webscoket working.\n')
	}

	imageSocket.onopen = function(e) {
		console.log("Image WebSocket is open now.");
		document.querySelector('#chat-log').value += ('Image websocket working.\n')
	}


	chatSocket.onclose = function(e) {
		document.querySelector('#chat-log').value += ('Chat Socket closed unexpectedly, please reload the page.\n')
		//this.chatSocket = new WebSocket(chatSocket.url);
	};

	imageSocket.onclose = function(e) {
		document.querySelector('#chat-log').value += ('Image Socket closed unexpectedly, please reload the page.\n')
		//this.chatSocket = new WebSocket(chatSocket.url);
	};



	document.querySelector('#chat-message-input').focus();
	document.querySelector('#chat-message-input').onkeyup = function(e) {
		if (e.keyCode === 13) {	// enter, return
			document.querySelector('#chat-message-submit').click();
		}
	};

	document.querySelector('#chat-message-submit').onclick = function(e) {
		var messageInputDom = document.querySelector('#chat-message-input');
		var message = messageInputDom.value;
		document.querySelector('#chat-log').value += ('Message sent: ');
		document.querySelector('#chat-log').value += (message + '\n');
		chatSocket.send(JSON.stringify({
			'message': message, 'recipient': 'chat_chatesp32'
		}));

		messageInputDom.value = '';
	};

	document.querySelector('#button-handler').onclick = function (e) {

		var message = e.target.id;
		document.querySelector('#chat-log').value += ('Message sent: ');
		document.querySelector('#chat-log').value += (message + '\n');

		chatSocket.send(JSON.stringify({
			'message': message, 'recipient': 'chat_chatesp32'
		}));
	};

	var length;
	var count;
	var interval;
	var lines;
	$('#length').val(100);
	$('#count').val(5);
	$('#graph').attr('width', length * 2).attr('height', length * 2);

	// Creates svg element, returned as jQuery object
	// source: https://stackoverflow.com/a/29017767
	function $s(elem) {
		return $(document.createElementNS('http://www.w3.org/2000/svg', elem));
	}

	// source: https://stackoverflow.com/a/27572056
	function findNewPoint(x, y, angle, distance) {
		var result = {};
		result.x = Math.round(Math.cos(angle * Math.PI / 180) * distance + x);
		result.y = Math.round(Math.sin(angle * Math.PI / 180) * distance + y);
		return result;
	}

	function setup() {
		length = parseInt($('#length').val());
		count = parseInt($('#count').val());
		interval = 360 / count;

		$('#graph').empty();
		$('#graph').attr('width', length * 2).attr('height', length * 2);
		lines = [];
		var polygonPoints = [];
		for (var i = 0; i < count; i++) {
			var angle = interval * i;
			lines[i] = {
				max: findNewPoint(length, length, (interval * i) - 90, length),
				score: findNewPoint(length, length, (interval * i) - 90, length * Math.random())
			};
			polygonPoints[i] = lines[i].score.x + ',' + lines[i].score.y;
			var attributes = {
				x1: length,
				y1: length,
				x2: lines[i].max.x,
				y2: lines[i].max.y
			};
			$s('line').attr(attributes).appendTo('#graph');
		}
		//console.dir(lines);
		//console.dir(polygonPoints.join(' '));
		$s('polygon').attr({'points': polygonPoints}).appendTo('#graph');
	}

	$('#setup').click(setup);
	setup();


});
