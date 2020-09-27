---
title: "Promises in jQuery"
date: 2016-08-17
category:
- Tutorials
tags:
- JavaScript
- jQuery
---

In the recent lesson about AJAX we saw how to make a server request in the background (asynchronous), and then handling the server response in a function. If a second asynchronous server request depends on the first one, it becomes messy to manage the dependencies. For example, the second asynchronous server request can be initiated in the response handler function of the first server request. This leads to long chains of calls that can be hard to read and make sense of.

To make composition of multiple asynchronous requests more manageable, the concept of a Promise was introduced. A Promise basically represents an action with an eventual outcome. By representing this eventual outcome as a promise object, the interaction between multiple promise objects can easily be expressed even when their results are not yet available. The [Promises/A+ specification](https://promisesaplus.com) details the behavior and interface of promise objects. This way there is a standard interface for interacting with promises, independent of the actual promise-implementing library. 

jQuery provides the [Deferred Object](http://api.jquery.com/category/deferred-object/) which is a promise object. When making an AJAX call with jQuery's $.ajax method (or with one of the convenience methods like $.get), the returned object implements the promise interface, just like the Deferred object. This way, multiple jQuery AJAX call objects can be coordinated using the mechanisms provided by promises.

First, let's look at some other means of making asynchronous calls. The built-in JavaScript functions `setTimeout` and `setInterval` can be used to make delayed function calls.

# Delayed function execution

The JavaScript `setTimeout` function can be used to call a function in the future, by specifying the function to be called and the time (in milliseconds) to wait until the function gets called. Here's an example:

```javascript
    function sayHello() {
        alert('hello');
    }

    setTimeout(sayHello, 5000);
```

Here, the sayHello function will show an alert popup box with the text "hello", but only after 5 seconds.

The function `setInterval` will also call the function after the specified delay, but it will repeatedly call the function:

```javascript
    function sayHello() {
        alert('hello');
    }

    setInterval(sayHello, 5000);
```

Here, the sayHello function will be called every 5 seconds.
Note: when using `setTimeout` or `setInterval`, the queued function call can be canceled. To cancel the call, use the JavaScript built-in function `clearTimeout` which takes the timer ID returned by a previous call to `setTimeout` or `setInterval`.

For example, the following will start a recurring call to function logGreeting every second. After 8 seconds, it will stop and cancel the recurring function calls:

```javascript
    function logGreeting() {
        console.log('hello at ' + new Date());
    }

    var timerId = setInterval(logGreeting, 1000);

    setTimeout(function() {
        clearTimeout(timerId);
    }, 8000);
```

# jQuery done method

When making a jQuery AJAX call, the `done` method can be used to attach a response handling function, to be called when the AJAX call finishes successfully.
The jQuery AJAX call (e.g. methods $.ajax or $.get) returns an object that is referred to as "jqXHR". 
The `done` method can be called on the jqXHR object to attach a function that will handle the eventual server response, if the server request was successful. Similar to `done`, there's also a fail method to attach a failure handling function and an `always` method that will be executed regardless of whether the call was successful or unsuccessful.

Consider the following function that makes a call to the Open Weather API server:

```javascript
    var API_KEY = '05e394dfc3d1b822698f06d759bc4c95';
    var WEATHER_SERVICE_URL = 'http://api.openweathermap.org/data/2.5/weather';

    function fetchWeather(city, country) {
        var li = $('<li>Weather in ' + city.toUpperCase() + ': </li>');
        $('#weatherlist').append(li);
        var data = {
            q: city + ',' + country,
            APPID: API_KEY
        };
        return $.get(WEATHER_SERVICE_URL, data, function(result) {
            if (result.weather) {
                var weather = result.weather[0];
                var kelvin = result.main.temp;
                var fahrenheit = Math.round((kelvin - 273) * 1.8 + 32);
                $('<span class="desc">' + weather.description + '</span>').appendTo(li);
                $('<span class="temp">' + fahrenheit + ' F</span>').appendTo(li);
            }
        });
    }
```

This function first adds a new `<li>` tag to the parent page's `<ul>` list with the ID of "weatherlist". It makes a call to api.openweathermap.org for the specified city. When the request gets back the weather data, it adds the weather description and temperature.
Note that this function returns the jqXHR object returned by the jQuery AJAX function. In this case it calls the $.get helper function.

Here's a function that uses the jQuery `done` methods on the jqXHR object returned by the fetchWeather function:

```javascript
    fetchWeather('boston', 'usa')
        .done( function() { fetchWeather('lima', 'peru'); })
        .done( function() { fetchWeather('nashua', 'usa'); })
        .done( function() { fetchWeather('hannover', 'germany'); });
```

When looking at the network requests in the Chrome Inspector's Network tab, we see that the weather requests for lima, nashua and hannover happen after the first request for boston. 

![jQuery done](/extras/jquery-weather-done.png)

The last three requests basically start simultaneously. This is because the requests for lima, nashua and hannover are all attached as "`done`" handlers to the original boston request. The `done` method returns the original jqXHR object, allowing multiple method calls to be chained. That means the above is equivalent to doing the following:

```javascript
    var bostonRequest = fetchWeather('boston', 'usa');
    bostonRequest.done( function() { fetchWeather('lima', 'peru'); });
    bostonRequest.done( function() { fetchWeather('nashua', 'usa'); });
    bostonRequest.done( function() { fetchWeather('hannover', 'germany'); });
```

# jQuery Deferred object

In jQuery, the the [Deferred Object](http://api.jquery.com/category/deferred-object/) can be used to represent a Promise.

Promises represent an eventual outcome. There is therefore some state attached to the promise object. The three states for promises are: 

* pending: This is the initial state. There is no outcome yet
* fulfilled: The eventual value is available and the request is successful.
* rejected; The eventual value is available and the request is unsuccessful.

jQuery's $.ajax (and related) methods return a jqXHR function that implement the promise interface. In Many cases these "project objects" can be used as-is. 
If we need more control over a promise - like when the promise is fulfilled or rejected, and what the eventual value is - we can create a jQuery Deferred object to manage the promise.

Here's one example of using a jQuery Deferred object to fetch the weather slowly:

```javascript
    function fetchWeatherSlowly(city, country, prevCountry) {
        var promise = $.Deferred();
        var weatherRequest = fetchWeather(city, country, prevCountry);
        weatherRequest.done(function(apiJSON) {
            setTimeout(function() {
                if (apiJSON.weather) {
                    promise.resolve(apiJSON);
                }
                else {
                    promise.reject("Error received from API: " + apiJSON.message);
                }
            }, 2000);
        });
        return promise;
    }
```

The Deferred object (the promise) will resolve 2 seconds after the AJAX request from the fetchWeather call returns a response.

The Deferred/promise object gets resolved or rejected by calling the resolve or reject methods, respectively. Optionally, a value can be specified. In the above example, the fetchWeather AJAX call's JSON response gets passed through to the Deferred/project object when it resolves.

# Chaining promises together

There are cases when an AJAX call depends on a previous AJAX call's response. If multiple AJAX requests need to be "chained" together, one way is to initiate the second AJAX call in the first AJAX call's response handler function. When there are many calls in the chain, this quickly becomes hard to manage and reason about. Promise objects have a `then` method that can be used to chain together a sequence of promises. The `then` method takes two parameters. Both of these parameters are functions. The first function parameter is a success handler, which will be called if the promise resolved (completed successfully). The second function parameter is a failure handler, which will be called if the promise got rejected (completed unsuccessfully).

Here's an example that fetches the whether of a few cities, but sequentially (not in parallel):

```javascript
    fetchWeather('boston', 'usa')
        .then( function(bostonResponse) {
            console.log('got boston!', bostonResponse); 
            return fetchWeather('lynn', 'usa'); 
         })
        .then( function(lynnResponse) { 
            console.log('got lynn!', lynnResponse);
            // normally this function would fetch the weather for the city of Lima,
            // but we intentionally don't specify the city name to produce an error:
            return fetchWeather('', '');
         })
        .then(
            function(limaResponse) {
                console.log('got lima!', limaResponse);
                return fetchWeather('hannover', 'germany'); 
            },
            function(response) {
                console.log('could not load lima!');
                console.log('here is the response:', response);
                return fetchWeather('hannover', 'germany'); 
            }
        )
        .then( function(hannoverResponse) {
            console.log('got hannover!', hannoverResponse);
            return fetchWeather('canton', 'usa'); 
        });
```

In Chrome Inspector's network tab, we see that the requests run sequentially - one after the other:

![jQuery then](/extras/jquery-weather-then.png)

Note: we intentially inserted a failed network request in the second `then` function call, where it makes a request with an empty city value. The following `then` function handles the error when the second function parameter gets called. Note: without the second function parameter, the `then` function would not contain a new promise object. The chain of `then` calls will continue as long as the previous `then` call returns a new promise for the next `then` call to act on.

# Managing sets of promises

Sometimes we need to know when a set of promises have completed. jQuery's Deferred object interface provides a `when` method that can be used to attach a function whenever the specified set of promises resolves.

Here's an example that loads cities from three continents. As soon as all cities of a continent have loaded, a banner gets displayed on the page:

```javascript
    var amsterdam        = fetchWeather('amsterdam', 'netherlands');
    var athens           = fetchWeather('athens', 'greece');
    var barcelona        = fetchWeather('barcelona', 'spain');
    var berlin           = fetchWeather('berlin', 'de');
    var cairo            = fetchWeather('Cairo', 'egypt');
    var capetown         = fetchWeather('Capetown', 'south africa');
    var chicago          = fetchWeather('Chicago', 'usa');
    var dallas           = fetchWeather('Dallas', 'usa');
    var dublin           = fetchWeather('dublin', 'ireland');
    var edinburgh        = fetchWeather('edinburgh', 'scottland');
    var houston          = fetchWeather('Houston', 'usa');
    var johannesburg     = fetchWeather('johannesburg', 'za');
    var la               = fetchWeather('Los Angeles', 'usa');
    var london           = fetchWeather('london', 'gb');
    var milan            = fetchWeather('milan', 'italy');
    var montreal         = fetchWeather('Montreal', 'canada');
    var nairobi          = fetchWeather('milan', 'kenya');
    var nyc              = fetchWeather('New York', 'usa');
    var paris            = fetchWeather('paris', 'france');
    var philadelphia     = fetchWeather('Philadelphia', 'usa');
    var phoenix          = fetchWeather('Phoenix', 'usa');
    var rome             = fetchWeather('roma', 'italy');
    var sanantonio       = fetchWeather('San Antonio', 'usa');
    var sandiego         = fetchWeather('San Diego', 'usa');
    var sanjose          = fetchWeather('San Jose', 'usa');
    var toronto          = fetchWeather('Toronto', 'canada');
    var vancouver        = fetchWeather('Vancouver', 'canada');

    $.when(rome, paris, barcelona, london, amsterdam, dublin, athens, edinburgh, berlin, milan)
        .then(function() {
            $('#continents').append('<div>EUROPE loaded</div>');
        });

    $.when(nyc, la, chicago, houston, philadelphia, phoenix, sanantonio, sandiego, dallas, sanjose, toronto, montreal, vancouver)
        .then(function() {
            $('#continents').append('<div>NORTH AMERICA loaded</div>');
        });

    $.when(johannesburg, cairo, nairobi, capetown)
        .then(function() {
            $('#continents').append('<div>AFRICA loaded</div>');
        });
```

Here is a screenshot, showing loading of the requests and the banners that appear when each continent's group finished loading:

![jQuery when](/extras/jquery-weather-when.gif)
docker build . -t ds.innernet.io:5002/innernet-blog:2
docker push ds.innernet.io:5002/innernet-blog:2

