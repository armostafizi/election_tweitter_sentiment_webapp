
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var data_received = [];
    //receive details from server
    socket.on('newdata', function(msg) {
	console.log("Received Data: " + msg.txt);
        //maintain the last 10 entities
        if (data_received.length >= 10){
            data_received.shift()
        }            
        data_received.push(msg.txt);
        data_string = '';
        for (var i = 0; i < data_received.length; i++){
            data_string = data_string + '<p>' + data_received[i] + '</p>';
        }
        $('#log').html(data_string);
    });

});
