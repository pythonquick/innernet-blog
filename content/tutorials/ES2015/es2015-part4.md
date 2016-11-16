Title: ES2015 Part 4: Rest and Spread operators
Date: 2016-09-23
Category: Tutorials
Tags: JavaScript, ES2015

Part 4 in the series of ES2015 deals with the new JavaScript operators: rest and spread

# The rest operator

The rest operator comes into play when a function receives a variable list of parameters. Before we look at the operator, let's first consider a function that takes a few parameters:

    :::JavaScript
    function registerFamily(mother, father, child1, child2, child3) {
        let response = `${mother} and ${father} have 3 kids: ${child1}, ${child2}, ${child3}`;
        return response;
    }


    registerFamily("Hilda", "Frederick", "Bobby", "Sally", "Jenny");

Here, the `registerFamily` function gets called with five parameters. It expects a family of five, so this function is not very versatile. It assumes the mother and father have exactly 3 children.

To make this more flexible, we can use the `arguments` keyword. The `arguments` variable exists inside a function body during the execution of the function. It is an array-like object that we can use to inspect the actual parameters that were passed to the function. This allows us to make the function more flexible:

    :::JavaScript
    function registerFamily(mother, father) {
        let response = `${mother} and ${father} have ${arguments.length - 2} kids: `;
        for (let idx=2; idx<arguments.length; idx++) {
            response += arguments[idx];
            if (idx < arguments.length - 1) {
                response += ', ';
            }
        }
        return response;
    }

The function now has two named parameters: mother and father. The `arguments` object contains _all_ the parameters. That means, we have to subtract 2 from its length, when dealing with parameters after the mother and father values. It feels clunky.

In ES2015, we can capture the remaining parameters using the rest operator. The rest operator consists of three periods and a variable name. It collects the remaining parameters that were not named in the parameter list - the "rest" of the parameters.

Here's what the function looks like with the rest operator to capture any parameters other than the first two:

    :::JavaScript
    function registerFamily(mother, father, ...children) {
        let response =`${mother} and ${father} have ${children.length} kids: `;
        for (let idx=0; idx<children.length; idx++) {
            response += children[idx];
            if (idx < children.length - 1) {
                response += ', ';
            }
        }
        return response;
    }

This looks similar to the approach with using the `arguments` keyword. Note: the children variable does not include the first two parameters as with the `arguments` object. This makes the loop clearer - no need to subtract 2. We can still simplify the above example by using the array method: `join`.

As a quick aside, here's an example of using the array method `join` to create a concatenated string that contains all array elements:

    :::JavaScript
    var nineties = ["George", "Gerald", "Herbert", "Jimmy", "John", "Ronald"];
    console.log("U.S. presidents that lived more than 90 years:");
    console.log(nineties.join(', '));

With this convenience method, we can simplify the registerFamily function:

    :::JavaScript
    function registerFamily(mother, father, ...children) {
        return `${mother} and ${father} have ${children.length} kids: ${children.join(', ')}`;
    }

Another advantage of using the rest operator as opposed to `arguments` is that the rest variable (in the above example the children array) is a genuine array, whereas `arguments` behaves like an array (we can query the length and access indexed items). Since the `arguments` object is not a true array, we cannot use array methods like `join`.

# The spread operator

The spread operator looks the same as the rest operator: it is three periods followed by a variable name.
The rest operator is used in the context of a function receiving its parameters.
The rest operator takes a variable number of items and collects them into an array.
The spread operator does the opposite: it starts out with a given array and "spreads" the array items out into individual items.

To explain this, let's first look at the example of using the built-in Math.min function:

    :::JavaScript
    Math.min(45, 27, 44, 28, 26, 47, 29, 42, 46);

The call to `Math.min` above will return the minimum parameter number passed to it: 26

Here we have a fixed list of parameters, but what if the number of values are not known ahead of runtime? The numbers could be in an array. How could we still call the Math.min function? One way would be to call the `apply` method of any function object:

    :::JavaScript
    let numbers = [45, 27, 44, 28, 26, 47, 29, 42, 46];
    Math.min.apply(null, numbers);

Remember, the apply method takes the context object as the first parameter. The context object is what becomes the "this" inside of the function. In this case, there is no context "this" object, so we just pass in a `null`. The `apply` function calls the function with the individual parameters taken from the items of the supplied array. How else can we call Math.min using the numbers array? You guessed it - the rest operator!

    :::JavaScript
    let numbers = [45, 27, 44, 28, 26, 47, 29, 42, 46];
    Math.min(...numbers);

Here the call to Math.min uses the spread operator to spread the array contents out into individual parameters for the Math.min function.

The spread operator can also be used to combine two arrays into a new array:

    :::JavaScript
    var forties = [45, 44, 47, 42, 46];
    var twenties = [27, 28, 26, 29];

    var numbers = [...twenties, 39, 37, 38, ...forties];
    Math.min(...numbers);


