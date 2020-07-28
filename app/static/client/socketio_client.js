var led = document.getElementById('led');
var led_start = document.getElementById('led_start');
var led_colorshift = document.getElementById('led_colorshift');
var led_increaseBrightness = document.getElementById('led_increaseBrightness');
var led_decreaseBrightness = document.getElementById('led_decreaseBrightness');
var led_stop = document.getElementById('led_stop');
var socketio = io.connect(location.origin + '/client-user');

led_start.innerHTML = 'On'
led_start.addEventListener("click", function()  {
    socketio.emit('LED_ON');
    alert('ARRRHG')
});

led_stop.innerHTML = 'Off'
led_stop.onclick = function()  {
    socketio.emit('LED_OFF');
}

led_colorshift.innerHTML = 'Colorshift'
led_colorshift.onclick = function()  {
    socketio.emit('START_COLORSHIFT');
}

led_increaseBrightness.innerHTML = 'Increase_Brightness'
led_increaseBrightness.onclick = function()  {
    socketio.emit('INCREASE_BRIGHTNESS');
}

led_decreaseBrightness.innerHTML = 'Decrease_Brightness'
led_decreaseBrightness.onclick = function()  {
    socketio.emit('DECREASE_BRIGHTNESS');
}

