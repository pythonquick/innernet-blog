---
title: "ES2015 Part 5: Destructuring"
date: 2016-10-19
category:
- Tutorials
tags:
- JavaScript
- ES2015
---

Part 5 in the series of ES2015 deals with destructuring: with arrays and with objects.

# Array destructuring

The following `logCoordinate` function takes an array as a parameter, and then reads the values from three indexes and assigns them to variables:

```javascript
    function logCoordinate(coordinate) {
        var x = coordinate[1];
        var y = coordinate[2];
        var z = coordinate[3];
        return "Your spacial coordinate is (" + x + ", " + y + ", " + z + ")";
    }

    logCoordinate(["5-October-2016", 12, 35, 22]);
```

Here the `logCoordinate` function gets called with an array containing four items: 

* A string that represents a calendar date
* The location's x coordinate
* The location's y coordinate
* The location's z coordinate

The ES2015 destructuring syntax can be used to make these assignments all in one line.
On the left hand side of the variable declaration is the list of variable names enclosed in square brackets.
On the right hand side is the array that contains the values to be assigned.

```javascript
    function logCoordinate(coordinate) {
        let [date, x, y, z] = coordinate;
        return "Your spacial coordinate is (" + x + ", " + y + ", " + z + ")";
    }

    logCoordinate(["5-October-2016", 12, 35, 22]);
```

Note: in this example, we do not need the first array element (the date string).
In that case, the array destructuring can omit the `date` variable name. It is still necessary to have a comma before the `x` variable, to ensure the correct positional value assignment.

Here's how that looks like:

```javascript
    function logCoordinate(coordinate) {
        let [, x, y, z] = coordinate;
        return "Your spacial coordinate is (" + x + ", " + y + ", " + z + ")";
    }

    logCoordinate(["5-October-2016", 12, 35, 22]);
```


# Object destructuring

Similar to array destructuring, in ES2015, parts of an object can be assigned to variables.

To illustrate, let's work with an object. In this example, it's an object that represents the key features of a movie:

```javascript
    var JAWS = {
        title: "Jaws",
        year: 1975,
        people: {
            director: "Steven Spielberg",
            star: "Roy Scheider"
        }
    };
```

The following function gets called with the JAWS object:

```javascript
    function movieInfo(movie) {
        let title = movie.title;
        let year = movie.year;
        let director = movie.people.director;
        let star = movie.people.star;
        return title + ' played in ' + year + ' directed by ' + director + ' starring ' + star;
    }

    movieInfo(JAWS);
```

The call to movieInfo returns the following string:

```text
    Jaws played in 1975 directed by Steven Spielberg starring Roy Scheider
```

Using ES2012's object destructuring, the variable declaration on the left hand side of the `=` sign, look like an object declaration with key/value pairs separated by `:` characters inside curly braces:

```javascript
    function movieInfo(movie) {
        let {title: title, year: year} = movie;
        let director = movie.people.director;
        let star = movie.people.star;
        return title + ' played in ' + year + ' directed by ' + director + ' starring ' + star;
    }

    movieInfo(JAWS);
```

The first line inside the function uses ES2015's object destructuring to define two variables: title and year. The values for these variables correspond to the "title" and "year" attributes from the movie object.
The variable name and the key/attribute from the object must not necessarily have the same name. In the above example, there's a lot of repetition because the variable name is the same as the object key.
In ES2015's object destructuring, there's a shortcut if the variable name and the object key is the same. The above example can be rewritten as follows:

```javascript
    function movieInfo(movie) {
        let {title, year} = movie;
        let director = movie.people.director;
        let star = movie.people.star;
        return title + ' played in ' + year + ' directed by ' + director + ' starring ' + star;
    }

    movieInfo(JAWS);
```

That's syntax takes some getting used to, but it's nice and concise.
Note, that we still have separate assignment statements for director and star. Those are attributes of the nested object under the "people" attribute.
Nested attributes can also be used in ES2015's object destructuring, by specifying the nested object's key and using another set of curly braces. 
Here's another that assigns all four variables in one object destructuring line:

```javascript
    function movieInfo(movie) {
        let {title, year, people: {director, star}} = movie;
        return title + ' played in ' + year + ' directed by ' + director + ' starring ' + star;
    }

    movieInfo(JAWS);
```

That looks very concise!

The object destructuring can even appear in the parameter list. This way, the function receives four parameter values but they come from a single object passed in as an argument:

```javascript
    function movieInfo({title, year, people: {director, star}}) {
        return title + ' played in ' + year + ' directed by ' + director + ' starring ' + star;
    }

    movieInfo(JAWS);
```

This is the shortest version so far, but it is questionable whether it is easier to understand. Better use the version that takes a single `movie` object parameter.

Finally, when destructuring objects, the source object (on the right hand side of the `=` sign) might not have the attributes specified on the left hand side of the `=` sign.
In that case, it's possible to supply a default value. Here's an example that takes a `SULLY` movie object that's missing the `year` attribute.

```javascript
    var SULLY = {
        title: "Sully",
        people: {
            director: "Clint Eastwood",
            star: "Tom Hanks"
        }
    };

    function movieInfo(movie) {
        let {title, year = 2016, people: {director, star}} = movie;
        return title + ' played in ' + year + ' directed by ' + director + ' starring ' + star;
    }

    movieInfo(SULLY);
```

# Default parameter values

Last topic is the ability to specify default parameter values, even though it's not directly related to destructuring. When using destructuring inside function parameter lists, one can use default values - that's why this topic made it into "Part 3".

In JavaScript, function parameters are optional. Even if the function declares two parameters, the function can still be called with zero, one or many parameters. 

Let's say we have a function that takes two parameters: an amount and a tax percentage and it returns the after-tax amount:

```javascript
    function totalAmount(amount, taxPercentage) {
        return amount * (100 + taxPercentage) / 100;
    }

    totalAmount(25.00, 6);
```

Here we call the function with two arguments: the amount 25 and tax percentage of 6.

What if the tax does not apply? The tax percentage could be zero and it would be nice to let it default to zero if the second argument is not passed in.
Here's one way of achieving this, by checking if the parameter is undefined. Here we provide a default value of 0 if the parameter was not supplied:

```javascript
    function totalAmount(amount, taxPercentage) {
        if (taxPercentage === undefined) {
            taxPercentage = 0;
        }
        return amount * (100 + taxPercentage) / 100;
    }
    totalAmount(25.00);
```

In ES2015 the default value can be specified in the function's parameter list directly:

```javascript
    function totalAmount(amount, taxPercentage = 0) {
        return amount * (100 + taxPercentage) / 100;
    }
    totalAmount(25.00);
```

Nice!

