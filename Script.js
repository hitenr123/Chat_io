
var socket = io();

function sendMessage() {
    let input = document.getElementById("message");
    socket.send(input.value);
    input.value = "";
}

socket.on("message", function(msg) {
    let div = document.createElement("div");
    div.classList.add("msg");
    div.innerText = msg;

    document.getElementById("messages").appendChild(div);
});