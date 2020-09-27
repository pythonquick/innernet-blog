---
title: "ES2015 Part 1: Variable declaration"
date: 2016-09-02 09:00
category:
- Tutorials
tags:
- JavaScript
- ES2015
---

Some background around JavaScript specifications:

Most (if not all) current browsers support the ES5 specification. Internet Explorer 8 however does not support ES5, it supports the previous version of JavaScript: ES3. Yes, that's right - there is no ES4. ES4 was never finalized due to various disagreements among the stakeholders and members of the specification team.

In the past, the new specifications to the JavaScript language were slow to be finalized. ES3 was released in December 1999 and ES5 came about 10 years later in December 2009.
TC39 is a technical committee that oversees the JavaScript language specification. They work on proposals to update the JavaScript language and define the specification. Each new proposal gets thoroughly vetted and moves through several "maturity stages" until it finally gets included in the specification or dropped. TC39 intends to increase the cadence of new language specifications to be yearly. As of now (September 2016), ES2015 is the latest "released" JavaScript specification. The "2015" refers to the year when the specification was finalized and the intent is for new language features to be finalized annually. That means, the next JavaScript specification should be finalized later in 2016 as ES2016. 

Not all browsers fully support ES2015 yet, but eventually will. That doesn't mean we cannot already use ES2015 language features and syntax in JavaScript programs. To make ES2015 language features work on non-ES2015 browsers, one can use a so-called "transpiler". This is a component that transforms the ES2015 JavaScript into equivalent ES5 JavaScript code, to be processed by the browser if the browser does not already implement ES2015. One such transpiler is Babel: https://babeljs.io/ and is used in modern web frameworks.

This lesson is the first in a series about ES2015. This will be far from a complete coverage of the ES2015 language features. The idea is to focus mostly on the features that we'll encounter when writing Ember applications. There is also a ES2015 course on CodeSchool.

# Declaration with let and const

## The let keyword

Before ES2015, variables were declared using the `var` keyword. By using `var`, the variable gets created in the current execution "scope". The scope is the function in which the `var` keyword appears, or it is the global scope if the `var` is defined in the outside scope -- that is the same as declaring a variable without the `var` keyword,

One interesting aspect to note about the `var` keyword, is that it "hoists" variables up to the beginning of the function. That means, inside a function, a variable will exist even if it gets declared (with the var keyword) much further down in the function.

In ES2015 there is a new keyword for defining variables: `let`
The `let` keyword has the following differences:

* No variable hoisting.
* There will be an error when defining a variable with `let` if that variable already exists in the execution scope
* Variables defined with `let` will be scoped inside the current block, e.g. within an if-block or inside a for-loop, whereas variables declared with `var` will be in scope in the entire function even if they're declared within an inner if-block inside the function - remember, the `var` variable gets hoisted to the top of the function

The following function will fail with an error when called without a parameter, because the title variable is only defined in side the if-block, not the else-block:

```javascript
    function testingLet(name) {
        if (name) {
            let title = 'Mister';
            console.log('Hello ' + title + ' ' + name);
        }
        else {
            console.log('Hello ' + title + ' stranger');
        }
    }
```

The following function will also fail with an error:

```javascript
    function testingLet(name) {
        let name = 'stranger';
        console.log('Hello ' + name);
    }
```
The error message will read:

```javascript
    Uncaught SyntaxError: Identifier 'name' has already been declared
```

Note: if the `let` appears in a separate block than an existing variable with the same name, there's no problem when declaring the variable. With the `let` keyword, the block isolates the scope - not the function. To illustrate, the following function will not result in an error when called:

```javascript
    function testingLet(name) {
        {
            let name = 'stranger';
            console.log('Hello ' + name);
        }
    }
```

## The const keyword

In earlier JavaScript versions, there was no way to declare a constant. Instead, we relied on naming conventions, like using ALL-UPPERCASE variables to hold "constants".
With ES2015 the new `const` keyword declares a constant. If the function attempts to assign a new value to the constant, there will be an error message. For example, the following function defines a NAME constant constant with the String-value of "Precilla". When the next line attempts to assign a new value, it will fail:

```javascript
    function func1() {
        const NAME = "Precilla";
        NAME = 'Mike';
        return "Miss " + NAME;
    }
```

The error message will read: 

<pre>
Uncaught TypeError: Assignment to constant variable.
</pre>

