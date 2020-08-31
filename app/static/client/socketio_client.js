var socketio = io.connect('https://smart-home-assistant.herokuapp.com' + '/client-user');

// Color helper variable
var color = Chart.helpers.color;

// Chart variable declaration to make possible to destroy when reloaded
var temp_chart;
var hum_chart;

// Variables to control led strip
var led = document.getElementById('led');

// Canvas variables
var temp_canvas = document.getElementById('temp-canvas').getContext('2d');
var hum_canvas = document.getElementById('hum-canvas').getContext('2d');

// Receives event to load temperatur and humidity data
socketio.on('loadData', function(data)    {
    parsed = JSON.parse(data);
    var latest_temp = document.getElementById('latest_temp');
    latest_temp.innerHTML = 'Current temperature: ' + parsed.latest_temp + 'ºC';
    var latest_hum = document.getElementById('latest_hum');
    latest_hum.innerHTML = 'Current humidity: ' + parsed.latest_hum + '%';
    
    if(temp_chart != undefined)
        temp_chart.destroy();
    temp_chart = makeChart(temp_canvas, parse_chart(parsed.temp_arr), "Temperature", 0, 35);
    if(hum_chart != undefined)
        hum_chart.destroy();
    hum_chart = makeChart(hum_canvas, parse_chart(parsed.hum_arr), "Humidity", 0, 100);

});

// Receives event to load actuator data
socketio.on('loadActuator', function(data) {
    parsed = JSON.parse(data);
    loadButtons(parsed.actuator_arr, parsed.controller_arr);
});

// Update state event
socketio.on('updateState', function(data)   {
    if(data['class'] == 'switch-onoff') {
        var button = document.getElementById('switch-onoff'+data['id']);
        if(data['state'])   {
            button.style.color = 'rgb(3, 118, 254)';
        }
        else if(!data['state']) {
            button.style.color = 'black';
        }
    }
    else if(data['class'] == 'controller-onoff') {
        var button = document.getElementById('controller-onoff'+data['id']);
        var button_colorshift = document.getElementById('controller-colorshift'+data['id']);
        if(data['state'])   {
            button.style.color = 'rgb(3, 118, 254)';
            if(data['state_colorshift'])
                button_colorshift.style.color = 'rgb(239, 206, 106)';            
        }
        else if(!data['state']) {
            button.style.color = 'black';
            button_colorshift.style.color = 'black';
        }
    }
    else if(data['class'] == 'controller-colorshift') {
        var button = document.getElementById('controller-colorshift'+data['id']);
        if(data['state'])   {
            button.style.color = 'rgb(239, 206, 106)';
        }
        else if(!data['state']) {
            button.style.color = 'black';
        }
    }
});

socketio.on('deleteActuator', function(data) {
    var remove = document.getElementById('led-switch'+data['id']);
    led.removeChild(remove);
});

socketio.on('deleteController', function(data) {
    var remove = document.getElementById('led-controller'+data['id']);
    led.removeChild(remove);
});


// Forms Events
$('form#actuatorform').submit(function(event)    {
    event.preventDefault();
    data =  {
        'type'  : 'actuator',
        'csrf_token'    : $('#csrfActuator').val(),
        'name'  : $('#nameActuator').val(),
        'ip'    : $('#ipActuator').val()
    }
    socketio.emit('submitForm', data=data, function(data)   {
        parsed = JSON.parse(data);
        if(parsed['OK'] == 0) {
            alert(parsed['errors']);
        }
    });
});

$('form#controllerform').submit(function(event)    {
    event.preventDefault();
    data =  {
        'type'  : 'controller',
        'csrf_token'    : $('#csrfController').val(),        
        'name'  : $('#nameController').val(),
        'red'   : $('#redController').val(),
        'green' : $('#greenController').val(),
        'blue'  : $('#blueController').val()
    }
    socketio.emit('submitForm', data=data, function(data)   {
        parsed = JSON.parse(data);
        if(parsed['OK'] == 0) {
            alert(parsed['errors']);
        }
    });
});

// Event Listener
document.addEventListener('click', function(e)  {

    // Led Switch Events
    if(e.target && e.target.classList.contains('switch-onoff')) {
        var id = e.target.id.match(/\d+/).join('');
        data = {'id' : id}
        socketio.emit('switchClick', data=data);
    }
    else if(e.target && e.target.classList.contains('switch-del-button'))   {
        var id = e.target.id.match(/\d+/).join('');
        data = {'id' : id}
        socketio.emit('switchDel', data=data);
    }

    // Led Controller Events
    else if(e.target && e.target.classList.contains('controller-onoff'))   {
        var id = e.target.id.match(/\d+/).join('');
        data = {'id' : id}
        socketio.emit('ledClick', data=data);
    }    
    else if(e.target && e.target.classList.contains('controller-increase'))   {
        var id = e.target.id.match(/\d+/).join('');
        data = {'id' : id}
        socketio.emit('increaseBrightness', data=data);  
    }   
    else if(e.target && e.target.classList.contains('controller-decrease'))   {
        var id = e.target.id.match(/\d+/).join('');
        data = {'id' : id}
        socketio.emit('decreaseBrightness', data=data);   
    }    
    else if(e.target && e.target.classList.contains('controller-colorshift'))   {
        var id = e.target.id.match(/\d+/).join('');
        data = {'id' : id}
        socketio.emit('colorshiftClick', data=data);
    }
    else if(e.target && e.target.classList.contains('controller-del-button'))   {
        var id = e.target.id.match(/\d+/).join('');
        data = {'id' : id}
        socketio.emit('controllerDel', data=data);
    }

    // Form toggle buttons
    else if(e.target && e.target.id == 'button_addActuator')    {
        var x = document.getElementById('addActuator');
        if(x.style.display == '')
            x.style.display = 'block';
        else if(x.style.display == 'block')
            x.style.display = '';
    }    
    else if(e.target && e.target.id == 'button_addController')    {
        var x = document.getElementById('addController');
        if(x.style.display == '')
            x.style.display = 'block';
        else if(x.style.display == 'block')
            x.style.display = '';        
    }
});

// Function to load buttons per information received by the arrays
function loadButtons(actuator_arr, controller_arr)  {
    for(var i=0; i<actuator_arr.length; i++)    {
        
        if(document.getElementById('switch-onoff'+actuator_arr[i]['id']))
            continue;
        
        // <div class='led-switch>'
        var div = document.createElement('div');
        div.className = 'led-switch'; 
        div.id = 'led-switch'+actuator_arr[i]['id'];

        // <div class='led-switch-onoff>'
        var div_switch = document.createElement('div');
        div_switch.className = 'led-switch-onoff';
        
        // <button>
        var button = document.createElement('button');
        button.className = 'switch-onoff material-icons';
        button.id = 'switch-onoff'+actuator_arr[i]['id'];
        button.innerHTML = 'power_settings_new';
        /* Color it according to state */
        if(actuator_arr[i]['state'])  {
            button.style.color = 'rgb(3, 118, 254)';
        }
        else if(!actuator_arr[i]['state'])    {
            button.style.color = 'black';
        }

        // Construct div_switch
        div_switch.appendChild(button);

        // <div class='led-switch-name>'
        var div_name = document.createElement('div');
        div_name.className = 'led-switch-name';

        // <label>
        var label_switch = document.createElement('label');
        label_switch.innerHTML = actuator_arr[i]['name'];

        // Construct div_name
        div_name.appendChild(label_switch);

        // <div class='led-switch-del'
        var div_del = document.createElement('div');
        div_del.className = 'led-switch-del';

        // <button class='del-button>
        var del_button = document.createElement('button');
        del_button.className = 'switch-del-button';
        del_button.id = 'del-button'+actuator_arr[i]['id'];
        del_button.innerHTML = 'X';

        // Construct led-switch-del
        div_del.appendChild(del_button);

        // Construct led-switch
        div.appendChild(div_del);
        div.appendChild(div_switch);
        div.appendChild(div_name);
        
        // Finally append to led div
        led.appendChild(div);
    }

    for(var j=0; j<controller_arr.length; j++)  {

        if(document.getElementById('controller-onoff'+controller_arr[j]['id']))
            continue;

        // <div class='led-controller>'
        var div_controller = document.createElement('div');
        div_controller.className = 'led-controller';
        div_controller.id = 'led-controller'+controller_arr[j]['id'];

        // <div class='led-controller-onoff>'
        var div_onoff = document.createElement('div');
        div_onoff.className = 'led-controller-onoff';

        // <button id='onoff-toggle{id}' type='checkbox'>
        var button_onoff = document.createElement('button');
        button_onoff.className = 'controller-onoff material-icons';
        button_onoff.id = 'controller-onoff'+controller_arr[j]['id'];
        button_onoff.innerHTML = 'power_settings_new';
        /* Color it according to state */
        if(controller_arr[j]['state'])  {
            button_onoff.style.color = 'rgb(3, 118, 254)';
        }
        else if(!controller_arr[j]['state'])    {
            button_onoff.style.color = 'black';
        }

        // Construct div_onoff
        div_onoff.appendChild(button_onoff);

        // <div class='led-controller-increase>'
        var div_increase = document.createElement('div');
        div_increase.className = 'led-controller-increase';
        
        var increase_button = document.createElement('button');
        increase_button.className = 'controller-increase material-icons';
        increase_button.id = 'controller-increase'+controller_arr[j]['id'];
        increase_button.innerHTML = 'add_circle_outline';

        // Construct div_increase
        div_increase.appendChild(increase_button);
        
        // <div class='led-controller-decrease>'
        var div_decrease = document.createElement('div');
        div_decrease.className = 'led-controller-decrease';
        
        var decrease_button = document.createElement('button');
        decrease_button.className = 'controller-decrease material-icons';
        decrease_button.id = 'controller-decrease'+controller_arr[j]['id'];
        decrease_button.innerHTML = 'remove_circle_outline';

        // Construct div_increase
        div_decrease.appendChild(decrease_button);      


        // <div class='led-controller-colorshift>'
        var div_colorshift = document.createElement('div');
        div_colorshift.className = 'led-controller-colorshift';

        // <button>
        var button_colorshift = document.createElement('button');
        button_colorshift.className = 'controller-colorshift';
        button_colorshift.id = 'controller-colorshift'+controller_arr[j]['id'];
        button_colorshift.innerHTML = 'Colorshift';
        /* Color it according to state_colorshift if state is true */
        if(controller_arr[j]['state'])  {
            if(controller_arr[j]['state_colorshift'])  {
                button_colorshift.style.color = 'rgb(239, 206, 106)';
            }
            else if(!controller_arr[j]['state_colorshift'])    {
                button_colorshift.style.color = 'black';
            }
        }

        // Contruct div_colorshift
        div_colorshift.appendChild(button_colorshift);

        // <div class='led-controller-del'
        var div_del = document.createElement('div');
        div_del.className = 'led-controller-del';

        // <button class='controller-del-button>
        var del_button = document.createElement('button');
        del_button.className = 'controller-del-button';
        del_button.id = 'del-button'+controller_arr[j]['id'];
        del_button.innerHTML = 'X';

        // Construct led-controller-del
        div_del.appendChild(del_button);

        // Construct led-controller
        div_controller.appendChild(div_del);
        div_controller.appendChild(div_onoff);
        div_controller.appendChild(div_increase);
        div_controller.appendChild(div_decrease);
        div_controller.appendChild(div_colorshift);

        // Finally append to led div
        led.appendChild(div_controller);
    }
};

// Takes the unprepared json data and transforms it into working chart.js data
function parse_chart(data)   {
    var aux = [];
    for(var i=0; i<data.length; i++)    {
        var x = {
            x: new moment({
                y: data[i][1].year,
                M: data[i][1].month-1, 
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
            pointBackgroundColor: 'rgba(239, 206, 106, 1.0)',
            pointBorderColor: 'rgba(242, 212, 122, 0.7)',
            backgroundColor: 'rgba(141, 123, 68, 0.5)',
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
            maintainAspectRatio: false,
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