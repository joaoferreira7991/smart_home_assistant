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
    socketio.emit('loadActuator');
    socketio.emit('loadData');
});

// Temperature related events
socketio.on('loadData', function(data)    {
    parsed = JSON.parse(data);
    //temp_value.innerHTML = 'Current temperature is ' + parsed.temp + 'ºC.';
    //hum_value.innerHTML = 'Current humidity is ' + parsed.hum + '%.';
    
    if(temp_chart != undefined)
        temp_chart.destroy();
    temp_chart = makeChart(temp_canvas, parse_chart(parsed.temp_arr), "Temperature", 0, 35);
    if(hum_chart != undefined)
        hum_chart.destroy();
    hum_chart = makeChart(hum_canvas, parse_chart(parsed.hum_arr), "Humidity", 0, 100);

});

socketio.on('loadActuator', function(data) {
    parsed = JSON.parse(data);
    loadButtons(parsed.actuator_arr, parsed.controller_arr);
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
function loadButtons(actuator_arr, controller_arr)  {
    for(var i=0; i<actuator_arr.length; i++)    {
                
        // <div class='led-switch>'
        var div = document.createElement('div');
        div.className = 'led-switch'+actuator_arr[i][0];

        // <div class='led-switch-onoff>'
        var div_switch = document.createElement('div');
        div_switch.className = 'led-switch-onoff';
        
        // <input id='switch-onoff{id}' type='checkbox'>
        var input = document.createElement('input');
        input.id = 'switch-onoff';
        input.type = 'checkbox';
        if(actuator_arr[i][2])  {
            input.checked = true;
        }

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
        label_switch.innerHTML = actuator_arr[i][1];

        // Construct div_name
        div_name.appendChild(label_switch);

        // Construct led-switch
        div.appendChild(div_switch);
        div.appendChild(div_name);
        
        // Finally append to led div
        led.appendChild(div);
    }

    for(var j=0; j<controller_arr.length; j++)  {

        // <div class='led-controller>'
        var div_controller = document.createElement('div');
        div_controller.className = 'led-controller';
        div_controller.id = 'led-controller'+controller_arr[j][0];

        // <div class='led-controller-onoff>'
        var div_onoff = document.createElement('div');
        div_onoff.className = 'led-led-controller-onoff';

        // <input id='onoff-toggle{id}' type='checkbox'>
        var input = document.createElement('input');
        input.id = 'onoff-toggle';
        input.type = 'checkbox';
        // controls state_current
        if(controller_arr[j][2])  {
            input.checked = true;
        }

        // <label for='onoff-toggle{id}' id='onoff-label'>
        var label_onoff = document.createElement('label');
        label_onoff.htmlFor = input.id;
        label_onoff.id = 'onoff-label';

        // <i id='onoff-icon' class='material-icons' >power_settings_new</i>
        var icon = document.createElement('i');
        icon.id = 'onoff-icon';
        icon.className = 'material-icons';
        icon.innerHTML = 'power_settings_new';

        // Construct div_onoff
        label_onoff.appendChild(icon);
        div_onoff.appendChild(input);
        div_onoff.appendChild(label_onoff);

        // <div class='led-controller-increase>'
        var div_increase = document.createElement('div');
        div_increase.className = 'led-controller-increase';
        
        var increase_button = document.createElement('button');
        var increase_icon = document.createElement('i');
        increase_icon.className = 'material-icons';
        increase_icon.innerHTML = 'add_circle_outline';

        increase_button.appendChild(increase_icon);
        div_increase.appendChild(increase_button);

        // <div class='led-controller-decrease>'
        var div_decrease = document.createElement('div');
        div_decrease.className = 'led-controller-decrease';
        
        var decrease_button = document.createElement('button');
        var decrease_icon = document.createElement('i');
        decrease_icon.className = 'material-icons';
        decrease_icon.innerHTML = 'remove_circle_outline';

        decrease_button.appendChild(decrease_icon);
        div_decrease.appendChild(decrease_button);        


        // <div class='led-controller-colorshift>'
        var div_colorshift = document.createElement('div');
        div_colorshift.className = 'led-controller-colorshift';        


        // <input id='colorshift-toggle{id}' type='checkbox'>
        var input = document.createElement('input');
        input.id = 'colorshift-toggle';
        input.type = 'checkbox';
        // controls state_colorshift
        if(controller_arr[j][3])  {
            input.checked = true;
        }

        // <label for='colorshift-toggle{id}' id='colorshift-label'>
        var label_colorshift = document.createElement('label');
        label_colorshift.htmlFor = input.id;
        label_colorshift.id = 'colorshift-label';
        //label_colorshift.innerHTML = controller_arr[j][1];
        label_colorshift.innerHTML = 'Colorshift';

        // Construct div_colorshift
        div_colorshift.appendChild(input);
        div_colorshift.appendChild(label_colorshift);

        // Construct led-controller
        div_controller.appendChild(div_onoff)
        div_controller.appendChild(div_increase)
        div_controller.appendChild(div_decrease)
        div_controller.appendChild(div_colorshift)

        // Finally append to led div
        led.appendChild(div_controller);
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