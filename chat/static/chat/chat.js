$(function() {

	var roomName = "{{ room_name|escapejs }}";

		
	// When we're using HTTPS, use WSS too.
	var ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";
	var chatSocket = new ReconnectingWebSocket(ws_scheme + window.location.host + '/ws/chat/bla');

	//var wss_protocol = (window.location.protocol == 'https:') ? 'wss://': 'ws://';
	//var chatSocket = new WebSocket(
	//wss_protocol + window.location.host + '/ws/chat/' + roomName + '/'
	//);

	chatSocket.onmessage = function(e) {
		var data = JSON.parse(e.data);
		var message = data['message'];
		document.querySelector('#chat-log').value += ('Message received: ');
		document.querySelector('#chat-log').value += (message + '\n');

	};

	chatSocket.onclose = function(e) {
		console.log('closed');
		this.chatSocket = new WebSocket(chatSocket.url);
	};

	document.querySelector('#chat-message-input').focus();
	document.querySelector('#chat-message-input').onkeyup = function(e) {
		if (e.keyCode === 13) {  // enter, return
			document.querySelector('#chat-message-submit').click();
		}
	};

	document.querySelector('#chat-message-submit').onclick = function(e) {
		var messageInputDom = document.querySelector('#chat-message-input');
		var message = messageInputDom.value;
		document.querySelector('#chat-log').value += ('Message sent: ');
		document.querySelector('#chat-log').value += (message + '\n');
		chatSocket.send(JSON.stringify({
			'message': message, 'recipient': 'chat_ble'
		}));

		messageInputDom.value = '';
	};

	document.querySelector('#button-handler').onclick = function (e) {

		var message = e.target.id;
		document.querySelector('#chat-log').value += ('Message sent: ');
		document.querySelector('#chat-log').value += (message + '\n');

		chatSocket.send(JSON.stringify({
			'message': message, 'recipient': 'chat_ble'
		}));
	};

});
