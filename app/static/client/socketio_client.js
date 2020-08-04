//var led = document.getElementById('led');
//var led_start = document.getElementById('led_start');
//var led_colorshift = document.getElementById('led_colorshift');
//var led_increaseBrightness = document.getElementById('led_increaseBrightness');
//var led_decreaseBrightness = document.getElementById('led_decreaseBrightness');
//var led_stop = document.getElementById('led_stop');
var socketio = io.connect('https://smart-home-assistant.herokuapp.com' + '/client-user');

// Variables from Dashboard 
var temp_value = document.getElementById('temp').children['temp_value'];
var hum_value = document.getElementById('hum').children['hum_value'];

// Load values
socketio.on('connect', function()    {
    socketio.emit('updateValues');
});

// Temperature related events
socketio.on('updateValues', function(data)    {
    temp_value.innerHTML = data.temp;
    hum_value.innerHTML = data.hum;
});

// Led Controller events
/*
led_start.addEventListener("click", function()  {
    socketio.emit('LED_ON');
});

led_stop.addEventListener("click", function()  {
    socketio.emit('LED_OFF');
});

led_colorshift.addEventListener("click", function()  {
    socketio.emit('START_COLORSHIFT');
});

led_increaseBrightness.addEventListener("click", function()  {
    socketio.emit('INCREASE_BRIGHTNESS');
});

led_decreaseBrightness.addEventListener("click", function()  {
    socketio.emit('DECREASE_BRIGHTNESS');
});
*/