//var led = document.getElementById('led');
var led_start = document.getElementById('led_start');
var led_colorshift = document.getElementById('led_colorshift');
var led_increaseBrightness = document.getElementById('led_increaseBrightness');
var led_decreaseBrightness = document.getElementById('led_decreaseBrightness');
var led_stop = document.getElementById('led_stop');
var socketio = io.connect('http://smart-home-assistant.herokuapp.com' + '/client-user');


led_start.addEventListener("click", function()  {
    socketio.emit('LED_ON');
    alert('On');
});

led_stop.addEventListener("click", function()  {
    socketio.emit('LED_OFF');
    alert('Off');
});

led_colorshift.addEventListener("click", function()  {
    socketio.emit('START_COLORSHIFT');
    alert('Colorshift');
});

led_increaseBrightness.addEventListener("click", function()  {
    socketio.emit('INCREASE_BRIGHTNESS');
    alert('Increase');
});

led_decreaseBrightness.addEventListener("click", function()  {
    socketio.emit('DECREASE_BRIGHTNESS');
    alert('Decrease');
});