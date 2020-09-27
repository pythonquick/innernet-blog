---
title: "ES2015 Part 3: Arrow Functions"
date: 2016-09-02 11:00
category:
- Tutorials
tags:
- JavaScript
- ES2015
---

Part 3 looks at a new way of declaring functions.

# Arrow functions

Arrow functions (also called "fat arrow functions") provide a short-hand syntax for declaring functions.

The general syntax looks like this:

<pre>
(x)  =＞ { }
</pre>

The above creates a function that takes one parameter. The body of the function is inside the curly braces: { }. The above function has an empty body, so it does nothing at all.

There are two further simplifications possible:

* If the function takes only one parameter, the parentheses around the parameter are optional
* If the function consists of a single return value, the curly braces can be omitted. In that case, the expression after the => (fat arrow) becomes the returned result and the `return` keyword is not used.

For example, the following is a function that returns the square of the input parameter number. Since the function consists of a single return statement, there are no curly braces and no `return` statement:

<pre>
x    =＞ x*x
</pre>

## Simple usage

The following example shows three calls to function `displayResult`. For each call, a function gets passed as the third parameter - the arrow function . The `displayResult` function will then call this function with the supplied parameter:

```javascript
    function displayResult(title, value, func) {
        console.log(title, 'of', value, 'is', func(value));
    }


    displayResult('identity'                    , 5,   x => x );
    displayResult('square'                      , 6,   x => x*x );
    displayResult('area of circle with radius'  , 7,   x => x*x*3.14 );
```

The output looks as follows:

<pre>
identity of 5 is 5
square of 6 is 36
area of circle with radius of 7 is 153.86
</pre>

## Useful with array methods

Arrays in JavaScript have several methods that take callbacks to transform, filter or operate on the array content:

* every
* filter
* find
* forEach
* map
* sort

One of these array methods is `map` which creates a new array based on the original array with each array element transformed according to the specified callback function.

The following will create a new array containing the volume of the given side-lengths of five cubic boxes:

```javascript
    let boxLengths = [1, 4, 6, 16, 24];
    let boxVolumes = boxLengths.map(x => x*x*x);
    for (let idx=0; idx<boxVolumes.length; idx++) {
        console.log(
            'Box with side length of',
            boxLengths[idx],
            'has volume of',
            boxVolumes[idx]
        );
    }
```

It will output the following:
<pre>
Box with side length of 1 has volume of 1
Box with side length of 4 has volume of 64
Box with side length of 6 has volume of 216
Box with side length of 16 has volume of 4096
Box with side length of 24 has volume of 13824
</pre>

Another array method is `filter`, which returns a new array which is a subset of the original array. The supplied callback function determines whether a given array element should be included in the returned (filtered) array. Here's an example that outputs which of the original numbers are divisible by 16:

```javascript
    let numbers = [15, 48, 80, 94, 128, 140];
    let sixteens = numbers.filter( x => x % 16 === 0 );
    console.log(
        "From the sequence of numbers, the ones divisible by sixteen are: ",
        sixteens.join(", ")
    );
```

The output will look as follows:

<pre>
From the sequence of numbers, the ones divisible by sixteen are:  48, 80, 128
</pre>

In the above cases, it would make no difference to use an arrow function, or an inline function. The nice thing about arrow functions is that it requires less boilerplate code. They are more succinct and easier to read when when dealing with simple transformation functions.

## The "this" context

In a JavaScript function the `this` keyword refers to the context in which the function got called. The context is the object on which the function gets called.

Consider this example:

```javascript
    let bob = {
        name: 'bob', 
        friends: ['Susan', 'Joe', 'Michael'], 
        printFriends: function() {
            console.log(this.name, "has", this.friends.length, 'friends')
        }
    };

    bob.printFriends();
```

Here, `printFriends` is a method function, called on the `bob` object. When the `printFriends` function executes, the `this` keyword will point to the `bob` object. The output looks as follows:
<pre>
Bob has 3 friends
</pre>

Consider the following version that attempts to use the forEach array method to print out bob's friends:

```javascript
    let bob = {
        name: 'bob', 
        friends: ['Susan', 'Joe', 'Michael'], 
        printFriends: function() {
            this.friends.forEach(
                function(item) { 
                    console.log(this.name + " knows " + item);
                }
            );
        }
    };

    bob.printFriends();
```

The output will not be as expected:
<pre>
undefined knows Susan
undefined knows Joe
undefined knows Michael
</pre>

Why is it printing undefined instead of bob?
The reason for this is that we lost the original context to the bob object. When the `forEach` array method calls the specified callback function, that callback function does not get called on the bob object. Therefore, the `this` keyword inside the specified callback function will not point to bob. In fact, because we're not running this script in "strict mode", the `this` keyword will point to the global context: the browser's Window object which also holds all global variables. Unless we previously defined a global variable with the name of "name", it will output "undefined" as above.

A workaround could be to capture the `this` object into another variable, and then reference that variable inside the callback function - using JavaScript's closure capability. Below is another version that captures the `this` context into a variable named "me":

```javascript
    let bob = {
        name: 'bob', 
        friends: ['Susan', 'Joe', 'Michael'], 
        printFriends: function() {
            var me = this;
            this.friends.forEach(
                function(item) { 
                    console.log(me.name + " knows " + item);
                }
            );
        }
    };

    bob.printFriends()
```

Now the output looks as expected:
<pre>
bob knows Susan
bob knows Joe
bob knows Michael
</pre>

A consequence of using arrow functions as opposed to regular functions, is that arrow functions do not create a new context when called. That means, when we use the `this` keyword inside the body of an arrow function, it will refer to `this` from the surrounding function. Here's how we can change the code to use an arrow function:

```javascript
    let bob = {
        name: 'bob', 
        friends: ['Susan', 'Joe', 'Michael'], 
        printFriends: function() {
            this.friends.forEach( 
                item => { 
                    console.log(this.name + " knows " + item); 
                }
            );
        }
    };

    bob.printFriends()
```

Note: the above examples with `forEach` merely illustrate the context behavior. A regular old `for` loop would probably work better in this case than using the `forEach` method.
