var led = document.getElementById('led');
var led_start = document.getElementById('led_start');
var led_colorshift = document.getElementById('led_colorshift');
var led_increaseBrightness = document.getElementById('led_increaseBrightness');
var led_decreaseBrightness = document.getElementById('led_decreaseBrightness');
var led_stop = document.getElementById('led_stop');
var socketio = io.connect(location.origin + '/client-user');

led_start.innerHTML = 'On'
led_start.onclick = function()  {
    socketio.emit('LED_ON', namespace='/client-user');
}

led_stop.innerHTML = 'Off'
led_stop.onclick = function()  {
    socketio.emit('LED_OFF', namespace='/client-user');
}

led_colorshift.innerHTML = 'Colorshift'
led_colorshift.onclick = function()  {
    socketio.emit('START_COLORSHIFT', namespace='/client-user');
}

led_increaseBrightness.innerHTML = 'Increase Brightness'
led_increaseBrightness.onclick = function()  {
    socketio.emit('INCREASE_BRIGHTNESS', namespace='/client-user');
}

led_decreaseBrightness.innerHTML = 'Decrease Brightness'
led_decreaseBrightness.onclick = function()  {
    socketio.emit('DECREASE_BRIGHTNESS', namespace='/client-user');
}

