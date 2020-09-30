const socket = io('http://localhost:8080')

function connectHandler() {
    console.log('Я успешно зацепился!');

    socket.emit('someEvent', { some: 'Value', testers: 'programmers' });
}

function someAnswerHandler(data) {
    console.log(data);

}

function messageHandler(data) {
    const { userName, message } = data;
    document.getElementById('chat').innerHTML += `<b>${userName ? userName : 'НоуНейм'}</b>: ${message}<br>`;
}

function joinToRoomHandler(data) {
    console.log('вошел', data);
    if (data) {
        document.getElementById('chat').innerHTML = '';
    }
}

function leaveRoomHandler(data) {
    console.log('вышел', data);
    if (data) {
        document.getElementById('chat').innerHTML = '';
    }
}

function getRoomMessagesHandler(data) {
    console.log(data);
    if (data && data.length) {
        data.forEach(mes => {
            const { userName, message } = mes;
            document.getElementById('chat').innerHTML += `<b>${userName ? userName : 'НоуНейм'}</b>: ${message}<br>`;
        });
    }
}

document.getElementById('sendMessage').onclick = function() {
    const userName = document.getElementById('userName').value;
    const message = document.getElementById('message').value;
    const roomName = document.getElementById('roomName').value;
    if (message) {
        socket.emit('message', { userName, roomName, message });
    }
};

document.getElementById('joinToRoom').onclick = function() {
    const roomName = document.getElementById('roomName').value;
    if (roomName) {
        socket.emit('joinToRoom', { roomName });
    }
};

document.getElementById('leaveRoom').onclick = function() {
    const roomName = document.getElementById('roomName').value;
    if (roomName) {
        socket.emit('leaveRoom', { roomName });
    }
};

socket.on('getRoomMessages', getRoomMessagesHandler);
socket.on('joinToRoom', joinToRoomHandler);
socket.on('leaveRoom', leaveRoomHandler);
socket.on('message', messageHandler);
socket.on('someAnswer', someAnswerHandler)
socket.on('connect', connectHandler)
