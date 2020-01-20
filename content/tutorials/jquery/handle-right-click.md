Title: Handle right-click browser event
Date: 2016-11-15
Category: Tutorials
Tags: JavaScript

A few months ago, a friend of mine claimed that it's probably very tricky to handle the right-click mouse event on a web page, since the browser already handles the right-click event. "How difficult can that be?", i thought to myself.

It turns out it's not all that difficult. This article explains one approach to handling the case when the user does a right-click with the mouse.

The browser normally implements its own default action when the user does a right-click. Typically, it's a context menu with some page actions, like reloading or saving the page or viewing the page source, etc. If the HTML page needs to use its own application-specific right click action, it is easily achieved.

Regular left-click actions can be used by specifying a handler function for the 'click' event:

    :::JavaScript
    var menuButton = document.getElementById('menuBtn');
    menuButton.addEventListener('click', function(e) {
        // handle the click event
    });

Any right-click action will not trigger the 'click' event however.

Other mouse events like mousedown and mouseup react to all types of click events, whether the user uses the left, middle or right mouse button:

    :::JavaScript
    var menuButton = document.getElementById('menuBtn');
    menuButton.addEventListener('mousedown', function(e) {
        alert('mouse down event with button index ' + e.button);
    });

The above snippet will capture the right-click action. To determine whether the user clicked the left or the right button, the `button` attribute of the event object can be used. A value of 0 means left button and 2 means right button was clicked.

Note: with the above snippet, when the user does a right-click the browser will still show the default context menu. There's an additional event that fires when the user clicks the right mouse button: the `contextmenu` event. To prevent the browser's default right-click behavior, we can handle the `contextmenu` event and prevent the default behavior by calling the `preventDefault` method on the event object:

    :::JavaScript
    var menuButton = document.getElementById('menuBtn');
    menuButton.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });

Without the `preventDefault()` call, the `contextmenu` event would "bubble up" to any further event listeners, and eventually the browser's listener would handle the `contextmenu` event and show the context menu.

To see this in action, here is the code to handle different click events inside the 'clickbox' DIV box below:

    :::JavaScript
    var clickbox = document.getElementById('clickbox');
    clickbox.addEventListener('mousedown', function(e) {
        var buttonSide = e.button === 0 ? 'left' : 'right';
        alert(buttonSide + '-clicked the ' + e.target.nodeName + ' tag');
    });
    clickbox.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });

<div id='clickbox' style='background-color: #ddddee; padding: 2em'>
    This is the clickbox. Click inside to test mouse click events!
    <hr>
    <button>button</button>
    <img src='{static}/extras/cat.png'>
</div>
<script src="{static}/extras/handle-right-click.js"></script>


