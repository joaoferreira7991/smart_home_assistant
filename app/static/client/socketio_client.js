var socketio = io.connect('https://smart-home-assistant.herokuapp.com' + '/client-user');

// Color helper variable
var color = Chart.helpers.color;

// Chart variable declaration to make possible to destroy when reloaded
var temp_chart;
var hum_chart;

// Variables to control led strip
var led_onoff_toggle = document.getElementById('led').children['led_onoff'].children['led_onoff_toggle'];
var led_increaseBrightness = document.getElementById('led').children['led_increaseBrightness'];
var led_decreaseBrightness = document.getElementById('led').children['led_decreaseBrightness'];
var led_colorshift_toggle = document.getElementById('led').children['led_colorshift_toggle'];

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
    temp_value.innerHTML = 'Current temperature is ' + parsed.temp + 'ºC.';
    hum_value.innerHTML = 'Current humidity is ' + parsed.hum + '%.';
    if(temp_chart != undefined)
        temp_chart.destroy();
    temp_chart = makeChart(temp_canvas, parse_data(parsed.temp_arr), "Temperature", 0, 35);
    if(hum_chart != undefined)
        hum_chart.destroy();
    hum_chart = makeChart(hum_canvas, parse_data(parsed.hum_arr), "Humidity", 0, 100);

});

// Led Controller events

led_onoff_toggle.addEventListener("change", function()  {
    if(led_onoff_toggle.checked)
        socketio.emit('LED_ON');    
    if(!led_onoff_toggle.checked)
        socketio.emit('LED_OFF');
});

led_colorshift_toggle.addEventListener("change", function()  {
    if(led_colorshift_toggle.checked)
        socketio.emit('START_COLORSHIFT');   
    if(!led_colorshift_toggle.checked)
        socketio.emit('STOP_COLORSHIFT'); 
});

led_increaseBrightness.addEventListener("click", function()  {
    socketio.emit('INCREASE_BRIGHTNESS');
});

led_decreaseBrightness.addEventListener("click", function()  {
    socketio.emit('DECREASE_BRIGHTNESS');
});


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

function makeChart(ctx, arr, name, min, max)    {
    var data = {
        datasets: [{
            label: name,
            backgroundColor: 'rgba(7, 152, 255, 0.5)',
            showLine: true,
            data: arr,
            min: Math.min.apply(this, arr[0]),
            max: Math.max.apply(this, arr[0])
        }]
    };

    var chart = new Chart.Scatter(ctx, {
        type: 'line',
        data: data,
        options: {
            lineTension: 1,
            responsive: true,
            scales: {
                xAxes:[{
                   type: 'time',
                   ticks:   {
                       //min: min,
                       //max: max
                   }
                }],
                yAxes:  [{
                    ticks:   {
                        min: min,
                        max: max
                    }
                }]
            }
        }
    });
    return chart;
};