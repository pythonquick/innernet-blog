---
title: "Functions. Part 1"
date: 2016-06-22
category:
- Tutorials
tags:
- JavaScript
- ES5
---

This is the first part in the series of functions. These tutorials will help to deal with functions declaration, scoping, parameters, default values and methods.

# Variable-length parameter lists

Consider the following `sumItUp` function and the call to it:

```javascript
    function sumItUp() {
        var sum = 0;
        return sum;
    }
    sumItUp(1, 2, 3, 4, 5, 6, 7);
```

Even though the sumItUp function gets called with 7 parameters, the return value is 0.
The caller wants the function to return the sum of all the supplied parameter values, and the number of parameters is not fixed -- it should work with any number of parameters.

Each function has access to a special `arguments` object. This object is like an array and it contains the values of all parameters that were passed in to the function.
Here is how to use it in the function:

```javascript
    function sumItUp() {
        var sum = 0;
        for (var idx=0; idx<arguments.length; idx++) {
            sum += arguments[idx];
        }
        return sum;
    }
    sumItUp(1, 2, 3, 4, 5, 6, 7);
```

# Variable hoisting

Suppose we have a function that displays a welcome message to a team. By running this function in the inspector and pausing the execution (see the debugger statement), we can inspect the "local" scope in the inspector. It displays all variables declared inside the function and all the parameters supplied.

```javascript
    function displayWelcomeMessage(teamName, teamSize) {
        var message = 'Welcome ' +  teamName;
        debugger
        if (teamSize > 4) {
            message += '. You are a strong team';
        }
        else {
            var doubleTheTeamSize = teamSize * 2;
            message += '. If your team grows 100%, you will have ';
            message += doubleTheTeamSize + ' members in 2017';
        }
        console.log(message);
    }
```

Assume we call the function as follows:

```javascript
    displayWelcomeMessage('A-Team', 5);
```

When the debugger pauses at the debugger statement, it will show the following items in the local scope (apart from the "this" reference):

* teamName
* teamSize
* message
* doubleTheTeamSize

The doubleTheTeamSize variable is declared later in the function, and it won't even be initialized because with the teamSize parameter value of 5, the ELSE block will not execute. So why is it showing up in the local scope? The reason is: when the JavaScript engine runs the function, it will "hoist" up all the variable declarations where the "var" keyword was used, as if these variables have been declared right at the top of the function. Note: the variables might not be initialized with values - they'll be undefined, but they'll be declared.

# Function declaration vs function calls

For the next section, assume the page has the jQuery library loaded in a separate script tag.
The following code will set up the function `pageHasFullyLoaded` to be run when the browser loaded the page fully.

```javascript
    function pageHasFullyLoaded(myParam) {
        debugger
        alert('page has fully loaded');
    }

    $(document).ready(pageHasFullyLoaded);
```

Notes about the `pageHasFullyLoaded` function:

* The function is _declared_ in the first line
* The function is _not_ called in the last line. The jQuery `ready` method gets called and we pass the reference to the function as a parameter. The function does not yet get called
* The function will eventually get called by jQuery when the page has finished loading

# Default values

Consider the following function that prints a greeting message:

```javascript
    function greet(name, title) {
        if (!name) {
            name = 'our respected guest';
        }
        var addressee;
        debugger
        if (!title) {
            addressee = name;
        }
        else {
            addressee = title + ' ' + name
        }
        return "Welcome to the resort, " + addressee;
    }
```

It checks if the parameter values were supplied, by checking the values for truthiness. If the values are not truty (e.g. when not supplied as parameters), it uses defaults.

Remember, the following values are not truthy (they are falsy):

* '' (empty string)
* 0
* null
* undefined

All other things in JavaScript are considered as "truthy".

Now, consider the following function that supplies a default value of 5 if the parameter is falsy:

```javascript
    function rating(stars) {
        if (!stars) {
            stars = 5;
        }
        return "The safety rating is " + stars;
    }
```

There is a potential problem with this.
If zero (0) is a valid safety rating, then the following call will return the string "The safety rating is 5", but we're expecting "The safety rating is 0":

```javascript
    rating(0);
```

In this case, we need to be more specific when checking for the missing value. In this case, instead of merely checking for falsiness, check if the value is undefined. When someone calls the rating function with no parameters, the stars parameter will be undefined.

```javascript
    function rating(stars) {
        if (stars === undefined) {
            stars = 5;
        }
        return "The safety rating is " + stars;
    }
```

# Alternative default values using the OR operator

The || (OR)  boolean operator will "short-circuit" when it finds the first truthy value. Also, the result of the || operator will be the last expression that it evaluated.

For example, the following table shows the result of each expression:

| Expression | Resulting value |
| ---------- | --------------- |
|<code class="javascript">false &#124;&#124; true</code> | true |
|<code class="javascript">"" &#124;&#124; false</code> | false |
|<code class="javascript">"" &#124;&#124; false &#124;&#124; undefined</code> | undefined  |
|<code class="javascript">"x" &#124;&#124; false &#124;&#124; ""</code> | "x" |
|<code class="javascript">"" &#124;&#124; 3 &#124;&#124; true &#124;&#124; "x"</code> | 3 |

We can use this behavior to conveniently supply a default value if something is falsy.

For example, let's say we have the following object with three attributes:

```javascript
    var game = {
        homeTeam: "USA",
        guestTeam: "Argentina",
        referee: "Mexico"
    };
```

Let's say we have a function that takes an object, and returns the value of a given attribute:

```javascript
    function getValueOrDefault(object, attribute) {
        return object[attribute];
    }

    getValueOrDefault(game, 'stadium');
```

When calling the function with the 'stadium' attribute (second parameter), it will return undefined.
That is because our game object does not have a stadium attribute. If we want the getValueOrDefault function to return a default value of "Unknown attribute", we can do it as follows:

```javascript
    function getValueOrDefault(object, attribute) {
        return object[attribute] || "Unknown attribute";
    }
```

# Method functions

When functions are part of an object, we refer to them as "method functions" or simply "methods".

Let's say we want to construct Person objects:

```javascript
    var leader = new Person("Jeff", "Shoneman");
    var intern = new Person("Sergio", "Torres Gonzalez");
```

The `new` keyword in JavaScript creates a new (empty) object and initializes it with the given "constructor function". In this example, we need a constructor function named Person. We also call Person the "class" and the objects (in this case leader and intern) are the "instances" of the class. Note: the words instances and objects are interchangeable.

Here is a Person constructor function needed so that the above will work:

```javascript
    function Person(firstName, lastName) {
        this.firstName = firstName;
        this.lastName = lastName;

        this.fullName = function() {
            return this.firstName + ' ' + this.lastName;
        }
        this.introduce = function(greeting, intro) {
            return greeting + '. My name is ' + this.fullName() + '\n' + intro;
        }
    }
```

Note, that the constructor function uses the `this` keyword. When using the `new` keyword to create new instances, there will be a new object and this new object is set up as the context of the constructor function. That means, inside the constructor function, `this` refers to the new object.
The constructor function adds four attributes to the new object. the attributes firstName and lastName are simply the parameter values passed in. The fullName and introduct attributes have functions as their values

Next, it's possible to call the -function- method of the Person instance:

```javascript
    leader.introduce('Good morning', 'let us get started')
```

