Title: Closure Functions
Date: 2016-03-03
Category: Tutorials
Tags: JavaScript, ES5

Quick definition of a closure in JavaScript:

> A function that "captures" or holds on to variables of its enclosing (parent) function.

That means a closure is always a function inside a function. Normally the local variables (and parameters) of a function only "live" during the call/execution of a function. Once the function completes or returns, the memory for those local variables are released or cleaned up. If the parent function returns a child function that references variables of the parent function, the JavaScript runtime (browser) cannot clean up the variable for those local variables. They need to stay around because the child function depends on them.

Let's consider an example. Let's suppose Judy needs to paint the ceiling of three rooms. She buys three cans of special ceiling paint - one for each room. The labels of the paint cans have an unusual way of specifying the volume. The label specifies how big a circle the paint can cover. For example, the small can of paint can cover the area of a circle that has a 3-foot radius. Is there enough to paint the three places that need renovation ?  

* The closet has an area of 10 square feet.
    * The can for closet ceiling paint is enough to paint the area of a 3-foot radius circle.
* The bathroom has an area of 150 square feet.
    * The can for bathroom ceiling paint is enough to paint the area of a 7-foot radius circle
* The entire second floor has an area of 1000 square feet.
    * The can for living area ceiling paint is enough to paint the area of a 10-foot radius circle

The snippet below will determine if Judy's cans of paint are enough to cover the above three rooms:

    :::JavaScript
    function generateCircleAreaChecker(radius) {
        var aeraOfCircle = Math.PI * radius * radius;

        return function(area) {
            // Return true if given area is within the area
            // of a circle of given radius:
            return area <= aeraOfCircle;
        };
    }


    function checkPaintCoverage(params) {
        var circleAreaChecker = generateCircleAreaChecker(params.paintCircleRadius);
        var isWithinCircleArea = circleAreaChecker(params.roomArea);
        if (isWithinCircleArea)
            console.log('YES! Enough paint to paint ' + params.room);
        else    
            console.log('NO... Not enough paint to paint ' + params.room);
    }


    // Check if the 3 rooms can be painted by the room's can of paint:
    checkPaintCoverage({room: 'Closet', roomArea: 10, paintCircleRadius: 3});
    checkPaintCoverage({room: 'Bathroom', roomArea: 150, paintCircleRadius: 7});
    checkPaintCoverage({room: 'Second Floor', roomArea: 1000, paintCircleRadius: 10});

At the bottom of the snippet, we call the `checkPaintCoverage` function to check if the can of paint for each room will be enough. Here is the output on the console:

    YES! Enough paint to paint Closet
    YES! Enough paint to paint Bathroom
    NO... Not enough paint to paint Second Floor

**Side Note:**

the `checkPaintCoverage` function takes only one parameter: an object containing three values. In some cases, passing multiple values inside an object can make things clearer because each value can be named. In the above snippet, the values are named `room`, `roomArea` and `paintCircleRadius`. In this case, we could have used three separate parameters - no difference. In cases where there's a very long list of 5 or more parameters, it can be clearer if the parameters are named. In the case of using a single object parameter, the order of the values inside the object don't matter. However, with a list of parameters, the order must match the order in which the function expects the parameters.

"So, where is the closure function?", you might ask. The picture below shows:

![closure](https://innernet.io/media/closure.png)

If you look at the ` generateCircleAreaChecker` function, you'll see that it defines a local variable called `aeraOfCircle` which contains the area of a circle with the given radius. 
In the first line of the function, it generates a function that is initialized with a radius for a circle.

This `generateCircleAreaChecker` function returns a nested (child) function. Notice that the child function references the variable `areaOfCircle` which is defined outside of the child function. It uses the pre-calculated area of the circle to compare the parameter that gets passed to it. In this case, since the child function will be returned and the child function references the outside variable `areaOfCircle`, it means the `areaOfCircle` variable needs to stay around - the JavaScript runtime environment (browser) will not clean up the memory for that variable as long as the child function is in scope. The child function "closes over" or captures a snapshot of the local variable `areaOfCircle` and holds on to it. Note: eventually the memory of the `areaOfCircle` variable will be cleaned up. When? As soon as the `checkPaintCoverage` function call is done, because the `checkPaintCoverage` function is the only place that holds a reference to the closure function.

That's it! Closures are basically just nested functions that reference (and hold on to) variables from their enclosing function. They remember the context or values when they were created.
