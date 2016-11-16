Title: Arrays
Date: 2016-01-13
Category: Tutorials
Tags: JavaScript, ES5

The notes for this tutorial do not contain many notes. See the source code for the different array operations. 

# The person.js source file

    :::JavaScript
    /**
     * Simple Person class.
     * Represents a person with name and age.
     */
    function Person(name, age) {
        this.age = age;
        this.name = name;
        this.toString = function() {
            return this.name + ", " + this.age + " years";
        };
    }
    </code></pre>

**Note:**

The toString method is necessary to give the instances of the Person class a textual representation (instead of the default "[Object object]" name).

The following source uses various methods of the array instance.

Note: in the example below, only the following array methods will actually change the array object on which they're invoked:

* push
* splice
* sort

All the other array methods will return a new array as the return value

    :::JavaScript
    function how_to_add_item_to_array() {
        LIST.push("hello");
        // following appears to work in Chrome:
        // (alternative to the push methd)
        // LIST[LIST.length] = "bla";
        // but better use the "official" way with the push method
    }


    function how_to_remove_item_from_array() {
        // Remove item from list using the "splice" string method.
        // The splice method takes two arguments:
        // 1) start index
        // 2) number of items to delete
        LIST.splice(3, 1);
    }


    function how_to_get_sub_range_from_array() {
        // Slice:
        // slice takes two arguments:
        // 1) start index (negative index counts from the end)
        // 2) end index (exclusive). If not used, will slice until the end of array
        LIST = LIST.slice(3, -1);
    }


    function how_to_join_items_into_concatenated_string() {
        // Joining items into a concatenated string:
        alert(LIST.join(" and "));
    }


    function how_to_find_position_within_array() {
        var index = LIST.indexOf(5443);
        alert("position is " + index);
    }


    function how_to_sort_simple_values() {
        LIST.sort();
    }


    function how_to_sort_complex_values() {
        LIST.sort(ageSorter);
    }


    var LIST = [33, 6, 544, 1, 66, 22, 11, 10, 55, 22];


    $(document).ready(function() {
        ////////////////////////////////////////////////////////////////////////////
        // COMMENT OUT THE FOLLOWING GROUPS
        // TO TRY THEM OUT
        ////////////////////////////////////////////////////////////////////////////

        // how_to_add_item_to_array();

        // how_to_remove_item_from_array();

        // how_to_get_sub_range_from_array();

        // how_to_join_items_into_concatenated_string();

        // how_to_find_position_within_array();

        // how_to_sort_simple_values();

        // LIST = [
        //     new Person("Jack", 20),
        //     new Person("Maggie", 29),
        //     new Person("Jose", 27),
        //     new Person("John", 39),
        //     new Person("Ziggie", 66),
        //     new Person("Sally", 29),
        //     new Person("Argor", 19)
        // ];
        // how_to_sort_complex_values();
        
        displayArray(LIST);
    });


    function displayArray(list) {
        var myListThingie = $('<ul>');
        for (var idx=0; idx<list.length; idx++) {
            var item = list[idx];
            myListThingie.append('<li>' + item + '</li>');
        }
        var $resultDiv = $('#array-display');
        $resultDiv.empty();
        $resultDiv.append(myListThingie);
    }


    function ageSorter(a, b) {
        if (a.age < b.age)
            return -1;
        else if (a.age > b.age)
            return 1;
        else
            return 0;
    }
