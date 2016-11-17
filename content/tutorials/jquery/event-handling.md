Title: Event handling with jQuery
Date: 2015-12-22
Category: Tutorials
Tags: JavaScript, jQuery

The following example uses jQuery to handle browser events. The event-handling can be done with raw DOM objects, but jQuery provides a nice interface for dealing with the DOM. Also, some browsers have different DOM object implementation and behavior. jQuery takes care of any differences between browsers and versions and provides a consistent interface for handling page elements and events.

jQuery provides the `on` method. Once you selected the target elements using a jQuery selector, you can attach event-handler functions. 

Here is a sample HTML page with a table:

    :::HTML
    <html>
        <head>
            <link rel='stylesheet' type='text/css' href='index.css'>
        </head>
        <body>

            <table id='MyTable'>
                <thead>
                    <tr>
                        <th>Name</th>   <th>Team</th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <td id='a'>Judy</td>   <td id='b'>Mariners</td>
                    </tr>
                    <tr>
                        <td id='c'>Jeff</td>   <td id='e'>Phillies</td>
                    </tr>
                </tbody>
            </table>

            <script src='lib/jquery.js'></script>
            <script src='index.js'></script>
        </body>
    </html>

You can see the table has one heading row with heading cells (`th`) and two rows of regular cells (`td`). The page imports the jquery.js file which is needed for jQuery. 
The other imported script file is index.js and looks as follows:

    :::JavaScript
    function headingClicked() {
        alert('You clicked cell a heading');

    }

    function doMouseOver(coolMouseEvent) {
        var element = $(coolMouseEvent.currentTarget);
        element.css('background', '#ffaaaa'); // light red
    }


    function doMouseOut(event) {
        var element = $(event.currentTarget);
        element.css('background', '#ffffff'); // white
    }

    $(document).ready(function() {
        $('#MyTable th').on('click', headingClicked);
        $('#MyTable td').on('mouseover', doMouseOver);
        $('#MyTable td').on('mouseout', doMouseOut);
    });

When the page loaded, the function that was passed into the jQuery ready function will be called (see the bottom part of the JavaScript file above).
Here, it sets up three event handlers:

* When the user clicks a `th` element that has a parent element with the id "MyTable", the headingClicked function will be called
* When the user's mouse moves over a `td` element that's inside the MyTable table, the `doMouseOver` function will be called
* When he user's mouse moves out of that `td` element, the `doMouseOut` function will be called

Notice that the three event-handling functions (`cellClicked`, `doMouseOver` and `doMouseOut`) do not get called when setting up the event-handling. The function itself gets passed in as argument. It is only at the time when the event actually occurs that the function will get called by the browser and jQuery. 

When these event-handling functions get called, they automatically get called with one argument: an event object that contains more details about the event that has just occurred. The event-handling function can use this event argument but does not have to.

In our example, the click-handling function (`headingClicked`) only cares about the fact that the heading was clicked. It doesn't need to look at more specifics of the event. In that case, it does not define an argument. It still gets passed in the argument, but it doesn't reference it in an argument variable.

The other two mouse-handling functions (`doMouseOver` and `doMouseOut`) _do very much_ care about the specifics of the event. They need to set the background color of the cell where the mouse moved over (or out of). They read the `currentTarget` object from the event object, which is the raw DOM element that the user's mouse moved over (or out of). For convenience, we wrap this DOM element object in a jQuery object and then use the jQuery `css` method to set a CSS style.

The screen capture below shows the event-handling in action.

![click mouse event demo]({filename}/extras/click-mouse-event-demo.gif)
