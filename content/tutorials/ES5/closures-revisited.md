---
title: "Closures Revisited"
date: 2016-07-20
category:
- Tutorials
tags:
- JavaScript
- ES5
---

The lesson covers some aspects of closures and some gotchas. 
For an introduction about the concept of closures, see the past lesson notes on [closure functions](/closure-functions.html)

This lesson looks at some common gotchas when dealing with closures and the scope of variables. The main ideas to remember from the last closures lesson is:

* Locally declared variables within a function (where the `var` keyword is used), will be recycled by the JavaScript engine when the function completes. That means, the memory for those variables will be released and those variables will no longer be available.
* The exception to this rule is when the function creates another function that accesses the locally declared variables of its outer parent function. The inner function "closes over" the variables declared by its outer function. Those referenced variables will have to stay around for as long as the inner function is referenced.

# Common closures loop bug

This section looks at a subtle bug that can arise when closure functions are defined within a for loop. 

Consider the following body of a simple HTML page:

```html
    <body>
        <h3>Here are some buttons:</h3>
        <ul id='button-list'>
        </ul>
    </body>
```

Next, the page's JavaScript file initializes the list with three list items as soon as the page loads in the browser:

```javascript
    $(document).ready(initDocument);


    function initDocument() {
        var buttonList = $('#button-list');
        for (var idx=0; idx<3; idx++) {
            var listItem = $('<li></li>');
            var button = $('<button>Button ' + idx + '</button>');
            button.on('click', function() {
                alert('You clicked button ' + idx);
            });
            listItem.append(button).appendTo(buttonList);
        }
    }
```

At first sight, one would assume that each button click would display a different alert message, but this is not the case.
Each button click displays the message:

    You clicked button 3

Why is this?

The click handler-function that's attached to the button references the idx variable from the outer (initDocument) function. The click handler-function is therefore a closure function. In fact, each of the three buttons has a separate closure function and they all reference the same idx variable as illustrated by the following graphic:

![Closure Loop Bug](/extras/closures-loop-bug.png)

The problem is that the click handler-function does not capture the current value of the idx variable, it merely references the idx variable which will change as the for loop iterates.

One solution is to call a function that returns a click handler-function that's seeded with the current value of the idx variable:

```javascript
    function makeClickHandler(idx) {
        return function() {
            alert('You clicked button ' + idx);
        };
    }


    function initDocument() {
        var buttonList = $('#button-list');
        for (var idx=0; idx<3; idx++) {
            var listItem = $('<li></li>');
            var button = $('<button>Button ' + idx + '</button>');
            button.on('click', makeClickHandler(idx));
            listItem.append(button).appendTo(buttonList);
    }
```

Each time makeClickHandler gets called, it will return a new function. That returned function is still a closure because it references the idx parameter variable of the makeClickHandler function. But in this case that is a separate copy of the original idx variable and will not change.

Another approach would be to put the entire list item creation into the function instead of merely returning the click-handler:

```javascript
    function makeIndexListItem(idx) {
        var listItem = $('<li></li>');
        var button = $('<button>Button ' + idx + '</button>');
        button.on('click', function() {
            alert('You clicked button ' + idx);
        });
        listItem.append(button);
        return listItem;
    }


    function initDocument() {
        var buttonList = $('#button-list');
        for (var idx=0; idx<3; idx++) {
            var listItem = makeIndexListItem(idx);
            listItem.appendTo(buttonList);
        }
    }
```

This might be a good approach when some other functionality on the page might ant to create new list items - the makeIndexListItem function can then be reused.

Lastly, another way of creating a separate function and seeding it with the current loop iteration's idx variable value, is to use the `bind` function method to create a new function that will pass the specified idx value as a parameter to the function that gets bound. See the last lesson on function methods: http://redmine.pma.space/projects/js-class/wiki/06-29-2016_Functions_part_2#bind-Create-a-new-wrapping-function.

```javascript
    function initDocument() {
        var buttonList = $('#button-list');
        for (var idx=0; idx<3; idx++) {
            var listItem = $('<li></li>');
            var button = $('<button>Button ' + idx + '</button>');
            button.on('click', function(theIndex) {
                alert('You clicked button ' + theIndex);
            }.bind(null, idx));
            listItem.append(button).appendTo(buttonList);
        }
    }
```

Note: the new function created by the `bind` method wraps the function that it was called on - the inner function. It passes the index as the first `theIndex` parameter. So, what happens to the event parameter when the user clicks the button? The event object gets passed as a parameter to this wrapping function (the function returned by the call to `bind`), and the event object will then in turn get passed on to the inner function - as its second parameter. Since the inner function does not need the event object, it does not list a parameter variable for it. It only lists the first parameter as `theIndex`.

# Variable scoping bug

The following code example was taken from a project, and updated only slightly:

```javascript
    function printRowsToTable(coffeeProduct, table){
        var tr = $('<tr></tr>');
        $('<td>' + coffeeProduct.name + '</td>').appendTo(tr);
        var btnDelete = $('<button>Delete</button>');
        btnDelete.click(function(e, coffeeProduct, tr){
            e.preventDefault();
            alert('Deleted coffee product: ' + coffeeProduct.name);
            $.ajax({
                url: SDEFMODDIR + SDEFMOD + "?FORMID=A4APICOFFEEPRODUCTDELETE&" + USESSION + 
                "&FTYPE=R&INIT=Y&TSESSIONSAVE=NO&KCOFFEEPRODUCT=" + coffeeProduct.id
            });
            tr.remove();
        });
        var buttonCell = $('<td></td>');
        btnDelete.appendTo(buttonCell);
        tr.append(buttonCell);
        table.append(tr);
    }
```

Here the delete button's click handler-function will fire as soon as the user clicks the button.
BUT, the AJAX call will not fire. In fact, it will not even reach the AJAX call because the alert statement will run into an exception, saying that name is not an attribute of undefined.
What is the bug?

When the click handler-function gets called, the coffeeProduct variable is undefined. The reason for this is that there is a parameter named coffeeProduct defined in the click function's list of parameters but it is not supplied. When the click function gets called, the browser and jQuery pass only one parameter: the click's event object. All further parameters that the function lists will not be supplied and will therefore be undefined. So in this case, the coffeeProduct parameter name "masks" the outer coffeeProduct parameter.

To fix the scoping bug, simply remove the parameters of the click function (except for the first parameter - the event object), so that the click function can act as a closure function and access the proper variables from its surrounding scope.
