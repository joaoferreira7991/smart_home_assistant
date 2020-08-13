var socketio = io.connect('https://smart-home-assistant.herokuapp.com' + '/client-user');

// Color helper variable
var color = Chart.helpers.color;

// Chart variable declaration to make possible to destroy when reloaded
var temp_chart;
var hum_chart;

// Variables to control led strip
var led = document.getElementById('led');
var led_onoff_toggle = document.getElementById('onoff-toggle');
var led_increaseBrightness = document.getElementById('increase-brightness');
var led_decreaseBrightness = document.getElementById('decrease-brightness');
var led_colorshift_toggle = document.getElementById('colorshift-toggle');

// Variables from Dashboard 
var temp_canvas = document.getElementById('temp-canvas').getContext('2d');
//var hum_value = document.getElementById('charts').children['hum_value'];
var hum_canvas = document.getElementById('hum-canvas').getContext('2d');
//var hum_canvas = document.getElementById('hum').children['hum_canvas'].getContext('2d');

// On connection asks the server for the required data
socketio.on('connect', function()    {
    socketio.emit('loadData');
});

// Temperature related events
socketio.on('loadData', function(data)    {
    parsed = JSON.parse(data);
    //temp_value.innerHTML = 'Current temperature is ' + parsed.temp + 'ºC.';
    //hum_value.innerHTML = 'Current humidity is ' + parsed.hum + '%.';
    
    loadButtons(parsed.actuator_arr);

    if(temp_chart != undefined)
        temp_chart.destroy();
    temp_chart = makeChart(temp_canvas, parse_chart(parsed.temp_arr), "Temperature", 0, 35);
    if(hum_chart != undefined)
        hum_chart.destroy();
    hum_chart = makeChart(hum_canvas, parse_chart(parsed.hum_arr), "Humidity", 0, 100);

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

// Function to load buttons per actuator received
function loadButtons(data)  {
    for(var i=0; i<data.length; i++)    {
                
        // <div class='led-switch-onoff>'
        var div_switch = document.createElement('div');
        div_switch.className = 'led-switch-onoff';
        
        // <input id='switch-onoff{id}' type='checkbox'>
        var input = document.createElement('input');
        input.id = 'switch-onoff'+data[i][0];
        input.type = 'checkbox';
        
        // <label for='switch-onoff{id}' id='switch-onoff-label'>
        var label_switch = document.createElement('label');
        label_switch.htmlFor = input.id;
        label_switch.id = 'switch-onoff-label';

        // <i id='switch-onoff-icon' class='material-icons' >power_settings_new</i>
        var icon = document.createElement('i');
        icon.id = 'switch-onoff-icon';
        icon.className = 'material-icons';
        icon.innerHTML = 'power_settings_new';

        // Construct div_switch
        label_switch.appendChild(icon);
        div_switch.appendChild(input);
        div_switch.appendChild(label_switch);

        // <div class='led-switch-name>'
        var div_name = document.createElement('div');
        div_name.className = 'led-switch-name';

        // <label>
        var label_switch = document.createElement('label');
        label_switch.innerHTML = data[i][1];

        // Construct div_name
        div_name.appendChild(label_switch);

        // <div class='led-switch>'
        var div = document.createElement('div');
        div.className = 'led-switch';

        // Construct led_switch
        div.appendChild(div_switch);
        div.appendChild(div_name);
        
        // Finally append to led div
        led.appendChild(div);
    }
};

// Takes the unprepared json data and transforms it into working chart.js data
function parse_chart(data)   {
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
            maintainAspectRatio: true,
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