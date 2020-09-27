---
title: "Object Definition"
date: 2016-01-06
category:
- Tutorials
tags:
- JavaScript
- ES5
---

This document is a review of the JavaScript class on 01/06/2016 at my company. Note: this tutorial focuses on the JavaScript ES5 specification, and therefore does not cover the ES2016 `class` syntax.

# Topics covered:

* Object Definition
* Method Chaining

# Some definitions:

This class deals with objects. When talking about objects, people use different names that basically mean the same:

* object : is a type of variable in JavaScript that can hold attributes. For example, an object that represents a rectangle might have two attributes: length and width.
* attribute : is a property / component of an object. 
* class : is a special function in JavaScript that can be used to create objects. The class is the template (like a "cookie cutter") for creating the actual objects
* instance : when talking about a class, the objects that are created from a class are "instances" of the class. The class is the "cookie cutter" and the instance is the cookie. The words "instance" and "object" are basically interchangeable. An "object" is the generic term, and "instance" is a more specific object that got created from a class function
* method : is an attribute of an object if that attribute is a function. For example, an object that represents a rectangle might have a function attribute named "draw" which renders the rectangle on a page. In this case "draw" is a method of the rectangle object

# Object Definition

JavaScript objects are created using curly braces. The simplest object is one with no attributes:

```javascript
    var myObject = {};
```

Attributes can be assigned to an object using dot notation (a period "." character separate the variable name and attribute name) if the name of the attribute is known. For example, to set the "name" and "team" attributes, do the following:

```javascript
    var myPlayerDetails = {}
    myPlayerDetails.name = "Shawn";
    myPlayerDetails.team = "Seahawks";
```

Attributes can also be assigned using square brackets. For example, to set the team attribute:

```javascript
    myPlayerDetails["team"] = "Seahawks";
```

This square brackets notation is useful if the name of the attribute is dynamic (if it is not known at the time you write the code). For example:

```javascript
    var attribute;
    if (city === "Seattle")
        attribute = "team";
    else
        attribute = "typeOfBird";
    myPlayerDetails[attribute] = "Seahawks";
```

Assuming the variable `city` has been defined somewhere, the above snippet will set an attribute named "team" if city is Seattle. If city is not Seattle, the attribute will be named "typeOfBird". In  both cases, the value for the attribute is the string "Seahawks".

To make objects more useful, they can have function attributes. A function that is an attribute of an object, is called a method. Within the method, the other attributes of the object can be accessed using the `this` keyword.

The `this` keyword refers to the object on which the method function got called. The code snippets below will show some examples where the `this` keyword is used.

# Method 1 - Attach attributes to object

In the code snippet below, the `makeNameRegistry` function creates a new object, attaches three attributes to it, and returns it to the caller of the function `makeNameRegistry`.

```javascript
    function makeNameRegistry(names) {}
        var registry = {};
        registry.names = names;
        registry.addName = function(name) {
            this.names.push(name);
        };
        registry.removeNameLike = function(partOfName) {
            var idx,
                name,
                matchIndex;
            for (idx=this.names.length-1; idx>=0; idx--) {
                name = this.names[idx];
                matchIndex = name.indexOf(partOfName);
                if (matchIndex > -1) {
                    this.names.splice(idx, 1);
                }
            }
        }
        return registry;
    }
```

# Method 2 - Create object with attributes in-place

The next code snippet will create and return the same object object as above. The difference is that it creates and defines the object in one step:

```javascript
    function makeNameRegistry(names) {
        return {
            names: names,
            addName: function(name) {
                this.names.push(name);
            },

            removeNameLike: function(partOfName) {
                var idx,
                    name,
                    matchIndex;
                    for (idx=this.names.length-1; idx>=0; idx--) {
                    name = this.names[idx];
                    matchIndex = name.indexOf(partOfName);
                    if (matchIndex > -1) {
                        this.names.splice(idx, 1);
                    }
                }
            }
        }; 
    }
```

# Method 3 - Use the "new" keyword with a "Class" function

The third method of creating objects involves a special function in combination with the `new` keyword in JavaScript.

```javascript
    function NameRegistry(names) {
        this.names = names;
        
        this.addName = function(name) {
            this.names.push(name);
        };
        
        this.removeNameLike = function(partOfName) {
            var idx,
                name,
                matchIndex;
            for (idx=this.names.length-1; idx>=0; idx--) {
                name = this.names[idx];
                matchIndex = name.indexOf(partOfName);
                if (matchIndex > -1) {
                    this.names.splice(idx, 1);
                }
            }
        }
    }
```

When calling the class function with the `new` keyword, a new and empty object gets created automatically. Here is an example:

```javascript
    var registry = new NameRegistry(["Sarah", "John", "Peter"]);
```

Inside the class function, the class function attaches attributes to the newly created object using the `this` keyword

# Method Chaining

Let's use the NameRegistry class function (defined above) to work with an array of names:

```javascript
    var RANDOM_NAMES = [
        "Charlie Scott",
        "Emily Hicks",
        "Alejandro Potter",
        "Lucia Wells",
        "Tamara Collier",
        "Randolph Dawson"
    ];

    var weddingList = new NameRegistry(RANDOM_NAMES);
    weddingList.addName("Judy Harrigan");
    weddingList.addName("Jeff Shoneman");
    weddingList.removeNameLike("o");
    weddingList.removeNameLike("Brady");
```

Here we create one instance of the NameRegistry class and store it in the variable named "weddingList". Then we call the addName method twice on the wedding instance/object. Next, we call the removeNameLike method twice.

Method chaining means we can chain multiple method calls together on the source instance/object. Here is what we would like to do:

```javascript
    var RANDOM_NAMES = [
        "Charlie Scott",
        "Emily Hicks",
        "Alejandro Potter",
        "Lucia Wells",
        "Tamara Collier",
        "Randolph Dawson"
    ];

    var weddingList = new NameRegistry(RANDOM_NAMES);
    weddingList
        .addName("Judy Harrigan")
        .addName("Jeff Shoneman")
        .removeNameLike("o")
        .removeNameLike("Brady");
```

Note: there is no repetition of the weddingList variable and it reads more naturally. Think of it this way:

    To the wedding list, add "Judy Harrigan" and "Jeff Shoneman". Next, remove any names that contain "o" and remove names that contain "Brady"

In order for method chaining to work, each method call / invocation must return the source object. That way, the next method call has an object (the same one) to operate on. 

To make the above method chaining work, we need to modify the methods of the NameRegistry class. Notice that each method now returns the source object by returning `this`   :

```javascript
    function NameRegistry(names) {
        this.names = names;
        
        this.addName = function(name) {
            this.names.push(name);
            return this;
        };
        
        this.removeNameLike = function(partOfName) {
            var idx,
                name,
                matchIndex;
            for (idx=this.names.length-1; idx>=0; idx--) {
                name = this.names[idx];
                matchIndex = name.indexOf(partOfName);
                if (matchIndex > -1) {
                    this.names.splice(idx, 1);
                }
            }
            return this;
        }
    }
```
