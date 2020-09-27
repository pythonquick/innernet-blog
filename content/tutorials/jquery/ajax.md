---
title: "AJAX calls"
date: 2016-07-27
category:
- Tutorials
tags:
- JavaScript
- jQuery
---


AJAX stands for asynchronous JavaScript and and XML. This allows a single page in the browser to make requests to the server without reloading the entire page.
Browsers implement the XMLHttpRequest object that can make these server requests in the background. This object and AJAX calls in general is often referred to as XHR.
In this lesson we'll work with the jQuery ajax method, which uses the browser's XMLHttpRequest object. The XMLHttpRequest object can be used directly, but jQuery adds a few convenient options, and also takes care of any differences between the XMLHttpRequest objects on different types of browsers.

# Simple call

jQuery provides the method `$.ajax` to initiate an AJAX call. The first parameter is the URL.

Here is a simple call using $.ajax and a URL. No other parameters and options used:

    :::JavaScript
    $.ajax("https://innernet.io/extras/boston.json");

# Specify a callback - the old way

We can specify a callback function - a function that will be called once we eventually get some results back from the AJAX call. For this we'll use the second parameter of the $.ajax method which is an object with options.

Three of these options are callback functions:

* success: the function that will be called once the AJAX is successful. The success function will get passed a parameter with the response that came back from the server request
* error: the function that will be called if the AJAX call was unsuccessful, for example, if the URL was invalid or the server returned an error response, like HTTP response code 500. This method will get three parameters passed:
    * the jqXHR object, which is the object representing the ajax call. This is the object returned by the call to $.ajax
    * textStatus: a string representing the status. This will typically be the string "error"
    * errorThrown: a string that represents the type of error. For example, "File not found"
* complete: the function that will be called once the AJAX call is complete, whether it completed with success or with error

NOTE: these callback functions are deprecated, but they still work. It is recommended to use the new "promise interface" and the done, fail and always methods. See one of the next sections: "Promise Interface"

Here is a sample of an AJAX call that uses the three callbacks:

    :::JavaScript
    function handleSuccess(data) { alert('handleSuccess'); }
    function handleError(jqXHR, textStatus, errorThrown) { alert('handleError ' + textStatus + ' ' + errorThrown); }
    function handleComplete() {  alert('handleComplete'); }

    var url = 'https://innernet.io/extras/boston.json'
    var settings = {
        success: handleSuccess,
        error: handleError,
        complete: handleComplete
    };
    $.ajax(url, settings);

# More AJAX call options

The previous section used the second parameter of $.ajax: the settings object, where it used the success, error and complete options.
There are many more options that can be set. For a complete list, see the $.ajax method documentation at [http://api.jquery.com/jQuery.ajax/](http://api.jquery.com/jQuery.ajax/)

The sections below deal with a few common options: method, data, dataType and headers.

## The method option

By default, the HTTP method GET will be used. To use a different HTTP method, use the `method` option. For example, to make a POST request to the same URL, do this:

    :::JavaScript
    var url = 'https://innernet.io/extras/boston.json'
    var settings = {
        method: "POST"
    };
    $.ajax(url, settings);

Note: doing a POST to the [https://innernet.io/extras/boston.json](https://innernet.io/extras/boston.json) URL will not be supported. This is just to illustrate how to use a different HTTP method.

## The data option

To add a collection of name-value parameters (also referred to as query parameters) to the URL, the parameters and values can be specified in an object for the "data" option. Here's an example that adds four query parameters to the URL:

    :::JavaScript
    var url = 'https://innernet.io/extras/boston.json'
    var settings = {
        data: {
            FTYPE: 'R',
            INKEY: 'abef692a32',
            INIT: 'Y',
            KPRODUCTID: 234
        }
    };
    $.ajax(url, settings);


## The dataType option

When specifying a success callback, the first parameter to the callback function will be the result of the server response. jQuery will try to infer the type of data. For example, if the URL ends with .json or if the HTTP response header specifies that the type of data is in JSON format, jQuery will attempt to parse the server response as JSON and provide a JSON object as a parameter. In the case of the URL to [https://innernet.io/extras/boston.json](/extras/boston.json), the success method will get back a big text string.
To tell jQuery that the response content is JSON, set the dataType option to "JSON":

    :::JavaScript
    var url = 'https://innernet.io/extras/boston.json'
    var settings = {
            dataType: 'json',
            success: function(data) {
                console.log(data.name);
            }
    };
    $.ajax(url, settings);

The success function's data parameter will now be an object that represents the JSON output - not a string. That means, we can now access the attributes of the object - in this case the name attribute.

## The headers option

To send certain HTTP request headers to the server, use the headers option. The value of this option is an object. Each property/key of the object is the name of the HTTP request header and the value of of the property is the value of the HTTP request header.

Here's an example of how to call the URL with the HTTP request header "Cache-Control" set to "max-age=1000":

    :::JavaScript
    var url = 'https://innernet.io/extras/boston.json';
    var settings = {
        headers: {
            'Cache-Control': 'max-age=1000'
        }
    };
    $.ajax(url, settings);

# Promise interface

A promise object represents an eventual outcome. The $.ajax method returns a jqXML object. This jqXML object implement's jQuery's promise interface. That means, once we have a reference to the jqXML object, we can attach functions that will be run eventually as the AJAX call completes.

The three common function hooks that can be attached are:

* done: a function that will run when the AJAX call completes successfully
* fail: a function that will run when the AJAX call completes with an error
* always: a function that will run when the AJAX call completes, regardless of success or error

These three types of "hooks" work like the success, error and complete functions of the $.ajax method's settings parameter (the second parameter, after the URL).

There is a difference however. By using the done, fail and always hooks one gets more flexibility. For example:

* these hooks can be attached at a later stage, as long as there's a reference to the jqXML object. With the success/error/complete functions however, they need to be attached at the time when the $.ajax call is made.
* one can attach more than one type of these hooks. For example, one can add 2 or more "done" functions. They will all get triggered (run) when the AJAX call completes successfully

Note: the done, fail and always methods are methods of the jqXML object and each of them return the jqXML object itself. That means, it's possible to "chain" the method calls.

Here's an example that reuses the previously defined functions: handleSuccess, handleError and handleComplete:

    :::JavaScript
    var jqXHR = $.ajax('https://innernet.io/extras/boston.json');

    jqXHR
        .done(handleSuccess)
        .fail(handleError)
        .always(handleComplete)
        .done(function(data) {
            console.log('we are done');
        });

# The post and get helper

There are a couple of helper methods that in turn use the $.ajax method but provide a simple call interface using several default options.

One of these is the $.post method. It takes the URL as the first parameter, just as with $.ajax. It uses the HTTP method "POST" and takes a success callback function as a subsequent parameter.

The following makes a POST request to the specified URL and logs the resulting response text to the console:

    :::JavaScript
    $.post('https://innernet.io/extras/boston.json', function(data) {
        console.log(data); 
    });

The $.get method works similar but it uses the HTTP GET method.

Note, the $.ajax method also uses HTTP GET method by default, but the $.get method is handy because it's easy to attach a success/done handler function by simply providing it as a second parameter to the call of $.get

# The getJSON helper

When the response from the server is a text string but it represents JSON data, one needs to first parse the text to a JavaScript object before that object can be queried. Here's an example that first gets the text data from the server, parses it and then alerts the weather condition:

    :::JavaScript
    $.get('https://innernet.io/extras/boston.json', function(data) {
        var jsonObject = $.parseJSON(data);
        alert(jsonObject.weather[0].description); 
    });

If we know already that the output will be in JSON format, the dataType option can be used to specify that the expected content type is JSON. In that case, the success / done function will get a parameter of type Object, instead of type String:

    :::JavaScript
    $.ajax('https://innernet.io/extras/boston.json', {
        dataType: 'json',
        success: function(data) {
            alert(data.weather[0].description); 
        }
    });

The $.getJSON method simplifies this. It sets the dataType to 'json' and takes the success function as the second parameter:

    :::JavaScript
    $.getJSON('https://innernet.io/extras/boston.json', function(data) {
        alert(data.weather[0].description); 
    });
