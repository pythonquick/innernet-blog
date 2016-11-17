Title: Objects Revisited
Date: 2016-02-04
Category: Tutorials
Tags: JavaScript, ES5


This section serves as a review of Objects in JavaScript, and visualizing their structure.

At their core, JavaScript objects are very simple. They are basically a container that hold zero or more key-value pairs.

The simplest object is this one:

    :::JavaScript
    var serverInfo = {};

Here the variable named serverInfo contains an object value. The object exists but is empty - it contains no values.

Below is an object that we use in the Project Planner's ProjPlanning.js file. It contains several "constant" values that are used in other places of the JavaScript file:

    :::JavaScript
    var CONST = {
        DEFAULT_CADENCE_THRESHOLD: 20,
        ZERO_PLACEHOLDER: "-",
        TABLE_DATE_DIALOG_HEIGHT: 440,
        MAX_PERIOD_SPAN: 17,
        PERIOD_TYPE: {
            MONTHLY: "30",
            WEEKLY: "40",
            SUMMARY: "10"
        },
        EXPORTCOL_SHOW: "0",
        EXPORTCOL_HIDE: "1"
    };

This object has 7 only key-value pairs. We can say it has seven attributes, or keys:

* DEFAULT_CADENCE_THRESHOLD
* ZERO_PLACEHOLDER
* TABLE_DATE_DIALOG_HEIGHT
* MAX_PERIOD_SPAN
* PERIOD_TYPE
* EXPORTCOL_SHOW
* EXPORTCOL_HIDE

The values for each of these keys are mostly strings or integers. One of the values (attribute PERIOD_TYPE) is an object. So we have a nested object. All attributes (keys) of objects are strings, but the values can be any type (even null). 

Here is a tabular representation of the above CONST object:

![Object tabular structure]({filename}/extras/object-structure-tabular.png)

Using the string name of the attribute, we can access the corresponding value. 

For example, the following alert will display 17

    :::JavaScript
    alert(CONST["MAX_PERIOD_SPAN"]);

The following alert will display 1

    :::JavaScript
    var setting = "EXPORTCOL_HIDE";
    alert(CONST[setting]);

If the name of the property is known, it can be used directly (without the square brackets []), using dot (.) notation:

    :::JavaScript
    alert(CONST.EXPORTCOL_HIDE);

An object can be thought of as a SQL table with two columns: "key" and "value". A value can be accessed if you know the key. For example, the following would select the same value (1) as the above code snippet, if CONST was a SQL table:

    :::sql
    select value
    from CONST
    where key = 'EXPORTCOL_HIDE'

Try to figure out what value the following snippets will display in the alert message. Some of the following will *NOT* work, meaning it will not display a proper value. Try to figure out which one.

    :::JavaScript
    alert(CONST.PERIOD_TYPE.MONTHLY);

    :::JavaScript
    alert(CONST["EXPORTCOL_SHOW"]);

    :::JavaScript
    alert(CONST["PERIOD_TYPE"]["WEEKLY"]);

    :::JavaScript
    var period = "SUMMARY";
    alert(CONST["PERIOD_TYPE"][period]);

    :::JavaScript
    var setting = "PERIOD_TYPE";
    var period = "MONTHLY";
    alert(CONST[setting][period]);

    :::JavaScript
    alert(CONST[PERIOD_TYPE].SUMMARY);

    :::JavaScript
    alert(CONST["PERIOD_TYPE.MONTHLY"]);

The following random image is merely a space-filler to hide the answer below ;-)

![random image](http://lorempixel.com/500/300/)

all of the above will work except for the last two. Note: all attributes (keys) of objects are of type string. When using the dot (.) notation, it is not necessary to use quotation marks. When using square bracket notation ([ ]) one must either use quotation marks, or use a string variable to access the key

