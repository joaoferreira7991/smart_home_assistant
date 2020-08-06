//var led = document.getElementById('led');
//var led_start = document.getElementById('led_start');
//var led_colorshift = document.getElementById('led_colorshift');
//var led_increaseBrightness = document.getElementById('led_increaseBrightness');
//var led_decreaseBrightness = document.getElementById('led_decreaseBrightness');
//var led_stop = document.getElementById('led_stop');
var socketio = io.connect('https://smart-home-assistant.herokuapp.com' + '/client-user');

// Color helper variable
var color = Chart.helpers.color;

// Variables from Dashboard 
var temp_value = document.getElementById('temp').children['temp_value'];
var hum_value = document.getElementById('hum').children['hum_value'];
var temp_canvas = document.getElementById('temp').children['temp_canvas'].getContext('2d');
var hum_canvas = document.getElementById('hum').children['hum_canvas'].getContext('2d');

// Load values
socketio.on('connect', function()    {
    socketio.emit('updateValues');
});

// Temperature related events
socketio.on('updateValues', function(data)    {
    parsed = JSON.parse(data);
    temp_value.innerHTML = parsed.temp;
    hum_value.innerHTML = parsed.hum;
    makeChart(temp_canvas, parse_data(parsed.temp_arr), "Temperature");
    makeChart(hum_canvas, parse_data(parsed.hum_arr), "Humidity");

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

// Takes the unprepared json data and transforms it into working chart.js data
function parse_data(data)   {
    var aux = [];
    for(var i=0; i<data.length; i++)    {
        var x = {x: new moment({y: data[i][1].year,
                                M: data[i][1].month, 
                                d: data[i][1].day,
                                h: data[i][1].hour, 
                                m: data[i][1].minute,
                                s: data[i][1].second}), 
                y: data[i][0]};
        aux.push(x);        
    }
    return aux;
};

function makeChart(ctx, arr, name)    {
    var data = {
        datasets: [{
            label: name,
            backgroundColor: 'rgba(7, 152, 255, 0.5)',
            showLine: true,
            data: arr
        }]
    };

    return new Chart.Scatter(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            scales: {
                xAxes:[{
                   type: 'time'
                }],
                yAxes:  [{
                }]
            }
        }
    });
};