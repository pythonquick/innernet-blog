Title: ES2015 Part 2: Variable declaration
Date: 2016-09-02 10:00
Category: Tutorials
Tags: JavaScript, ES2015

Part 2 in the series of ES2015 looks at a new way of defining strings, with the ability to substitute variables into place-holders.

# Template Strings

In JavaScript, strings can be created using a pair of double-quotes: " or a pair of single-quotes: '
With ES2015, there's another quotation mark that can be used to define strings: the back tick: `

Strings declared with the back tick have some new options:

* It is possible to insert variable substitutions or expressions. This is done by inserting a ${} inside the string. Any expression can be inserted between the { and }, whether it be a variable name, numeric expression or even the result of a function call
* Strings can span multiple lines. It is not necessary to insert newline characters (\n). One can simply define a string that spans multiple lines that already includes the newline characters

Here's an example:

    :::JavaScript
    function count(legs) {
        return 2*4;
    }

    function intro(person, school, animal) {
        return `Introducing:
        ${person} from ${school}.
        Owns ${count() + 1} ${animal}s`;
    }


    intro("John", "MIT", "bird")

The call to the intro function will return the following string:

<pre>
Introducing:
    John from MIT. 
    Owns 9 birds
</pre>

