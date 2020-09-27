---
title: "Functions. Part 2"
date: 2016-06-29
category:
- Tutorials
tags:
- JavaScript
- ES5
---

This tutorial focuses on three methods of all function objects: `apply`, `call` and `bind`.

The first two sections deal with how functions can be called dynamically.
The last section deals with a concept called "currying", by creating a new function that wraps an existing function.

The examples below are very contrived, but they illustrate the use of these three functions.

# apply: Call functions with array of parameters

Each function object has an `apply` method that can be used to `call` the function with a single array that contains the individual values that should be applied as the parameters for the function.

Assume we have a function to calculate the volume of a block:

```javascript
    function volumeOfBlock(width, length, height) {
        return width * length * height;
    }
```

We can call this function as follows if we have an array of parameter values:

```javascript
    var dimensions = [12, 22, 44];
    var volume = volumeOfBlock.call(null, dimensions);
```

In this example, the volumeOfBlock function got called with two parameters:

* the first parameter is the "context object". The context object is the object the function operates on, and it is the object that will be accessible with the `this` keyword within the function. Since the `volumeOfBlock` function does not need a context object, we specify null.
* The second parameter is the array of parameters. The array has three numbers and these will be the three parameters passed to the volumeOfBlock function

In order to see how the context object works, consider the following Person class and two instances of it:

```javascript
    // Constructor/Class function:
    function Person(firstName, lastName) {
        this.firstName = firstName;
        this.lastName = lastName;

    }
    Person.prototype.fullName = function() {
        return this.firstName + ' ' + this.lastName;
    }

    Person.prototype.introduce = function X(greeting, intro) {
        return greeting + '. My name is ' + this.firstName + ',\n\n' + intro;
    }


    // Person is the class.
    // Use the "new" keyword to create instances or objects of this class:
    var intern = new Person("Sergio", "Torres Gonzalez");
    var talker = new Person("Judy", "Harrigan");
```

There are two functions attached to the Person class. They can be accessed using the prototype object. For example:

Person.prototype.introduce is a function, and we can call it using `call` as follows:

```javascript
    Person.prototype.introduce.apply(intern, ['Hola', 'Nice day today']);
```

In this case, the context object is set to the `intern` instance. This is important because the `introduce` function uses the `this` keyword to access the firstName attribute of the object it operates on.

The above call will return the following message:

    Hola. My name is Sergio,
    Nice day today

Even though the `introduce` function is part of the Person class, it is not necessary to call it with a Person instance.

For example, if we have the following simple object:

```javascript
    var outsider = {
        firstName: 'Lou',
        lastName: 'Pereira'
    };
```

then we can call the `introduce` function as follows:

```javascript
    Person.prototype.introduce.apply(outsider, ['Good morning', 'I am the boss around here']);
```

The above call will return the following message:

```text
    Good morning. My name is Lou,
    I am the boss around here
```

Here the context object is the `outsider` object.


# call: Call functions with sequence of parameters

Each function object has a `call` method that can be used to call the function with a sequence of parameters.

The `call` method is very similar to the `apply` method. It only differs in the way it passes the parameters.

The above call to the `introduce` function on the `outsider` object would look as follows if we use the `call` method:

```javascript
    Person.prototype.introduce.apply(outsider, 'Good morning', 'I am the boss around here');
```

# bind: Create a new wrapping function

Each function object has a `bind` method.
The method `bind` can be used to create a new function that calls the original function with the given `this` context.

Let's say we a function that calculates the volume of a block:

```javascript
    function volumeOfBlock(width, length, height) {
        return width * length * height;
    }
```

Let's assume we have many different blocks but they all have the same area, but they differ in height.
The following would calculate the volume of many world trade centers that all occupy an area of 100 by 75 meters:

```javascript
    var volumeForBostonWTC = volumeOfBlock(100, 75, 100);
    var volumeForMiamiWTC = volumeOfBlock(100, 75, 120);
    var volumeForHoustonWTC = volumeOfBlock(100, 75, 175);
    var volumeForSeattleWTC = volumeOfBlock(100, 75, 160);
```

The first two parameters are always the same. If we want to reuse the `volumeOfBlock` function, but abstract away those parameters (and use the default values), we can expose a new function with only the one parameter that matters: the height of the world trade center:

```javascript
    var volumeForWTC = volumeOfBlock.bind(null, 100, 75);
```

By calling the `bind` method, we're not calling the volumeOfBlock function. Instead, we're creating a new function. We can call this new function as follows instead of the original four calls:

```javascript
    var volumeForBostonWTC = volumeForWTC(100);
    var volumeForMiamiWTC = volumeForWTC(120);
    var volumeForHoustonWTC = volumeForWTC(175);
    var volumeForSeattleWTC = volumeForWTC(160);
```

as with `apply` and `bind`, the first parameter to the `bind` method is the context object. In this case, we don't need a context object for the `volumeOfBlock` function, and specify null. The new function that `bind` creates, supplies the first two parameters. When we call this function, the parameters to this newly created function will be added as additional parameters. In this case, the one and only parameter passed in the call to `volumeForWTC` will become the third parameter passed to `volumeOfBlock` "behind the scenes".

The following statement with `bind`:

```javascript
    var volumeForWTC = volumeOfBlock.bind(null, 100, 75);
```

is basically the same as doing the following:

```javascript
    var volumeForWTC = function(height) {
        return volumeOfBlock(100, 75, height);
    };
```

